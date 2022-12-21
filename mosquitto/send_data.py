from time import sleep
import paho.mqtt.publish as pub
import json,datetime
from generate_data import *

def send_data(data,topic="test/",address="localhost"):
    assert type(topic)==str
    if type(data)!=type(''):
        j = json.dumps(data,indent=4)
    else:
        j=data
    pld = j
    pub.single(topic,pld,hostname=address)

def send_readings(start_time = datetime.datetime.now()-datetime.timedelta(days=2),\
    address="localhost",homeTopic="/home",
    quarterTopic="/15min",dayTopic="/day",moveSensorTopic = "/movement",withSleep=True):
    th1 = 20
    th2 = 20
    Etot = 0
    Wtot = 0
    movTriggered=0
    i=1
    while True:
        messages=[]
        current_time = start_time+datetime.timedelta(minutes=15*i)
        # print(current_time)
        ## Generate TH[1,2] data using previous readings and append
        th1,th1data = generate_TH(th1,current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/TH1",\
            "payload":th1data})
        th2,th2data = generate_TH(th2,current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/TH2",\
            "payload":th2data})
        ## Generate HVAC[1,2] data and append
        messages.append({"topic":homeTopic+quarterTopic+"/HVAC1",\
            "payload":generateHVAC(current_time)})
        messages.append({"topic":homeTopic+quarterTopic+"/HVAC2",\
            "payload":generateHVAC(current_time)})
        ## Generate MiAC[1,2] readings and append
        messages.append({"topic":homeTopic+quarterTopic+"/MiAC1",\
            "payload":generateMiAC(device=1,time=current_time)})
        messages.append({"topic":homeTopic+quarterTopic+"/MiAC2",\
            "payload":generateMiAC(device=2,time=current_time)})
        ## Generate W1 reading and append.
        W1data = generateW1(time=current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/W1",\
            "payload":W1data})
        ## Generate W1 late data every 20 seconds and append
        if i%20==0:
            print("Generating late W1 data.")
            W1data = generateW1(time=current_time-datetime.timedelta(days=2))
            messages.append({"topic":homeTopic+quarterTopic+"/W1",\
            "payload":W1data})
        ## Generate VERY late W1 data every 120 seconds and append
        if i%120==0:
            print("Generating VERY late W1 data.")
            W1data = generateW1(time=current_time-datetime.timedelta(days=10))
            messages.append({"topic":homeTopic+quarterTopic+"/W1",\
            "payload":W1data})
        ## Randomly generate Mov1 readings and append
        if random.random()>0.5+0.1*movTriggered:
            #print(0.1*movTriggered,movTriggered)
            messages.append({"topic":homeTopic+moveSensorTopic+"/Mov1",\
            "payload":generateMov1(time=current_time)})
            movTriggered+=1
            print(f"Triggered Mov1. Times today: {movTriggered}")
        ## on the final reading for each day, generate daily
        ## sensor readings and append
        if current_time.hour==23 and current_time.minute>=45:
            ##TODO: change time to 00.00 of next day
            print("Generating daily meter data.")
            Etot,Etotdata = generateEtot(Etot,time=current_time)
            messages.append({"topic":homeTopic+dayTopic+"/Etot",\
                "payload":Etotdata})
            Wtot,Wtotdata = generateWtot(Wtot,time=current_time)
            messages.append({"topic":homeTopic+dayTopic+"/Wtot",\
                "payload":Wtotdata})  
            ## Reset times Mov1 was triggered
            movTriggered = 0      
        #print(messages)
        pub.multiple(messages,hostname=address)
        if withSleep:
            sleep(1)
        i+=1
