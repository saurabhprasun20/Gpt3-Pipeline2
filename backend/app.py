import ast
import json
import logging
import time
# import psycopg2
from flask import Flask, request, g as app_ctx
from In_out_DomainClassification import user_input
from flask_pymongo import PyMongo

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/juli-chat")
db = mongodb_client.db
time_in_ms = 0
input_global = ''
answer_global = ''
flag = 0
gpt3_time = 'Response not from GPT-3'


@app.route('/')
def hello_world():
    print("Get method")
    return 'Hello Juli!'


@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    LOGGER.info(f'The total execution time for the request is: {time_in_ms} ms {request.method}')
    LOGGER.info(f'The input is {input_global} and the answer is {answer_global}')

    if flag == 0:
        db.davinci_avg.insert_one({'question': input_global[0], 'answer': answer_global, 'time': time_in_ms,
                                   'gpt3-time': gpt3_time*1000})

    else:
        db.curie_avg.insert_one({'question': input_global[0], 'answer': answer_global, 'time': time_in_ms,
                                'gpt3-time': gpt3_time*1000})

    return response


@app.route('/api/v1/answer', methods=['POST'])
def get_gpt3_answer():
    global input_global
    global answer_global
    global flag
    global gpt3_time
    record = json.loads(request.data)
    print(record['answer']['question'])
    inp = [record['answer']['question']]
    answer_returned, gpt3_time = user_input(inp)
    LOGGER.info(f'Answer returned is {answer_returned}')
    LOGGER.info(f'The time for GPT-3 is {gpt3_time}')
    if "[" in answer_returned:
        answer_returned = answer_returned.replace('[', '').replace(']', '')
    LOGGER.info(f'Answer after change is {answer_returned}')
    input_global = inp
    answer_global = answer_returned
    flag = 0
    return answer_returned, 200


@app.route('/api/v1/answer_curie', methods=['POST'])
def get_gpt3_answer_curie():
    global input_global
    global answer_global
    global flag
    record = json.loads(request.data)
    print(record['answer']['question'])
    inp = [record['answer']['question']]
    answer_returned = user_input(inp, model_flag=1)
    LOGGER.info(f'Answer returned is {answer_returned}, {type(answer_returned)}')
    if "[" in answer_returned:
        answer_returned = answer_returned.replace('[', '').replace(']', '')
        # answer_returned = answer_returned[0]
    print(answer_returned)
    input_global = inp
    answer_global = answer_returned
    flag = 1
    return answer_returned, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
