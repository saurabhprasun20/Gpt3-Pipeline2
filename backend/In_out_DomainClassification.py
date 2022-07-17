import logging
from nltk.stem import WordNetLemmatizer
from NER_POS import get_data
from fa_chat_close import genResults
from fa_chat_close import getBertAnswer
from gpt3 import answer_gpt3

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

wordnet_lemmatizer = WordNetLemmatizer()

noun_list_final, verb_list_final, verb_noun_rel_dict, verb_token_list, noun_token_list = get_data()


def user_input(inp):
    answer, score = genResults(inp, getBertAnswer)

    if score > 0.65:
        LOGGER.info(f'The user query score is above the threshold of 0.65, so returning answer from the in-domain'
                    f'model for this user query')
        LOGGER.debug(f'The score of the closest question to the user query in the in-domain '
                     f'dataset is {score}')
        LOGGER.debug(f'The closest matched question to the user query in the in-domain '
                     f'dataset is `{answer}`')
        return answer
    else:
        LOGGER.info(f'The user query score for the current question is below the threshold of 0.65, so returning answer'
                    f' from the out-domain model for this query')

        answer_returned = answer_gpt3(inp)
        return answer_returned

