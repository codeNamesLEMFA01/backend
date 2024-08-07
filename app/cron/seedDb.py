from ..database import db
from ..extract.all_names import run_yob_import
from ..utils.cron.seedDb import cronSeedDb
from fastapi_utilities import repeat_at
from fastapi import APIRouter
import os


router = APIRouter()

@repeat_at(cron=cronSeedDb)
@router.on_event("startup")
async def seedDb():
    try:
        if (os.getenv("SEEDER") == "True"):
            print("Starting seedDb")
            run_yob_import(db)
            print("seedDb completed successfully")
    except Exception as e:
        print(f"Error in seedDb: {e}")