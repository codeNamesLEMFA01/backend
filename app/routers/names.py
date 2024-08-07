from fastapi import APIRouter, Request, HTTPException
from ..dto.byYear import get_names_by_year
from ..dto.byYear import get_sum_by_year_and_sex
from ..dto.byYear import get_total_by_sex

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

@router.get("/total_by_sex/")
def read_total_birth_by_sex(request: Request):
    try:
        return get_total_by_sex()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))