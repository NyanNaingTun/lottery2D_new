import json
import time

import uvicorn
from fastapi import FastAPI
import os
from threading import Thread
app = FastAPI()
def thread_fun():
    os.system("venv\Scripts\python lottery_result.py")
    #os.system("python lottery_result.py")

@app.get("/insert")
async def root():

    thread=Thread(target=thread_fun)
    thread.start()
    return {"message": "Success"}

@app.get("/")
async def root():
    return {"welcome": "page"}


@app.get("/result/{name}")
async def say_hello(name: str):
    if(name=='marketclose'or name=='9am'or name=='12pm'or name=='2pm'or name=='4pm'):
        f=open(name+'.json', "r")
        data=json.loads(f.read())
        return data
    else:
        return {"url":["/result/marketclose","/result/9am","/result/12pm","/result/2pm","/result/4pm"]}



