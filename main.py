import logging
import logging.config

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


if __name__ == "__main__":
    settings.ensure_backend_port_available()
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug_mode,
        reload_dirs=["app"],
    )
