from fastapi import APIRouter, Request, HTTPException, Query

from app.dto.details import get_details
from ..auth.authServices import get_current_active_user
from fastapi import Depends
from typing import Annotated
from ..models.users import User

router = APIRouter(
    prefix="/util",
)


@router.get("/info")
def read_names_by_year(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        return get_details()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
