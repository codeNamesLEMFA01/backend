from .extract import extract
import pandas as pd


def transform():
    df = extract()
    yearly_total = df.groupby("year")["birth"].sum().reset_index(name="total")
    df_with_total = pd.merge(df, yearly_total, on="year")
    df_with_total["ratio"] = (df_with_total["birth"] / df_with_total["total"]) * 100
    result = df_with_total[["year", "name", "ratio", "birth", "sex"]]
    result = result.sort_values(["year", "ratio"], ascending=[True, False])
    return result
