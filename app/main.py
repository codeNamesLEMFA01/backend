from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from .routers.names import router as names_router
from .routers.details import router as details_router
from .cron.cron import router as cron_router
from .database import connect_to_mongo
import logging
import argparse
from mongoengine import connect
from .routers.auth import router as auth_router
# from .routers.posts import router as posts_router


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
app.include_router(details_router)
app.include_router(cron_router)
app.include_router(seed_router)
app.include_router(yopByYear)

app.include_router(auth_router)
# app.include_router(posts_router)

def main() -> None:
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
