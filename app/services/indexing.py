from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import FAISS as FAISSVectorStore

from app.core.settings import settings
from app.services.embedding import get_embedding_model


def get_vectorstore() -> FAISSVectorStore:
    embedding = get_embedding_model()
    try:
        return FAISS.load_local(
            settings.index_file,
            embeddings=embedding,
            allow_dangerous_deserialization=True
        )
    except Exception:
        # Create a new empty FAISS index with the embedding model
        return FAISS.from_texts(
            texts=["init"],
            embedding=embedding,
            metadatas=[{"source": "init"}]
        )


def save_vectorstore(vstore: FAISSVectorStore) -> None:
    vstore.save_local(settings.index_file)
