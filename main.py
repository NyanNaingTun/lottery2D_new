import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    time.sleep(180)
    return {"message": "Hello World 180"}


@app.get("/hello/{name}")
async def say_hello(name: str):

    return {"message": f"Hello {name}"}
