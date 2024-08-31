from mongoengine import Q
from ..models.yob import Yob
from ..models.yobLengthName import YobLengthName
import json
import pandas as pd
from fastapi import HTTPException
import time
import numpy as np


def get_name_length_trends():
    start = time.time()
    print("⏰ Start => ", start)
    yobs = Yob.objects()
    names = pd.DataFrame(json.loads(yobs.to_json()))

    df = pd.DataFrame(names)

    # Calculate the length of names
    df['name_length'] = df['name'].str.len()

    # Create a pivot table summarizing average name lengths by year and gender
    pivot_table = df.pivot_table(index='year', columns='sex', values='name_length', aggfunc='mean')

    # Find the longest names by gender
    max_male = df.loc[df['sex'] == 'M'].sort_values('name_length', ascending=False).iloc[0]
    max_female = df.loc[df['sex'] == 'F'].sort_values('name_length', ascending=False).iloc[0]

    # Calculate evolution percentages
    male_evolution = float((pivot_table['M'].iloc[-1] - pivot_table['M'].iloc[0]) / pivot_table['M'].iloc[0] * 100)
    female_evolution = float((pivot_table['F'].iloc[-1] - pivot_table['F'].iloc[0]) / pivot_table['F'].iloc[0] * 100)
    global_evolution = float((pivot_table.mean(axis=1).iloc[-1] - pivot_table.mean(axis=1).iloc[0]) / pivot_table.mean(axis=1).iloc[0] * 100)

    # Convert numpy types to native Python types
    max_male_dict = max_male.to_dict()
    max_female_dict = max_female.to_dict()

    # Convert dictionary values from numpy to Python native types
    for key in max_male_dict:
        if isinstance(max_male_dict[key], (np.int64, np.float64)):
            max_male_dict[key] = max_male_dict[key].item()

    for key in max_female_dict:
        if isinstance(max_female_dict[key], (np.int64, np.float64)):
            max_female_dict[key] = max_female_dict[key].item()

    # Ensure pivot_table index and values are converted to native types
    male_years = list(map(int, pivot_table.index))
    male_lengths = list(map(float, pivot_table['M'].to_list()))
    female_years = list(map(int, pivot_table.index))
    female_lengths = list(map(float, pivot_table['F'].to_list()))
    global_years = list(map(int, pivot_table.index))
    global_lengths = list(map(float, pivot_table.mean(axis=1).to_list()))

    # Convert describe() statistics to native Python types
    male_describe = {k: float(v) for k, v in pivot_table['M'].describe().to_dict().items()}
    female_describe = {k: float(v) for k, v in pivot_table['F'].describe().to_dict().items()}

    result = {
        'data': {
            'male': {
                'years': male_years,
                'length': male_lengths,
            },
            'female': {
                'years': female_years,
                'length': female_lengths,
            },
            'global': {
                'years': global_years,
                'length': global_lengths,
            }
        },
        'meta': {
            'max': {
                'male': max_male_dict,
                'female': max_female_dict
            },
            'evolution': {
                'male': male_evolution,
                'female': female_evolution,
                'global': global_evolution
            },
            'describe': {
                'male': male_describe,
                'female': female_describe
            }
        }
    }

    end = time.time()
    print("⏰ End => ", end)
    print("⏰ => ", end - start)
    return result


def get_name_length():
    latest_doc = YobLengthName.objects().order_by('-id').first()

    if not latest_doc:
        return None

    return {
        "data": {
            "male": {
                "years": latest_doc.data['male'].years,
                "length": latest_doc.data['male'].length
            },
            "female": {
                "years": latest_doc.data['female'].years,
                "length": latest_doc.data['female'].length
            },
            "global": {
                "years": latest_doc.data['global'].years,
                "length": latest_doc.data['global'].length
            }
        },
        "meta": {
            "max": {
                "male": latest_doc.meta_data.max['male'].to_mongo().to_dict(),
                "female": latest_doc.meta_data.max['female'].to_mongo().to_dict()
            },
            "evolution": {
                "male": latest_doc.meta_data.evolution.male,
                "female": latest_doc.meta_data.evolution.female,
                "global": latest_doc.meta_data.evolution.global_
            },
            "describe": {
                "male": latest_doc.meta_data.describe['male'].to_mongo().to_dict(),
                "female": latest_doc.meta_data.describe['female'].to_mongo().to_dict()
            }
        }
    }