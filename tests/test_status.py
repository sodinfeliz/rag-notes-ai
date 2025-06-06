import json
from datetime import datetime

import pytest

from app.api import status


@pytest.mark.asyncio
async def test_get_status_empty_log(tmp_path, monkeypatch):
    log_file = tmp_path / "sync_log.json"
    log_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(status, "SYNC_LOG_FILE", str(log_file))
    monkeypatch.setattr(status, "VAULT_DIR", tmp_path)
    monkeypatch.setattr(status, "INDEX_FILE", str(tmp_path / "index"))

    result = await status.get_status()

    assert result["log_exists"] is True
    assert result["note_count"] == 0
    assert result["chunk_count"] == 0
    assert result["last_sync_time"] is None


@pytest.mark.asyncio
async def test_get_status_with_entries(tmp_path, monkeypatch):
    log_data = {
        "note1.md": {"mtime": 100.0, "ids": ["1", "2"]},
        "note2.md": {"mtime": 200.0, "ids": ["3"]},
    }
    log_file = tmp_path / "sync_log.json"
    log_file.write_text(json.dumps(log_data), encoding="utf-8")
    monkeypatch.setattr(status, "SYNC_LOG_FILE", str(log_file))
    monkeypatch.setattr(status, "VAULT_DIR", tmp_path)
    monkeypatch.setattr(status, "INDEX_FILE", str(tmp_path / "index"))

    result = await status.get_status()

    assert result["log_exists"] is True
    assert result["note_count"] == 2
    assert result["chunk_count"] == 3
    expected_time = datetime.fromtimestamp(200.0).strftime("%Y-%m-%d %H:%M:%S")
    assert result["last_sync_time"] == expected_time
