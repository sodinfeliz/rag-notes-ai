import json
from pathlib import Path

from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    INDEX_FILE,
    SYNC_LOG_FILE,
    VAULT_DIR,
)
from app.services.indexing import get_vectorstore, save_vectorstore

router = APIRouter()


@router.post("/update_index")
async def update_index():
    if Path(SYNC_LOG_FILE).exists():
        with open(SYNC_LOG_FILE, "r", encoding="utf-8") as f:
            sync_log = json.load(f)
    else:
        sync_log = {}

    modified_files = []
    for path in Path(VAULT_DIR).rglob("*.md"):
        mtime = path.stat().st_mtime
        if str(path) not in sync_log or sync_log[str(path)] != mtime:
            modified_files.append(path)
            sync_log[str(path)] = mtime

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    all_new_docs = []
    for file_path in modified_files:
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        all_new_docs.extend(chunks)

    if all_new_docs:
        vectorstore = get_vectorstore()
        vectorstore.add_documents(all_new_docs)
        save_vectorstore(vectorstore)

    with open(SYNC_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(sync_log, f, ensure_ascii=False, indent=2)

    return {"updated_files": [str(p) for p in modified_files], "added_chunks": len(all_new_docs)}


@router.get("/status")
async def get_status():
    return {
        "vault_path": Path(VAULT_DIR).resolve(),
        "index_path": Path(INDEX_FILE).resolve(),
        "log_exists": Path(SYNC_LOG_FILE).exists()
    }
