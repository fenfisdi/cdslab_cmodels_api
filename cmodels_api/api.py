from fastapi import FastAPI, Request


app = FastAPI()


@app.get('/')
def hello(request: Request):
    return {'hello': 'world'}
