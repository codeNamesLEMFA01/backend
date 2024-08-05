from zipfile import ZipFile
import pandas as pd
from mongoengine import connect
from ..models.yob import Yob

zip_path = "./data/names.zip"
columns = ["name", "sex", "birth"]
yobs = []

def insert_yob_data(mongo_client):
    """
      +  Reads the zip file of all the names from 1880 to 2018
      +  and merges all the dataframes into a single dataframe.
      +  Returns:
      +    names: pandas dataframe of all names from 1880 to 2018.
    """
    with ZipFile(zip_path, "r") as zipObj:
        for year in range(1880, 2019):
            file_name = f"yob{year}.txt"
            with zipObj.open(file_name) as zipFile:
                df = pd.read_csv(zipFile, names=columns)
                df["year"] = year
                yobs.append(df)

    names = pd.concat(yobs, ignore_index=True)

    with mongo_client.start_session() as session:
        for _, row in names.iterrows():
            yob = Yob(
                name=row['name'],
                sex=row['sex'],
                birth=row['birth'],
                year=row['year']
            )
            yob.save(session=session)

    print("Données insérées avec succès dans MongoDB.")

def run_yob_import(db):
    insert_yob_data(db)
