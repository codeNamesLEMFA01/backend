from fastapi_utilities import repeat_at
from fastapi import APIRouter
from ..models.yob import Yob
from ..utils.cron.yobNamesCron import yobNamesCron


router = APIRouter()

@repeat_at(cron=yobNamesCron)
@router.on_event('startup')
async def namesList():
    pipeline = [
        {'$group': {
            '_id': {'$toLower': '$name'}
        }},
        {'$project': {
            'name': '$_id',
            '_id': 0
        }},
        {'$sort': {'name': 1}},
        {'$out': 'yobNamesList'}
    ]

    Yob.objects.aggregate(pipeline)