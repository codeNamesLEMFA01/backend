from fastapi_utilities import repeat_at
from fastapi import APIRouter


router = APIRouter()

@router.on_event('startup')
@repeat_at(cron="yobsBySexCron")
async def yobsBySex():
    pipeline = [
        {'$match': {'sex': {'$in': ['M', 'F']}}},
        {'$group': {
            '_id': {'year': '$year', 'sex': '$sex'},
            'total': {'$sum': '$birth'}
            }
            },
        {'$group': {
            '_id': '$_id.year',
            'M': {'$sum': {'$cond': [{'$eq': ['$_id.sex', 'M']}, '$total', 0]}},
            'F': {'$sum': {'$cond': [{'$eq': ['$_id.sex', 'F']}, '$total', 0]}},
            'total': {'$sum': '$total'}
            }
            },
        {'$project': {
            '_id': 0,
            'data': {
                '$arrayToObject': [[
                    {'k': {'$toString': '$_id'},
                     'v': {
                         'M': '$M',
                         'F': '$F',
                         'total': '$total'
                         }
                     }
                    ]]
                }
            }
            },
        {'$group': {
            '_id': null,
            'data': {'$mergeObjects': '$data'}
            }
            },
        {'$project': {'_id': 0, 'data': 1}},
        {'$out': 'yobsBySex'}
        ]
    data = list(Yob.objects.aggregate(pipeline))
    return data
