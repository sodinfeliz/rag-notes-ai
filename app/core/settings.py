from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Model config - load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API keys
    openai_api_key: str = Field(default=...)

    # RAG settings
    vault_dir: str = Field(default="./tests")
    llm_model_name: str = Field(default="gpt-4.1-mini")
    embedding_model_name: str = "all-MiniLM-L6-v2"

    # File paths
    index_file: str = "ragnote.index"
    sync_log_file: str = "sync_log.json"

    # Chunk settings
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Backend settings
    backend_port: int = Field(default=8000)
    backend_host: str = Field(default="127.0.0.1")
    debug_mode: bool = Field(default=False)

    # Logging settings
    log_file_name: str = "backend.log"
    log_file_backup_count: int = 10
    log_file_max_size: int = 10 * 1024 * 1024  # 10MB

    @property
    def log_file_path(self) -> Path:
        return Path.cwd() / "logs" / self.log_file_name


# Global settings instance
settings = Settings()
