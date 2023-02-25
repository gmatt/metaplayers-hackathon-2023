from typing import Callable, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from backend.document_retrieval.retriever_reader import get_qa_pipeline, index_documents

app = FastAPI()


class RequestModel(BaseModel):
    query: str
    # TODO Unused.
    retriever_top_k: int = 10
    reader_top_k: int = 5


model: Optional[Callable] = None


@app.on_event("startup")
async def startup_event():
    global model
    index_documents()
    model = get_qa_pipeline()


@app.post("/question")
async def question(request: RequestModel):
    return model(request.query)
