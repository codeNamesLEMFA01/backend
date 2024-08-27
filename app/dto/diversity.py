import json
import pandas as pd
from ..models.yob import Yob

def get_diversity(start_year, end_year):
    def simpson_index(series):
        N = series.sum()
        return 1 - ((series / N) ** 2).sum()

    yobs = Yob.objects(year__gte=start_year, year__lte=end_year)
    names = pd.DataFrame(json.loads(yobs.to_json()))

    diversity_by_year_sex = names.groupby(["year", "sex", "name"])["birth"].sum().groupby(level=[0, 1]).agg(simpson_index).reset_index()
    diversity_total = names.groupby(["year", "name"])["birth"].sum().groupby(level=0).agg(simpson_index).reset_index()

    diversity_total = diversity_total.rename(columns={"birth": "Total"})
    merged = pd.merge(diversity_by_year_sex, diversity_total, on="year", how="outer")

    pivoted = merged.pivot(index="year", columns="sex", values="birth").reset_index()
    pivoted = pd.merge(pivoted, diversity_total[['year', 'Total']], on='year', how='left')

    pivoted.columns.name = None

    result = pivoted.to_dict(orient="records")

    return json.dumps(result)