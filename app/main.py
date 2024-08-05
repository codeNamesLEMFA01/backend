from typing import Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .routers.names import router as names_router
import argparse
from mongoengine import connect
from .database import get_db
from .extract.all_names import run_yob_import

# parser = argparse.ArgumentParser()
# parser.add_argument("--seed", action="store_true",default=False ,help="Enable debug mode")
# args = parser.parse_args()

db = get_db()
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

app.include_router(names_router)
# app.include_router(posts_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)


# run_yob_import(db)
print("🧨 HELL 🤘")

from fastapi import Depends
