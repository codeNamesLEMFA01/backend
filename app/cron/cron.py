from fastapi import APIRouter
from fastapi_utilities import repeat_at

from .diversity import diversity
from .yobsBySex import yobsBySex
from .seedDb import seedDb

router = APIRouter()


@repeat_at(cron="* * 1 * *")
@router.on_event("startup")
def cron_startup() -> None:
    print("Starting cron tasks")

    seedDb()
    print("seedDb completed")

    yobsBySex()
    print("yobsBySex completed")

    diversity()
    print("diversity completed")

    print("All startup tasks completed")
