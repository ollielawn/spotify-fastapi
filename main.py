from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def initial_connection():
    return {'message': "Hello world"}
