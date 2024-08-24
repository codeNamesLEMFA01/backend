import pandas as pd
from ..extract.all_names import names as df
import json

def get_name_length_trends():
    # Calculate the length of names
    df['name_length'] = df['name'].str.len()

    # creates a pivot table summarizing average name lengths by year and gender
    pivot_table = df.pivot_table(index='year', columns='sex', values='name_length', aggfunc='mean')

    # Find the longest names by gender
    max_male = df.loc[df['sex'] == 'M'].sort_values('name_length', ascending=False).iloc[0]
    max_female = df.loc[df['sex'] == 'F'].sort_values('name_length', ascending=False).iloc[0]

    male_evolution = (pivot_table['M'].iloc[-1] - pivot_table['M'].iloc[0]) / pivot_table['M'].iloc[0] * 100
    female_evolution = (pivot_table['F'].iloc[-1] - pivot_table['F'].iloc[0]) / pivot_table['F'].iloc[0] * 100
    global_evolution = (pivot_table.mean(axis=1).iloc[-1] - pivot_table.mean(axis=1).iloc[0]) / pivot_table.mean(axis=1).iloc[0] * 100


    result = {
        'data': {
            'male': {
                'years': pivot_table.index.to_list(),
                'length': pivot_table['M'].to_list(),
                # 'change': male_change.to_list()
            },
            'female': {
                'years': pivot_table.index.to_list(),
                'length': pivot_table['F'].to_list(),
                # 'change': female_change.to_list()
            },
            'global': {
                'years': pivot_table.index.to_list(),
                'length': pivot_table.mean(axis=1).to_list(),
                # 'change': global_change.to_list()
            }
        },
        'meta': {
            'max': {
                'male': max_male.to_dict(),
                'female': max_female.to_dict()
            },
            'evolution': {
                'male': male_evolution,
                'female': female_evolution,
                'global': global_evolution
            },
            'describe': {
                'male': pivot_table['M'].describe().to_dict(),
                'female': pivot_table['F'].describe().to_dict()
            }
        }
    }

    return result