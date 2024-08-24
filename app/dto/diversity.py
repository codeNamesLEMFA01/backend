import pandas as pd
import numpy as np
from ..extract.all_names import names

def quantification_diversity(start_year=2000, end_year=2010):
    # Filtrer les données par intervalle de dates
    filtered_df = names[(names['year'] >= start_year) & (names['year'] <= end_year)]

    # Compter le nombre de prénoms différents pour chaque sexe
    male_diversity = filtered_df[filtered_df['sex'] == 'M']['name'].nunique()
    female_diversity = filtered_df[filtered_df['sex'] == 'F']['name'].nunique()

    result = {
        "start_year": start_year,
        "end_year": end_year,
        "diversity": {
            "male": male_diversity,
            "female": female_diversity,
            "total": male_diversity + female_diversity
        }
    }

    return result

def quantification_diversity_all_years():
    diversity_by_year = {}

    for year in names['year'].unique():
        # Filtrer les données pour une année spécifique
        filtered_df = names[names['year'] == year]

        # Compter le nombre de prénoms différents pour chaque sexe
        male_diversity = filtered_df[filtered_df['sex'] == 'M']['name'].nunique()
        female_diversity = filtered_df[filtered_df['sex'] == 'F']['name'].nunique()

        # Ajouter les résultats au dictionnaire
        diversity_by_year[int(year)] = {
            "male": int(male_diversity),
            "female": int(female_diversity),
            "total": int(male_diversity) + int(female_diversity)
        }

    return diversity_by_year


unique_names_per_year = names.groupby('year')['name'].nunique()

def shannon_diversity(x):
    proportions = x / x.sum()
    return -np.sum(proportions * np.log(proportions))

diversity_index = names.groupby('year').apply(lambda x: shannon_diversity(x['birth']))

# Proportion des top 10 prénoms par année
def top_10_proportion(group):
    total = group['birth'].sum()
    top_10 = group.nlargest(10, 'birth')['birth'].sum()
    return top_10 / total

top_10_prop = names.groupby('year').apply(top_10_proportion)


resultDiversity = {
  "unique": unique_names_per_year.to_dict(),
  "index": diversity_index.to_dict(),
}
