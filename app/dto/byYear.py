import json
from mongoengine import Q
from ..models.yob import Yob
from ..models.yobBySex import Yob



def namesByYear(year):
    return Yob.objects(year=year)


def get_names_by_year(year):
    result = {}
    data = namesByYear(year)
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
    pipeline =[
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

    result = {}
    result['data'] = {str(item['_id']['year']): {item['_id']['sex']: item['total']} for item in data}

    total_pipeline = [
        {'$group': {
            '_id': '$sex',
            'total': {'$sum': '$birth'}
            }}
        ]
    result['total'] = {item['_id']: item['total'] for item in Yob.objects.aggregate(total_pipeline)}

    year_range = Yob.objects.aggregate([
        {'$group': {
            '_id': None,
            'min_year': {'$min': '$year'},
            'max_year': {'$max': '$year'}
            }}
        ]).next()

    result['year'] = {
        'start': year_range['min_year'],
        'end': year_range['max_year']
        }

    return result


def calculate_total_birth_by_year_and_sex():


    pipeline = [
        {'$group': {
            '_id': {'year': '$year', 'sex': '$sex'},
            'total': {'$sum': '$birth'}
            }},
        {'$sort': {'_id.year': 1, '_id.sex': 1}}
        ]
    data = list(Yob.objects.aggregate(pipeline))

    total_birth_by_year_and_sex = {}
    for item in data:
        year = item['_id']['year']
        sex = item['_id']['sex']
        total = item['total']
        if year not in total_birth_by_year_and_sex:
            total_birth_by_year_and_sex[year] = {'M': 0, 'F': 0, 'total': 0}
        total_birth_by_year_and_sex[year][sex] = total
        total_birth_by_year_and_sex[year]['total'] += total

    return total_birth_by_year_and_sex
