import paho.mqtt.publish as pub
import json

def send_data(data,topic="test/",address="localhost"):
    assert type(topic)==str
    if type(data)!=type(''):
        j = json.dumps(data,indent=4)
    else:
        j=data
    pld = j
    pub.single(topic,pld,hostname=address)