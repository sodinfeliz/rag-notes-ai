import json
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from app.core.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    INDEX_FILE,
    SYNC_LOG_FILE,
    VAULT_DIR,
)
from app.services.indexing import get_vectorstore, save_vectorstore

router = APIRouter()


def generate_docs_ids(
    path: Path,
    splitter: TextSplitter,
) -> tuple[list[Document], list[str]]:
    """Generate documents and ids from a path.

    Args:
        path (Path): The absolute path to the file to load.
        splitter (TextSplitter): The splitter to use to split the documents.

    Returns:
        tuple[list[Document], list[str]]: A tuple of documents and ids.
    """
    loader = TextLoader(path, encoding="utf-8")
    rel_path = str(path.relative_to(Path(VAULT_DIR)))

    docs = loader.load()
    docs[0].metadata = {"source": rel_path}

    # Chunks will inherit the metadata of the original document
    chunks = splitter.split_documents(docs)
    ids = [str(uuid4()) for _ in chunks]

    return chunks, ids


@router.post("/update_index")
async def update_index():
    if Path(SYNC_LOG_FILE).exists():
        with open(SYNC_LOG_FILE, encoding="utf-8") as f:
            sync_log = json.load(f)
    else:
        sync_log = {}

    modified_files, new_files = [], []

    for path in Path(VAULT_DIR).rglob("*.md"):
        mtime = path.stat().st_mtime
        file_name = path.name

        if file_name not in sync_log:
            new_files.append(path)
            sync_log[file_name] = {"mtime": mtime, "ids": []}
        elif sync_log[file_name]["mtime"] != mtime:
            modified_files.append(path)
            sync_log[file_name]["mtime"] = mtime

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    all_new_docs, all_new_ids = [], []
    vectorstore = get_vectorstore()

    # Delete the modified files from the vectorstore
    for file_path in modified_files:
        file_name = file_path.name
        vectorstore.delete(sync_log[file_name]["ids"])
        sync_log[file_name]["ids"] = []

    for file_path in new_files + modified_files:
        file_name = file_path.name
        chunks, ids = generate_docs_ids(file_path, splitter)

        all_new_docs.extend(chunks)
        all_new_ids.extend(ids)
        sync_log[file_name]["ids"].extend(ids)

    if all_new_docs:
        vectorstore.add_documents(documents=all_new_docs, ids=all_new_ids)
        save_vectorstore(vectorstore)

    with open(SYNC_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(sync_log, f, ensure_ascii=False, indent=2)

    return {
        "updated_files": [str(p) for p in modified_files + new_files],
        "added_chunks": len(all_new_docs),
    }


@router.get("/status")
async def get_status():
    return {
        "vault_path": Path(VAULT_DIR).resolve(),
        "index_path": Path(INDEX_FILE).resolve(),
        "log_exists": Path(SYNC_LOG_FILE).exists()
    }
