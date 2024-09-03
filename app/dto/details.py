from app.models.yob import Yob


def get_details():
    total_births = Yob.objects().sum("birth")
    top_female = (
        Yob.objects(sex="F")
        .aggregate(
            [
                {"$group": {"_id": "$name", "total_births": {"$sum": "$birth"}}},
                {"$sort": {"total_births": -1}},
                {"$limit": 1},
            ]
        )
        .next()["_id"]
    )

    top_male = (
        Yob.objects(sex="M")
        .aggregate(
            [
                {"$group": {"_id": "$name", "total_births": {"$sum": "$birth"}}},
                {"$sort": {"total_births": -1}},
                {"$limit": 1},
            ]
        )
        .next()["_id"]
    )

    return {
        "top_female_name": top_female,
        "top_male_name": top_male,
        "total_births": total_births,
    }
