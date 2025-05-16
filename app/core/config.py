import os

from dotenv import load_dotenv

load_dotenv()

# From .env
VAULT_DIR = os.getenv("VAULT_DIR") or "./tests"
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

# Index file path & sync log file
INDEX_FILE = "ragnote.index"
SYNC_LOG_FILE = "sync_log.json"

# Chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Backend settings
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
