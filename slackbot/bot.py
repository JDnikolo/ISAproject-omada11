from math import ceil, floor
import slack
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
from flask import Flask, request, Response

app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(BASEDIR, '.env')
load_dotenv(env_path)

slack_token = os.getenv('SLACK_TOKEN')
client = slack.WebClient(token=slack_token)

def format_dtime(iso_dtime):
    utc_dt = iso_dtime[:-1]
    timezone = pytz.timezone("Europe/Athens")
    dtime = datetime.fromisoformat(utc_dt)
    dtime = timezone.localize(dtime)
    return dtime.strftime("%H:%M:%S, %B %d %Y")

@app.route('/alarm', methods=['POST'])
def alarm_notification():
    data = request.json

    dtime = format_dtime(data.get('dtime'))
    alarm_trigger = data.get('alarm_trigger')
    client.chat_postMessage(
        channel="C04DG8G7M4N", 
        blocks = [
        {
        "type": "section",
        "text": {
            "text": f'*Alarm Triggered {dtime}*',
            "type": "mrkdwn"
        },
        "fields": [
        {
            "type": "mrkdwn",
            "text": f'Trigger: {alarm_trigger}'
        }
        ]
        }]
    )
    return Response(), 200

@app.route('/aggregation', methods=['POST'])
def total_notification():
    data = request.json

    dtime = format_dtime(data.get('dtime'))
    aggregation_type = data.get('aggregation_type')
    aggregation = ceil(data.get('aggregation'))
    device_type = data.get('device_type')
    curr_device = data.get('curr_device')
    client.chat_postMessage(
        channel= "C04N3ULSX9R", 
        blocks = [
        {
        "type": "section",
        "text": {
            "text": f'*{device_type}*',
            "type": "mrkdwn"
        },
        "fields" : [
        {
            "type" : "mrkdwn",
            "text" : f'Device: {curr_device}\nDate: {dtime}\n{aggregation_type}: {aggregation}'
        }
        ]
        }
        ]
    )

if (__name__ == '__main__'):
    app.run(debug=True)