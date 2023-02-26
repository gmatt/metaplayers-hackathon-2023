from typing import Callable

from haystack import Document
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline

from backend.scraping.clean_html import CLEANED_OUTPUT_DIR

INDEX_DOCUMENTS_PATH = CLEANED_OUTPUT_DIR

# document_store = InMemoryDocumentStore()
document_store = ElasticsearchDocumentStore()

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_format="sentence_transformers",
)


def index_documents():
    """Create embedding for paragraphs. Show, but only need to happen once."""
    # document_store.delete_documents()

    docs = []
    for file in CLEANED_OUTPUT_DIR.glob("*"):
        url = "https://njt.hu/jogszabaly/" + file.stem
        title = None
        subtitle = None
        jhid = None
        last_line = ""
        for line in file.read_text().splitlines():
            if not line:
                continue

            # My custom marks in the scraped data. Not to be included in the final text.
            if line.startswith("<note>jhId="):
                jhid = line[11:-7]
                continue
            elif line.startswith("<note>jogszabalyMainTitle="):
                title = line[26:-7]
                continue
            elif line.startswith("<note>jogszabalySubtitle="):
                subtitle = line[25:-7]
                continue

            if line.startswith(" "):
                line = f"{last_line} [SEP] {line}"
            else:
                last_line = line

            docs.append(
                Document(
                    content=f"{line}",
                    meta={
                        "name": file.name,
                        "title": title,
                        "subtitle": subtitle,
                        "url": url,
                        "jhid": jhid,
                    },
                )
            )

    document_store.write_documents(docs)
    document_store.update_embeddings(
        retriever,
        update_existing_embeddings=False,
    )


def get_qa_pipeline() -> Callable[[str], dict]:
    """Question answering pipeline. Returns a predictor function."""
    reader = FARMReader(
        model_name_or_path="deepset/xlm-roberta-large-squad2",
        use_gpu=True,
    )

    pipe = ExtractiveQAPipeline(reader, retriever)

    def predict(query: str, retriever_top_k: int, reader_top_k: int) -> dict:
        return pipe.run(
            query=query,
            params={
                "Retriever": {"top_k": retriever_top_k},
                "Reader": {"top_k": reader_top_k},
            },
        )

    return predict

    # print_answers(prediction)


if __name__ == "__main__":
    index_documents()
