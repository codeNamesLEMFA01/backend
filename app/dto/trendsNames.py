import json
import pandas as pd
from ..extract.all_names import names
import numpy as np

pivot_table_by_name_year = pd.pivot_table(names, values='birth', index='year', columns='name', aggfunc='sum', fill_value=0)
# pivot_table_by_name_year['total'] = pivot_table_by_name_year.sum(axis=1)
pivot_table_by_name_year_sex = pd.pivot_table(names, values='birth', index=['year', 'sex'], columns='name', aggfunc='sum', fill_value=0)

all_years = list(range(names['year'].min(), names['year'].max() + 1))

def get_name_trend(name):
    if name in pivot_table_by_name_year.columns:
        trend = pivot_table_by_name_year[name]
        return trend.to_dict()
    else:
        return {"error": "Name not found in the data"}

def trends_name(name):
    name = name.strip().capitalize()
    trend = get_name_trend(name)

    if "error" in trend:
        print(trend["error"])
    else:
      trend_series = pivot_table_by_name_year[name]
      sex = names[names['name'] == name].groupby('sex')['birth'].sum().to_dict()

    data = {}
    all_years = list(range(names['year'].min(), names['year'].max() + 1))
    for year in all_years:
        year_data = {'M': 0, 'F': 0, 'T': 0}
        if year in pivot_table_by_name_year_sex.index.get_level_values('year'):
            year_data['M'] = int(pivot_table_by_name_year_sex.loc[(year, 'M'), name])
            year_data['F'] = int(pivot_table_by_name_year_sex.loc[(year, 'F'), name])
            year_data['T'] = year_data['M'] + year_data['F']
        data[year] = year_data

    result = {
        "data": data,
        "name": name,
        "total": int(trend_series.sum()),
        "max_year": int(trend_series.idxmax()),
        "max_value": int(trend_series.max()),
        "by_gender": sex
    }

    return result



# def get_name_diversity():
#     data = {
#         "male": [],
#         "female": [],
#     }

#     # Remplir les données pour les prénoms masculins
#     # if 'M' in pivot_table_by_name_year_sex.index.get_level_values('sex'):
#     male_names = pivot_table_by_name_year_sex.xs('M', level='sex')
#     for name in male_names.columns:
#         birth_counts = [int(male_names.loc[year, name]) if year in male_names.index else 0 for year in all_years]
#         data["male"].append({"name": name, "year": all_years, "birth": birth_counts})

#     # Remplir les données pour les prénoms féminins
#     # if 'F' in pivot_table_by_name_year_sex.index.get_level_values('sex'):
#     female_names = pivot_table_by_name_year_sex.xs('F', level='sex')
#     for name in female_names.columns:
#         birth_counts = [int(female_names.loc[year, name]) if year in female_names.index else 0 for year in all_years]
#         data["female"].append({"name": name, "year": all_years, "birth": birth_counts})

#     return data

# def get_name_diversity():
#     data = {
#         "male": [
#           {
#             name: "eric",
#             years: [1880,1881,...],
#             birth: [0,50,...]
#           }
#           ],
#         "female": [],
#     }

#     # Initialisation des DataFrames pour les noms masculins et féminins
#     male_names = pivot_table_by_name_year_sex.xs('M', level='sex', drop_level=False).reindex(all_years, fill_value=0).reset_index(level='sex', drop=True)
#     female_names = pivot_table_by_name_year_sex.xs('F', level='sex', drop_level=False).reindex(all_years, fill_value=0).reset_index(level='sex', drop=True)

#     # Remplir les données pour les prénoms masculins
#     for name in male_names.columns:
#         birth_counts = male_names[name].tolist()
#         data["male"].append({"name": name, "year": all_years, "birth": birth_counts})

#     # Remplir les données pour les prénoms féminins
#     for name in female_names.columns:
#         birth_counts = female_names[name].tolist()
#         data["female"].append({"name": name, "year": all_years, "birth": birth_counts})

#     return data
pivot_table = names.pivot_table(index=['sex', 'name'], columns='year', values='birth', aggfunc='sum', fill_value=0)
pivot_table = pivot_table.reset_index()

# 1. Créer des tables de pivot séparées pour chaque sexe
pivot_male = names[names['sex'] == 'M'].pivot_table(index='name', columns='year', values='birth', aggfunc='sum', fill_value=0)
pivot_female = names[names['sex'] == 'F'].pivot_table(index='name', columns='year', values='birth', aggfunc='sum', fill_value=0)

# 2. Réinitialiser les index pour faciliter la transformation en dictionnaire
pivot_male = pivot_male.reset_index()
pivot_female = pivot_female.reset_index()

def pivot_to_dict(pivot_df):
    return pivot_df.apply(lambda row: {
        'name': row['name'],
        'years': [int(year) for year in pivot_df.columns[1:] if row[year] > 0],  # Les années où il y a des naissances
        'birth': [int(row[year]) for year in pivot_df.columns[1:] if row[year] > 0]
    }, axis=1).tolist()

# 4. Créer la structure de données finale
# def get_name_diversity():

#   data = {
#       'male': pivot_to_dict(pivot_male),
#       'female': pivot_to_dict(pivot_female)
#   }
#   return data

def diversity_index_simpson(df):
    total_count = df['birth'].sum()
    name_counts = df.groupby('name')['birth'].sum()
    proportions = name_counts / total_count
    return 1 - (proportions**2).sum()

# 2. Calculer l'Indice de Shannon
def diversity_index_shannon(df):
    total_count = df['birth'].sum()
    name_counts = df.groupby('name')['birth'].sum()
    proportions = name_counts / total_count
    return - (proportions * np.log(proportions)).sum()

# 3. Calculer le Nombre de Prénoms Uniques
def unique_name_count(df):
    return df['name'].nunique()

# Calculer les indices pour chaque année
annual_diversity = names.groupby('year').apply(lambda x: {
    'simpson': diversity_index_simpson(x),
    'shannon': diversity_index_shannon(x),
    'unique_names': unique_name_count(x)
})

# Convertir en DataFrame pour faciliter l'export
annual_diversity_df = pd.DataFrame(annual_diversity.tolist(), index=annual_diversity.index)
annual_diversity_df.reset_index(inplace=True)

# 2. Préparer les fréquences des prénoms pour une année spécifique (par exemple, 2020)
frequencies_2020 = names[names['year'] == 2018].groupby('name')['birth'].sum()
frequencies_2020 = frequencies_2020.sort_values(ascending=False)

# 3. Préparer les données pour les graphiques en barres des prénoms les plus courants
top_names_2020 = frequencies_2020.head(10)
top_names_data = {
    'names': top_names_2020.index.tolist(),
    'values': top_names_2020.values.tolist()
}

def get_name_diversity():
  # annual_diversity = annual_diversity_df.to_dict()
  # frequencies_2020 = frequencies_2020.to_dict()
  return top_names_data
# Sauvegarder les données pour l'export
# annual_diversity_df.to_csv('annual_diversity.csv', index=False)
# frequencies_2020.to_csv('frequencies_2020.csv', header=True)
# pd.DataFrame(top_names_data).to_csv('top_names_2020.csv', index=False)

# def get_top_names_between_years(start_year= 1880, end_year= 1900, sex= 'M', top_n=10):
#     # Filtrer les données par sexe et par intervalle de dates
#     filtered_df = names[(names['sex'] == sex) & (names['year'] >= start_year) & (names['year'] <= end_year)]

#     # Grouper par prénom et sommer les naissances
#     name_counts = filtered_df.groupby('name')['birth'].sum()

#     # Trier les prénoms par nombre de naissances et sélectionner les top_n
#     top_names = name_counts.nlargest(top_n)

#     # Préparer les données pour l'export ou l'affichage
#     top_names_data = {
#         'names': top_names.index.tolist(),
#         'values': top_names.values.tolist()
#     }

#     return top_names_data

# def get_top_names_between_years(start_year= 1880, end_year= 1900, sex= 'M', top_n=10):
#     # Filtrer les données par sexe et par intervalle de dates
#     filtered_df = names[(names['sex'] == sex) & (names['year'] >= start_year) & (names['year'] <= end_year)]

#     # Grouper par prénom et sommer les naissances pour obtenir le top_n
#     name_counts = filtered_df.groupby('name')['birth'].sum()
#     top_names = name_counts.nlargest(top_n).index.tolist()

#     # Préparer les données pour chaque prénom
#     data = []
#     for name in top_names:
#         name_data = filtered_df[filtered_df['name'] == name]
#         yearly_births = name_data.groupby('year')['birth'].sum().reindex(range(start_year, end_year + 1), fill_value=0)
#         data.append({
#             "name": name,
#             "years": yearly_births.index.tolist(),
#             "birth": yearly_births.values.tolist()
#         })

#     return data

def get_top_names_between_years(start_year, end_year, top_n):
    def top_names_by_sex(sex):
        # Filtrer les données par sexe et par intervalle de dates
        filtered_df = names[(names['sex'] == sex) & (names['year'] >= start_year) & (names['year'] <= end_year)]

        # Grouper par prénom et sommer les naissances pour obtenir le top_n
        name_counts = filtered_df.groupby('name')['birth'].sum()
        top_names = name_counts.nlargest(top_n).index.tolist()

        # Préparer les données pour chaque prénom
        data = []
        for name in top_names:
            name_data = filtered_df[filtered_df['name'] == name]
            yearly_births = name_data.groupby('year')['birth'].sum().reindex(range(start_year, end_year + 1), fill_value=0)
            data.append({
                "name": name,
                "years": yearly_births.index.tolist(),
                "birth": yearly_births.values.tolist()
            })

        # Obtenir le prénom le plus courant
        top_name = name_counts.nlargest(1).index[0]
        top_name_total = name_counts.nlargest(1).values[0]

        return data, top_name, top_name_total

    male_data, top_male_name, top_male_total = top_names_by_sex('M')
    female_data, top_female_name, top_female_total = top_names_by_sex('F')

    result = {
        "data": {
            "male": male_data,
            "female": female_data
        },
        "info": {
            "start_year": start_year,
            "end_year": end_year,
            "top_n": top_n,
            "top_name": {
                "male": {
                    "name": top_male_name,
                    "total": int(top_male_total)
                },
                "female": {
                    "name": top_female_name,
                    "total": int(top_female_total)
                }
            }
        }
    }

    return result

# result = {
#   "data" : {
#     "male":[
#       {
#         "name": "John",
#         "years": [1880, 1881, 1882,...],
#         "birth": [1, 2, 3,...]
#       },
#     ],
#     "female":[
#       {
#         "name": "Jane",
#         "years": [1880, 1881, 1882,...],
#         "birth": [1, 2, 3,...]
#       }
#     ]
#   },
#   "info":{
#     "start_year": 1880,
#     "end_year": 1900,
#     "top_n": 10 ,
#     "top_name":{
#       "male":{
#         "name": "John",
#         "total": 100,
#       },
#       "female":{
#         "name": "Jane",
#         "total": 100
#       }
#     }
#   }
# }