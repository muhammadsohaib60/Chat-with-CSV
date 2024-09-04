from flask import Flask, jsonify, request
from utils.text.chat import chat
from utils.data.main import talkToData
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

app = Flask(__name__)

key = os.environ["OPENAI_API_KEY"]
history = []


@app.route("/", methods=['POST', 'OPTIONS'])
def yaia():

    global key
    # print(request.json)
    inputText = ""

    inputText = request.get_json().get('input_text', "")
    history = request.get_json().get("history", [])
    operationType = "chat data"

    data = pd.read_csv('data.csv', index_col=False)

    output = None
    if operationType == "chat data" or operationType == "process data" or operationType == "visualize data":
        if inputText == None or inputText == "":
            output = "Enter text to communicate with your CSV"
        else:
            output = talkToData(
                data=data, text=inputText, key=key)
        return output

    history.append(f"user: {inputText}")
    history.append(f"assistant: ", {output})
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
