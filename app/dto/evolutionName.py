from mongoengine import Q
from ..models.yob import Yob
import json
import pandas as pd
from fastapi import HTTPException

def get_name_trend(name):
    data = Yob.objects(name=name)
    result = json.loads(data.to_json())

    if len(result) > 0:
        return pd.DataFrame(result)
    else:
        raise HTTPException(status_code=404, detail="Not Found")

def evolution_name(name):
    name = name.strip().capitalize()
    df = get_name_trend(name)

    sex = {'M': 0, 'F': 0}
    sex.update(df.groupby('sex')['birth'].sum().to_dict())

    pivot_table_by_name_year_sex = pd.pivot_table(df, values='birth', index=['year', 'sex'], columns='name', aggfunc='sum', fill_value=0)

    data = {}
    all_years = list(range(df['year'].min(), df['year'].max() + 1))

    for year in all_years:
        year_data = {'M': 0, 'F': 0, 'T': 0}
        # Check if 'M' exists for this year in the pivot table
        if (year, 'M') in pivot_table_by_name_year_sex.index:
            year_data['M'] = int(pivot_table_by_name_year_sex.loc[(year, 'M')].sum())

        # Check if 'F' exists for this year in the pivot table
        if (year, 'F') in pivot_table_by_name_year_sex.index:
            year_data['F'] = int(pivot_table_by_name_year_sex.loc[(year, 'F')].sum())
        year_data['T'] = year_data['M'] + year_data['F']
        data[year] = year_data

    # Calculate total births by year
    total_births_by_year = pivot_table_by_name_year_sex.groupby('year').sum().sum(axis=1)

    result = {
        "data": data,
        "name": name,
        "total": int(df['birth'].sum()),
        "max_year": int(total_births_by_year.idxmax()),
        "max_value": int(total_births_by_year.max()),
        "by_gender": sex
    }

    return result

