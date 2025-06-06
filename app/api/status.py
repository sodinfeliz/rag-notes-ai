import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter

from app.core.config import INDEX_FILE, SYNC_LOG_FILE, VAULT_DIR

router = APIRouter()

@router.get("/status")
async def get_status():
    status = {
        "vault_path": str(VAULT_DIR),
        "index_path": INDEX_FILE,
        "log_exists": Path(SYNC_LOG_FILE).exists(),
    }

    if Path(SYNC_LOG_FILE).exists():
        with open(SYNC_LOG_FILE, encoding="utf-8") as f:
            sync_log = json.load(f)

        if sync_log:
            note_count = len(sync_log)
            chunk_count = sum(len(v["ids"]) for v in sync_log.values())
            last_sync = max(v.get("mtime", 0.0) for v in sync_log.values())
            status.update({
                "note_count": note_count,
                "chunk_count": chunk_count,
                "last_sync_time": datetime.fromtimestamp(last_sync).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            })
        else:
            status.update({
                "note_count": 0,
                "chunk_count": 0,
                "last_sync_time": None,
            })
    else:
        status.update({
            "note_count": 0,
            "chunk_count": 0,
            "last_sync_time": None,
        })

    return status
