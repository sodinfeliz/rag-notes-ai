import pickle
from pathlib import Path
from typing import Any, Dict, List

from langchain_community.vectorstores import FAISS

from app.core.config import INDEX_FILE
from app.services.embedding import get_embedding_model


def inspect_index() -> None:
    """Inspect the contents of the FAISS index pickle file."""
    index_path = Path(INDEX_FILE)
    if not index_path.exists():
        print(f"Index file not found at {index_path}")
        return

    try:
        # Load the FAISS index with the required security parameter
        embedding = get_embedding_model()
        index_data = FAISS.load_local(
            index_path,
            embedding,
            allow_dangerous_deserialization=True  # Safe because we trust our own index file
        )
        
        print("\n=== FAISS Index Contents ===")
        
        # Print basic information
        print(f"\nNumber of documents: {len(index_data.docstore._dict)}")
        
        # Print document contents
        print("\nDocument Contents:")
        print("-" * 50)
        for i, (doc_id, doc) in enumerate(index_data.docstore._dict.items(), 1):
            print(f"\nDocument {i}:")
            print(f"ID: {doc_id}")
            print(f"Content: {doc.page_content[:200]}...")  # First 200 chars
            print(f"Metadata: {doc.metadata}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error reading index file: {e}")


if __name__ == "__main__":
    inspect_index() 