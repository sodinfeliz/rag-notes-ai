import socket
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
    backend_port: int = Field(default=8600)
    backend_host: str = Field(default="127.0.0.1")
    lm_studio_port: int = 1234
    debug_mode: bool = Field(default=False)

    # Logging settings
    log_file_name: str = "backend.log"
    log_file_backup_count: int = 10
    log_file_max_size: int = 10 * 1024 * 1024  # 10MB

    @property
    def log_file_path(self) -> Path:
        return Path.cwd() / "logs" / self.log_file_name

    def _is_port_in_use(self, port: int, host: str) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    def _find_available_port(self, start_port: int, host: str) -> int:
        while self._is_port_in_use(start_port, host):
            start_port += 1
        return start_port

    def ensure_backend_port_available(self):
        if self._is_port_in_use(self.backend_port, self.backend_host):
            self.backend_port = self._find_available_port(
                self.backend_port, self.backend_host
            )


# Global settings instance
settings = Settings()
