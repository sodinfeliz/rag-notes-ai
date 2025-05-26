import logging
import logging.config
import socket

import uvicorn
from fastapi import FastAPI

from app.api import index, query, status
from app.core.logging_settings import LOGGING_SETTINGS
from app.core.settings import settings

logging.config.dictConfig(LOGGING_SETTINGS)
logger = logging.getLogger("RagNotesAI")

app = FastAPI()

app.include_router(query.router)
app.include_router(index.router)
app.include_router(status.router)


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_available_port(port: int, host: str = "127.0.0.1") -> int:
    while is_port_in_use(port, host):
        port += 1
    return port


if __name__ == "__main__":
    port = settings.backend_port
    if is_port_in_use(port, settings.backend_host):
        port = find_available_port(port, settings.backend_host)

    logger.info(f"Starting backend server on {settings.backend_host}:{port}.")

    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=port,
        reload=settings.debug_mode,
        reload_dirs=["app"],
    )
