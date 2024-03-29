import logging
from nltk.stem import WordNetLemmatizer
from NER_POS import get_data
from fa_chat_close import genResults
from fa_chat_close import getBertAnswer
from gpt3 import answer_gpt3
from outdoor_activity import get_question_type, current_response
import time

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

wordnet_lemmatizer = WordNetLemmatizer()

noun_list_final, verb_list_final, verb_noun_rel_dict, verb_token_list, noun_token_list = get_data()


def user_input(inp, model_flag=0):
    activity_type = get_question_type(inp[0])
    if activity_type == 'current time':
        return current_response()
    answer, score = genResults(inp, getBertAnswer)

    if score > 0.65:
        LOGGER.info(f'The user query score is above the threshold of 0.65, so returning answer from the in-domain'
                    f'model for this user query')
        LOGGER.debug(f'The score of the closest question to the user query in the in-domain '
                     f'dataset is {score}')
        LOGGER.debug(f'The closest matched question to the user query in the in-domain '
                     f'dataset is `{answer}`')
        return answer, 'Response not from GPT-3'
    else:
        LOGGER.info(f'The user query score for the current question is below the threshold of 0.65, so returning answer'
                    f' from the out-domain model for this query')
        if model_flag == 0:
            start_time = time.time()
            answer_returned = answer_gpt3(inp)
            execution_time = time.time() - start_time
        else:
            start_time = time.time()
            answer_returned = answer_gpt3(inp, curie_flag=1)
            execution_time = time.time() - start_time
        return answer_returned, execution_time
