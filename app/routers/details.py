from fastapi import APIRouter, Request, HTTPException, Query

from app.dto.details import get_details

router = APIRouter(
    prefix="/util",
)


@router.get("/info")
def read_names_by_year(request: Request):
    try:
        return get_details()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
