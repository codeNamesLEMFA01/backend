from mongoengine import DoesNotExist
from ..models.diversity import Diversity
from ..dto.diversity import make_diversity


def diversity():
    result = make_diversity()
    for record in result:
        try:
            diversity = Diversity.objects.get(year=record["year"])

            diversity.F = record["F"]
            diversity.M = record["M"]
            diversity.total = record["Total"]
            diversity.total_name = record["total_name"]
        except DoesNotExist:
            diversity = Diversity(
                year=record["year"],
                F=record["F"],
                M=record["M"],
                total=record["Total"],
                total_name=record["total_name"],
            )

        diversity.save()

    return result
