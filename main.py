import uvicorn
from fastapi import FastAPI

from app.api import index, query

app = FastAPI()

app.include_router(query.router)
app.include_router(index.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"],
    )
