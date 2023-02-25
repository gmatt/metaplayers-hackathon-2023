from fastapi import FastAPI

app = FastAPI()


@app.post("/question")
async def root():
    return {"message": "Hello World"}
