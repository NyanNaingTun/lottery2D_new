import json
import time

import uvicorn
from fastapi import FastAPI
import os
import datetime
from threading import Thread
app = FastAPI()
compareservertime=datetime.datetime.now()
def thread_fun():
    #os.system("venv\Scripts\python lottery_result.py")
    os.system("python lottery_result.py")

@app.get("/insert")
async def insert():
    thread=Thread(target=thread_fun)
    thread.start()
    return {"message": "Success"}

@app.get("/")
async def root():
    return {"welcome": "page"}

def excesstime(define_time):
    if(define_time=='9am'):
        if(compareservertime.time()> datetime.time(9,30,0)):
            return True
    elif(define_time=='12pm'):
        if (compareservertime.time() > datetime.time(12, 1,0)):
            return True
    elif(define_time=='2pm'):
        if(compareservertime.time() > datetime.time(14, 0,0)):
            return True
    elif(define_time=='4pm'):
        if(compareservertime.time() > datetime.time(4, 30,0)):
            return True
    else:
        return False
    return False
@app.get("/result/{name}")
async def say_hello(name: str):
    if(name=='marketclose'or name=='9am'or name=='12pm'or name=='2pm'or name=='4pm'):
        f=open(name+'.json', "r")
        data=json.loads(f.read())
        return data
    else:
        return {"url":["/result/marketclose","/result/9am","/result/12pm","/result/2pm","/result/4pm"]}


@app.get("/selectedresult/{name}")
async def say_hello(name: str):
    global compareservertime
    if ( name == '9am' or name == '12pm' or name == '2pm' or name == '4pm'):
        tempsetdata = {"temp": "temp"}
        finaldata={"temp": "temp"}
        f = open(name + '.json', "r")
        data = json.loads(f.read())
        for setlist in data[name]:
            compareservertime=datetime.datetime.strptime(setlist['stocktime_mm'], "%d/%m/%y %H:%M:%S")
            tempsetdata = setlist
            if (excesstime(name)):
                finaldata=tempsetdata
                break

        return {name+"_result":finaldata,"datalist":data}
    else:
        return {"url": [ "/selectedresult/9am", "/selectedresult/12pm", "/selectedresult/2pm", "/selectedresult/4pm"]}



