import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    #time.sleep(180)
    exec(open("hello.py").read())
    return {"message": "Hello World "}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
