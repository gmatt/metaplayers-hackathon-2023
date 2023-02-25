from typing import Callable

from haystack import Document
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers

from backend.scraping.clean_text import CLEANED_OUTPUT_DIR

INDEX_DOCUMENTS_PATH = CLEANED_OUTPUT_DIR

document_store = ElasticsearchDocumentStore()

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_format="sentence_transformers",
)


def index_documents():
    document_store.delete_all_documents()

    docs = []
    for file in CLEANED_OUTPUT_DIR.glob("*"):
        # We concatenate the title with the text to provide context.
        h1 = ""
        h2 = ""
        h3 = ""
        for line in file.read_text().splitlines():
            if line.startswith("# "):
                h1 = line[2:]
            elif line.startswith("## "):
                h2 = line[3:]
            elif line.startswith("### "):
                h3 = line[4:]
            else:
                docs.append(
                    Document(
                        content=f"{h1}/{h2}/{h3} [SEP] {line}",
                        meta={"name": file.name},
                    )
                )

    document_store.write_documents(docs)
    document_store.update_embeddings(
        retriever,
        update_existing_embeddings=False,
    )


def get_qa_pipeline() -> Callable[[str], dict]:
    reader = FARMReader(
        model_name_or_path="deepset/xlm-roberta-large-squad2",
        use_gpu=True,
    )

    pipe = ExtractiveQAPipeline(reader, retriever)

    def predict(query: str) -> dict:
        return pipe.run(
            query=query,
            params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}},
        )

    return predict

    # print_answers(prediction)


if __name__ == "__main__":
    pass

    # docs = here("../data/scraped/1_per_1975. (II. 5.) KPM–BM együttes rendelet.txt").read_text().splitlines()
    # # docs = [Document(content=d) for d in docs]
    #
    # docs = [
    #     Document(content=" ===apple=== hello", meta={"headlines": "apple"}),
    #     Document(
    #         content=" ===America=== world",
    #         meta={"headlines": "America", "name": "America", "title": "America"},
    #     ),
    # ]

    # document_store.write_documents(docs)

    index_documents()
    model = get_qa_pipeline()

    prediction = model("Mennyivel mehetek lakott területen belül autóval?")
    print_answers(prediction)
