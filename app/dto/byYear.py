import json
from mongoengine import Q
from ..models.yob import Yob
from ..models.yobBySex import YobsBySex
import pandas as pd


def get_names_by_year(year):
    result = {}
    data = Yob.objects(year=year)
    result['data'] = json.loads(data.to_json())
    return result


def get_sum_by_year_and_sex(year):
    pipeline = [
        {'$match': {'year': year}},
        {'$group': {
            '_id': '$sex',
            'total': {'$sum': '$birth'}
            }}
        ]
    result = {item['_id']: item['total'] for item in Yob.objects.aggregate(pipeline)}
    result['total'] = sum(result.values())
    result['year'] = year
    return result


def get_total_by_sex():
    data = [yb.to_dict() for yb in YobsBySex.objects.all()]
    df = pd.DataFrame(data)
    df = df.sort_values('year')

    data_dict = df.set_index('year').to_dict('index')
    total_F = df['F'].sum()
    total_M = df['M'].sum()
    start_year = df['year'].min()
    end_year = df['year'].max()

    max_total_row = df.loc[df['total'].idxmax()]
    max_total_year = int(max_total_row['year'])
    max_total_births = int(max_total_row['total'])

    max_M_row = df.loc[df['M'].idxmax()]
    max_F_row = df.loc[df['F'].idxmax()]

    result = {
        'data': data_dict,
        'total': {
            'F': int(total_F),
            'M': int(total_M)
            },
        'year': {
            'start': int(start_year),
            'end': int(end_year)
            },
        "meta": {
            "max_total": {
                "year": max_total_year,
                "birth": max_total_births
                },
            "max_gender": {
                "M": {
                    "year": int(max_M_row['year']),
                    "birth": int(max_M_row['M']),
                    },
                "F": {
                    "year": int(max_F_row['year']),
                    "birth": int(max_F_row['F']),
                    }
                }
            },
    }
    return result