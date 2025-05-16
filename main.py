import socket

import uvicorn
from fastapi import FastAPI

from app.api import index, query
from app.core.config import BACKEND_HOST, BACKEND_PORT

app = FastAPI()

app.include_router(query.router)
app.include_router(index.router)


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_available_port(port: int, host: str = "127.0.0.1") -> int:
    while is_port_in_use(port, host):
        port += 1
    return port


if __name__ == "__main__":
    port = BACKEND_PORT
    if is_port_in_use(port, BACKEND_HOST):
        port = find_available_port(port, BACKEND_HOST)

    print(f"Starting backend server on {BACKEND_HOST}:{port}.")

    uvicorn.run(
        "main:app",
        host=BACKEND_HOST,
        port=port,
        reload=True,
        reload_dirs=["app"],
    )
