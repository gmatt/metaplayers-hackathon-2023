from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers
from pyprojroot import here

if __name__ == "__main__":
    document_store = InMemoryDocumentStore()

    docs = here("../data/kresz.txt").read_text().splitlines()
    docs = [Document(content=d) for d in docs]

    document_store.write_documents(docs)

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        model_format="sentence_transformers",
    )

    document_store.update_embeddings(retriever)

    reader = FARMReader(
        model_name_or_path="deepset/xlm-roberta-large-squad2",
        use_gpu=True,
    )

    pipe = ExtractiveQAPipeline(reader, retriever)

    prediction = pipe.run(
        query="Használhatom a mobilom vezetés közben?",
        params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}},
    )

    print_answers(prediction)
