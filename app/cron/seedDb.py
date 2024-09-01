from ..etl.load import load
from ..auth.seedDb import seed_users_db
from ..utils.cron.seedDb import cronSeedDb
from fastapi_utilities import repeat_at
from fastapi import APIRouter
import os


def seedDb():
    try:
        print("Starting seedDb")
        result = load()
        print("seedDb completed successfully")
        return result
    except Exception as e:
        print(f"Error in seedDb: {e}")
        return False
