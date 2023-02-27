from sys import argv
from time import sleep
import paho.mqtt.publish as pub
import json,datetime
from generate_data import *
import math
import argparse

def send_data(data,topic="test/",address="localhost"):
    assert type(topic)==str
    if type(data)!=type(''):
        j = json.dumps(data,indent=4)
    else:
        j=data
    pld = j
    pub.single(topic,pld,hostname=address)

def send_readings(stop:int = math.inf, step:int=1, start:datetime = datetime.datetime.now(),\
    address="localhost",homeTopic="/home",
    quarterTopic="/15min",dayTopic="/day",moveSensorTopic = "/movement",
    withSleep=True, delay:float=1.0,qos:int=1,retain=False):
    th1 = 20
    th2 = 20
    Etot = 0
    Wtot = 0
    movTriggered=0
    i=0
    start_time=datetime.datetime(start.year,start.month,start.day)
    current_time=start_time
    current_day = current_time.day
    while i<=stop*step:
        messages=[]
        # print(current_time)
        ## Generate TH[1,2] data using previous readings and append
        th1,th1data = generate_TH(th1,current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/TH/TH1",\
            "payload":th1data,"qos":qos,"retain":retain})
        th2,th2data = generate_TH(th2,current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/TH/TH2",\
            "payload":th2data,"qos":qos,"retain":retain})
        ## Generate HVAC[1,2] data and append
        messages.append({"topic":homeTopic+quarterTopic+"/HVAC/HVAC1",\
            "payload":generateHVAC(current_time),"qos":qos,"retain":retain})
        messages.append({"topic":homeTopic+quarterTopic+"/HVAC/HVAC2",\
            "payload":generateHVAC(current_time),"qos":qos,"retain":retain})
        ## Generate MiAC[1,2] readings and append
        messages.append({"topic":homeTopic+quarterTopic+"/MiAC/MiAC1",\
            "payload":generateMiAC(device=1,time=current_time),"qos":qos,"retain":retain})
        messages.append({"topic":homeTopic+quarterTopic+"/MiAC/MiAC2",\
            "payload":generateMiAC(device=2,time=current_time),"qos":qos,"retain":retain})
        ## Generate W1 reading and append.
        W1data = generateW1(time=current_time)
        messages.append({"topic":homeTopic+quarterTopic+"/W/W1",\
            "payload":W1data,"qos":qos,"retain":retain})
        ## Generate W1 late data every 20 seconds and append
        if i%20==0:
            print("Generating late W1 data.")
            W1data = generateW1(time=current_time-datetime.timedelta(days=1)\
                +datetime.timedelta(seconds=random.randint(1,59),minutes=random.randint(0,10)))
            messages.append({"topic":homeTopic+quarterTopic+"/W/W1",\
            "payload":W1data,"qos":qos,"retain":retain})
        ## Generate VERY late W1 data every 120 seconds and append
        if i%120==0:
            print("Generating VERY late W1 data.")
            W1data = generateW1(time=current_time-datetime.timedelta(days=10)\
                +datetime.timedelta(seconds=random.randint(1,59),minutes=random.randint(0,10)))
            messages.append({"topic":homeTopic+quarterTopic+"/W/W1",\
            "payload":W1data,"qos":qos,"retain":retain})
        ## Randomly generate Mov1 readings and append
        if random.random()>0.5+0.1*movTriggered:
            #print(0.1*movTriggered,movTriggered)
            messages.append({"topic":homeTopic+moveSensorTopic+"/Mov1",\
            "payload":generateMov1(time=current_time),"qos":qos,"retain":retain})
            movTriggered+=1
            print(f"Triggered Mov1. Times today: {movTriggered}")
        ## on the final reading for each day, generate daily
        ## sensor readings and append
        if current_day != current_time.day:
            print("Generating daily meter data.")
            Etot,Etotdata = generateEtot(Etot,time=current_time-datetime.timedelta(days=1))
            messages.append({"topic":homeTopic+dayTopic+"/Etot",\
                "payload":Etotdata,"qos":qos,"retain":retain})
            Wtot,Wtotdata = generateWtot(Wtot,time=current_time-datetime.timedelta(days=1))
            messages.append({"topic":homeTopic+dayTopic+"/Wtot",\
                "payload":Wtotdata,"qos":qos,"retain":retain})  
            ## Reset times Mov1 was triggered
            movTriggered = 0
            current_day=current_time.day      
        #print(messages)
        pub.multiple(messages,hostname=address)
        if withSleep:
            sleep(delay)
        i+=step
        current_time = start_time+datetime.timedelta(minutes=15*i)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate meter readings.")
    parser.add_argument('-amount',dest="a",help="the amount of 15-minute readings to be generated (default: infinite)",
    default=math.inf,type=int)
    parser.add_argument('-step',dest="s",help="the amount of 15-minute step(s) taken after generation (default: 1)",
    default=1,type=int)
    parser.add_argument('-wait',dest="w",help="the delay in seconds between steps (default: 1.0)",
    default=1.0,type=float)
    args=parser.parse_args()
    send_readings(stop=args.a,step=args.s,delay=args.w)
        