from typing import Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .routers.names import router as names_router
from .cron.seedDb import router as seed_router
from .cron.yobsBySex import router as yopByYear
from .database import connect_to_mongo
import logging
import argparse
from mongoengine import connect


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return Response("Server is running.")


@app.on_event("startup")
async def startup_event():
    connect_to_mongo()
    logging.basicConfig(level=logging.INFO)


# Inclure le routeur
app.include_router(names_router)
app.include_router(seed_router)
app.include_router(yopByYear)


def main() -> None:
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
