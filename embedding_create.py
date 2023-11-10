from transformers import AutoTokenizer, AutoModel


def create_embeddings(paragraphs):
    model = AutoModel.from_pretrained(
        "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
    )

    embeddings = model.encode(paragraphs)
    return embeddings
