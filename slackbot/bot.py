import slack
import os
from dotenv import load_dotenv
from flask import Flask, request, Response

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(BASEDIR, '.env')
load_dotenv(env_path)

slack_token = os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=slack_token)




@app.route('/notification', methods=['POST'])
def notification():
    data = request.form
    ts = data.get('ts')
    client.chat_postMessage(channel="#test", text=f'{ts}')
    return Response(), 200

if (__name__ == '__main__'):
    app.run(debug=True)