from fastapi import APIRouter
from fastapi_utilities import repeat_at

from .diversity import diversity
from .yobsBySex import yobsBySex
from .seedDb import seedDb
from .namesCron import namesList
from .lengthNameCron import lengthNameCron
import os

router = APIRouter()


@router.on_event("startup")
def cron_startup() -> None:
    if os.getenv("SEEDER") == "True":
        exec_order()
    else:
        print("SEEDER environment variable is not set to True. Skipping seedDb.")


@repeat_at(cron="* * 1 * *")
def cron_exec():
    exec_order()


def exec_order():
    print("Starting cron tasks")

    seedDb()
    print("seedDb completed")

    yobsBySex()
    print("yobsBySex completed")

    diversity()
    print("diversity completed")

    namesList()
    print("namesList completed")

    lengthNameCron()
    print("lengthNameCron completed")
    print("All startup tasks completed")
