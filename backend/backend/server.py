from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers
from pyprojroot import here

if __name__ == "__main__":
    document_store = InMemoryDocumentStore()

    docs = here("../data/kresz_eng.txt").read_text().splitlines()
    docs = [Document(content=d) for d in docs]

    document_store.write_documents(docs)

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        model_format="sentence_transformers",
    )

    document_store.update_embeddings(retriever)

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    pipe = ExtractiveQAPipeline(reader, retriever)

    prediction = pipe.run(
        query="Can I use my phone while driving?",
        params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}},
    )

    print_answers(prediction)
