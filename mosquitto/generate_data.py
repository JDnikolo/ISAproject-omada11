import datetime,random

# returns the new temperature value and the string to be sent via MQTT
def generate_TH(previous=20,time=datetime.datetime.now()):
    new = previous+random.uniform(-2.1,2.1)
    if new>35.0:
        new=35.0
    if new<12.0:
        new=12.0
    return new,time.strftime("%Y-%m-%d %H:%M:%S")+"|"+str(new)[:5]

def generateHVAC(time=datetime.datetime.now()):
    new = random.randint(0,100)
    return time.strftime("%Y-%m-%d %H:%M:%S")+"|"+str(new)[:5]

def generateMiAC(device = 1,time = datetime.datetime.now()):
    if device == 1:
        new = random.randint(0,150)
    else:
        new = random.randint(0,200)
    return time.strftime("%Y-%m-%d %H:%M:%S")+"|"+str(new)[:5]

def generateEtot(previous, time = datetime.datetime.now()):
    time=time+datetime.timedelta(hours=24)
    new = previous + 2600*24 +random.randint(-1000,1000)
    return new,time.strftime("%Y-%m-%d 00:00:00")+"|"+str(new)

def generateW1(time=datetime.datetime.now()):
    new = random.random()
    return time.strftime("%Y-%m-%d %H:%M:%S")+"|"+str(new)[:5]

def generateWtot(previous,time=datetime.datetime.now()):
    time=time+datetime.timedelta(hours=24)
    new = previous + 110 +random.randint(-10,10)
    return new,time.strftime("%Y-%m-%d 00:00:00")+"|"+str(new)

def generateMov1(time=datetime.datetime.now()):
    return time.strftime("%Y-%m-%d %H:%M:%S")+"|"+str(1)
