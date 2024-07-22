import json
from ..extract.all_names import names

def namesByYear(year):
  return names[names["year"] == year]

def get_names_by_year(year):
  result = {}
  json_str = namesByYear(year).to_json(orient="records")
  result['data'] = json.loads(json_str)
  result["year"] = year
  return result

def get_sum_by_year_and_sex(year):
  result = namesByYear(year).groupby('sex')['birth'].sum().to_dict()
  result["year"] = year
  return result

def get_total_by_sex():
  result= names.groupby('sex')['birth'].sum().to_dict()
  result["year"] = {
    "start": int(names["year"].min()),
    "end": int(names["year"].max()),
  }
  return result