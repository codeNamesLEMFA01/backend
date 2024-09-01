import pandas as pd
from ..models.diversity import Diversity
from ..models.yob import Yob
import json


def simpson_index(series):
    N = series.sum()
    return 1 - ((series / N) ** 2).sum()


def make_diversity():
    yobs = Yob.objects()
    names = pd.DataFrame(json.loads(yobs.to_json()))

    diversity_by_year_sex = (
        names.groupby(["year", "sex", "name"])["birth"]
        .sum()
        .groupby(level=[0, 1])
        .agg(simpson_index)
        .reset_index()
    )
    diversity_total = (
        names.groupby(["year", "name"])["birth"]
        .sum()
        .groupby(level=0)
        .agg(simpson_index)
        .reset_index()
    )

    diversity_total = diversity_total.rename(columns={"birth": "Total"})
    merged = pd.merge(diversity_by_year_sex, diversity_total, on="year", how="outer")

    pivoted = merged.pivot(index="year", columns="sex", values="birth").reset_index()
    pivoted = pd.merge(
        pivoted, diversity_total[["year", "Total"]], on="year", how="left"
    )
    total_names = (
        names.groupby("year")["name"]
        .nunique()
        .reset_index()
        .rename(columns={"name": "total_name"})
    )
    pivoted = pd.merge(pivoted, total_names, on="year", how="left")

    pivoted.columns.name = None

    result = pivoted.to_dict(orient="records")
    return result


def get_diversity(start_year, end_year):
    diversities = Diversity.objects(year__gte=start_year, year__lte=end_year)

    df = pd.DataFrame([diversity.to_dict() for diversity in diversities])
    max_diversity_year = df.loc[df["total_name"].idxmax(), "year"]
    max_diversity_count = df["total_name"].max()

    result = {
        "data": df.to_dict("records"),
        "info": {
            "max_diversity_year": int(max_diversity_year),
            "max_diversity_count": int(max_diversity_count),
        },
    }

    return result
