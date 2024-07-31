from typing import Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .routers.names import router as names_router
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

# models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
  return Response("Server is running.")

app.include_router(names_router)
# app.include_router(posts_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

print("🧨 HELL 🤘")