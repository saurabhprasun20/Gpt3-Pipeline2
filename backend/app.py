from flask import Flask, request
from gpt3 import answer_gpt3
from In_out_DomainClassification import user_input
import json

# from In_out_DomainClassification import user_input
# from fa_chat_close import genResults
# from fa_chat_close import getBertAnswer


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Juli!'


@app.route('/api/v1/answer', methods=['POST'])
def get_gpt3_answer():
    record = json.loads(request.data)
    print(record['answer']['question'])
    inp = [record['answer']['question']]
    answer_returned = user_input(inp)
    # print(token)
    return answer_returned, 200


if __name__ == '__main__':
    app.run(port=8000, debug=True)
