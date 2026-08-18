from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from syfu.api.routers.api import api_router
from syfu.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("syfu.main:app", host="0.0.0.0", port=8000)
