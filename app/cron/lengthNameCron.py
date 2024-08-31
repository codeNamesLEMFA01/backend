import time
from fastapi_utilities import repeat_at
from fastapi import APIRouter
from ..utils.cron.yobLengthNameCron import lengthNameCron
from ..dto.lengthName import get_name_length_trends
from ..models.yobLengthName import MetaSection, MetaMax, MetaEvolution, MetaDescribe, DataSection, YobLengthName


router = APIRouter()

last_execution_time = 0
MIN_INTERVAL = 3600  # 1 hour in seconds

@repeat_at(cron=lengthNameCron)
@router.on_event('startup')
async def lengthNameCron():
    global last_execution_time
    current_time = time.time()

    if current_time - last_execution_time < MIN_INTERVAL:
        print("Skipping execution: too soon since last run")
        return

    last_execution_time = current_time
    obj = get_name_length_trends()

    result = YobLengthName(
        data={
            "male": DataSection(
                years=obj['data']['male']['years'],
                length=obj['data']['male']['length']
            ),
            "female": DataSection(
                years=obj['data']['female']['years'],
                length=obj['data']['female']['length']
            ),
            "global": DataSection(
                years=obj['data']['global']['years'],
                length=obj['data']['global']['length']
            ),
        },
        meta_data=MetaSection(
            max={
                "male": MetaMax(
                    name=obj['meta']['max']['male']['name'],
                    sex=obj['meta']['max']['male']['sex'],
                    birth=int(obj['meta']['max']['male']['birth']),
                    year=int(obj['meta']['max']['male']['year']),
                    ratio=float(obj['meta']['max']['male']['ratio']),
                    name_length=int(obj['meta']['max']['male']['name_length'])
                ),
                "female": MetaMax(
                    name=obj['meta']['max']['female']['name'],
                    sex=obj['meta']['max']['female']['sex'],
                    birth=int(obj['meta']['max']['female']['birth']),
                    year=int(obj['meta']['max']['female']['year']),
                    ratio=float(obj['meta']['max']['female']['ratio']),
                    name_length=int(obj['meta']['max']['female']['name_length'])
                )
            },
            evolution=MetaEvolution(
                male=float(obj['meta']['evolution']['male']),
                female=float(obj['meta']['evolution']['female']),
                global_=float(obj['meta']['evolution']['global'])
                ),
            describe={
                "male": MetaDescribe(
                    count=float(obj['meta']['describe']['male']['count']),
                    mean=float(obj['meta']['describe']['male']['mean']),
                    std=float(obj['meta']['describe']['male']['std']),
                    min=float(obj['meta']['describe']['male']['min']),
                    q25=float(obj['meta']['describe']['male']['25%']),
                    q50=float(obj['meta']['describe']['male']['50%']),
                    q75=float(obj['meta']['describe']['male']['75%']),
                    max=float(obj['meta']['describe']['male']['max'])
                ),
                "female": MetaDescribe(
                    count=float(obj['meta']['describe']['female']['count']),
                    mean=float(obj['meta']['describe']['female']['mean']),
                    std=float(obj['meta']['describe']['female']['std']),
                    min=float(obj['meta']['describe']['female']['min']),
                    q25=float(obj['meta']['describe']['female']['25%']),
                    q50=float(obj['meta']['describe']['female']['50%']),
                    q75=float(obj['meta']['describe']['female']['75%']),
                    max=float(obj['meta']['describe']['female']['max'])
                )
            }
        )
    )

    result.save()
    print("LengthNameCron executed successfully")