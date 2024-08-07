from fastapi import APIRouter, Request, HTTPException, Query
from ..dto.byYear import get_names_by_year
from ..dto.byYear import get_sum_by_year_and_sex
from ..dto.byYear import get_total_by_sex

from ..dto.trendsNames import trends_name, get_top_names_between_years
from ..dto.trendsNames import get_name_diversity

class NotFoundError(Exception):
    """Exception raised for errors in the input data that lead to not found results."""
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

router = APIRouter(
    prefix="/names",
)

@router.get("/{year}")
def read_names_by_year(request: Request, year: int):
    print(request)
    try:
        return get_names_by_year(year)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sum_by_year/{year}")
def read_sum_by_year(request: Request, year: int):
    try:
        return get_sum_by_year_and_sex(year)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

 def read_total_birth_by_sex(request: Request):
    try:
        return get_total_by_sex()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
 
@router.get("/total_by_sex/")
def read_total_birth_by_sex(request: Request, ):
  try:
    return get_total_by_sex()
  except NotFoundError as e:
    raise HTTPException(status_code=404) from e

@router.get("/trends_name/{name}")
def read_trends_name(request: Request, name: str):
  try:
    return trends_name(name)
  except NotFoundError as e:
    raise HTTPException(status_code=404) from e

@router.get("/trends_name/diversity/")
def read_trends_name(request: Request,):
  try:
    return get_name_diversity()
  except NotFoundError as e:
    raise HTTPException(status_code=404) from e

@router.get("/trends_name/top/")
def read_trends_name(
  request: Request,
  start_year: int = Query(1880, description="The start year for the trend analysis"),
  end_year: int = Query(1900, description="The end year for the trend analysis"),
  top_n: int = Query(10, description="The number of top names to return")
  ):
  try:
    if start_year > end_year:
      raise HTTPException(status_code=400, detail="l'année de début doit être inférieure ou égale à l'année de fin")
    return get_top_names_between_years(start_year, end_year, top_n)
  except NotFoundError as e:
    raise HTTPException(status_code=404) from e
