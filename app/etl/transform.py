from .extract import extract
import pandas as pd


def transform():
    df = extract()

    # Calculate total births per year
    yearly_total = df.groupby("year")["birth"].sum().reset_index(name="total")
    # Merge original DataFrame with yearly totals
    df_with_total = pd.merge(df, yearly_total, on="year")
    # Calculate birth ratio for each entry
    df_with_total["ratio"] = (df_with_total["birth"] / df_with_total["total"]) * 100
    # Select and reorganize relevant columns
    result = df_with_total[["year", "name", "ratio", "birth", "sex"]]
    # Sort result by year (ascending) and ratio (descending)
    result = result.sort_values(["year", "ratio"], ascending=[True, False])
    return result
