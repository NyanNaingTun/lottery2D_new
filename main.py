import time

import uvicorn
from fastapi import FastAPI
import os
from threading import Thread
app = FastAPI()
def thread_fun():
    os.system("venv\Scripts\python lottery_result.py")
    os.system("python lottery_result.py")

@app.get("/")
async def root():

    thread=Thread(target=thread_fun)
    thread.start()
    return {"message": "Hello World2 "}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




