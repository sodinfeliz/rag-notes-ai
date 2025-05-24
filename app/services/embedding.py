from langchain_huggingface import HuggingFaceEmbeddings

from app.core.settings import settings


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model_name)
