from typing import Callable, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from backend.document_retrieval.retriever_reader import get_qa_pipeline, index_documents

app = FastAPI()


class RequestModel(BaseModel):
    query: str
    retriever_top_k: int = 10
    reader_top_k: int = 5


model: Optional[Callable] = None


@app.on_event("startup")
async def startup_event():
    global model
    model = get_qa_pipeline()


@app.post("/create-index")
async def index():
    index_documents()


@app.post("/question")
async def question(request: RequestModel):
    return model(
        query=request.query,
        retriever_top_k=request.retriever_top_k,
        reader_top_k=request.reader_top_k,
    )
