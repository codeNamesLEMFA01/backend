from ..models.yob import Yob


def yobsBySex():
    pipeline = [
        {"$match": {"sex": {"$in": ["M", "F"]}}},
        {
            "$facet": {
                "byYear": [
                    {
                        "$group": {
                            "_id": "$year",
                            "M": {
                                "$sum": {"$cond": [{"$eq": ["$sex", "M"]}, "$birth", 0]}
                            },
                            "F": {
                                "$sum": {"$cond": [{"$eq": ["$sex", "F"]}, "$birth", 0]}
                            },
                            "total": {"$sum": "$birth"},
                        }
                    }
                ]
            }
        },
        {"$unwind": "$byYear"},
        {"$replaceRoot": {"newRoot": "$byYear"}},
        {"$project": {"year": "$_id", "M": 1, "F": 1, "total": 1, "_id": 0}},
        {"$out": "yobsBySex"},
    ]
    data = list(Yob.objects.aggregate(pipeline))
    return data
