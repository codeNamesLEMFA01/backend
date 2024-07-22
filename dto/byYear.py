import json
import pandas as pd
from ..extract.all_names import names

total_birth_by_year_and_sex = pd.pivot_table(names, values='birth', index='year', columns='sex', aggfunc='sum', fill_value=0)

def namesByYear(year):
  return names[names["year"] == year]

def get_names_by_year(year):
  result = {}
  json_str = namesByYear(year).to_json(orient="records")
  result['data'] = json.loads(json_str)
  return result

def get_sum_by_year_and_sex(year):
  result = total_birth_by_year_and_sex.loc[year].to_dict()
  result["year"] = year
  return result

def get_total_by_sex():
  result = {}
  result["data"] = json.loads(total_birth_by_year_and_sex.to_json(orient="index" ))
  result["total"]= names.groupby('sex')['birth'].sum().to_dict()
  result["year"] = {
    "start": int(names["year"].min()),
    "end": int(names["year"].max()),
  }
  return result