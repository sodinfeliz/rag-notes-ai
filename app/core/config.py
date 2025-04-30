from pathlib import Path

# Obsidian vault directory
VAULT_DIR = Path("./test").resolve()

# Index file path & sync log file
INDEX_FILE = "ragnote.index"
SYNC_LOG_FILE = "sync_log.json"

# Embedding model name
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# OpenAI LLM model name
OPENAI_MODEL_NAME = "gpt-4o-mini"

# Chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
