import uvicorn
from fastapi import FastAPI

from app.api import index, query
from app.core.config import BACKEND_PORT

app = FastAPI()

app.include_router(query.router)
app.include_router(index.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=BACKEND_PORT,
        reload=True,
        reload_dirs=["app"],
    )
