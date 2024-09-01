from ..models.yob import Yob


def namesList():
    pipeline = [
        {"$group": {"_id": {"$toLower": "$name"}}},
        {"$project": {"name": "$_id", "_id": 0}},
        {"$sort": {"name": 1}},
        {"$out": "yobNamesList"},
    ]

    Yob.objects.aggregate(pipeline)
