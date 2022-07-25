import json
import time
from flask import Flask, request, g as app_ctx
from In_out_DomainClassification import user_input
import logging
import ast

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

app = Flask(__name__)


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
    return response


@app.route('/api/v1/answer', methods=['POST'])
def get_gpt3_answer():
    record = json.loads(request.data)
    print(record['answer']['question'])
    inp = [record['answer']['question']]
    answer_returned = user_input(inp)
    LOGGER.info(f'Answer returned is {answer_returned}, {type(answer_returned)}')
    if "[" in answer_returned:
        print('true, this shit is happening dawg')
        answer_returned = ast.literal_eval(answer_returned.strip())
        print(f'{answer_returned}')
        answer_returned = answer_returned[0]
    return answer_returned, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
