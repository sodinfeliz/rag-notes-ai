from fastapi import FastAPI

from app.api import index, query

app = FastAPI()

app.include_router(query.router)
app.include_router(index.router)
