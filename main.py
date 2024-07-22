from typing import Union
from fastapi import FastAPI
import pandas as pd

from .extract.all_names import names
from .dto.byYear import get_names_by_year
from .dto.byYear import get_sum_by_year_and_sex
from .dto.byYear import get_total_by_sex

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/names/{year}")
def read_names_by_year(year: int):
  return get_names_by_year(year)

@app.get("/names/sum_by_year/{year}")
def read_sum_by_year(year: int):
  return get_sum_by_year_and_sex(year)

@app.get("/names/total_by_sex/")
def read_total_birth_by_sex():
  return get_total_by_sex()