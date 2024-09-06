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
        .next()
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
        .next()
    )

    return {
        "top_female_name": {"name": top_female["_id"], "total_births": top_female["total_births"]},
        "top_male_name": {"name": top_male["_id"], "total_births": top_male["total_births"]},
        "total_births": total_births,
    }
