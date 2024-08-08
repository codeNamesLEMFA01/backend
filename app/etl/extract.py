from zipfile import ZipFile
import csv
import time
from ..models.yob import Yob

zip_path = "./data/names.zip"


from zipfile import ZipFile
import pandas as pd

zip_path = "./data/names.zip"
columns = ["name", "sex", "birth"]
yobs = []





def extract():
  with ZipFile(zip_path, "r") as zipObj:
    """
      +  Reads the zip file of all the names from 1880 to 2018
      +  and merges all the dataframes into a single dataframe.
      +  Returns:
      +    names: pandas dataframe of all names from 1880 to 2018.
    """
    for year in range(1880, 2019):
      file_name = f"yob{year}.txt"
      with zipObj.open(file_name) as zipFile:
        df = pd.read_csv(zipFile, names=columns)
        df["year"] = year
        yobs.append(df)
  return pd.concat(yobs, ignore_index=True)

#     start_time = time.time()
#     mongo_client
#     batch_size = 2000
#     batch = []
#     total_records = 0
#
#     with ZipFile(zip_path, "r") as zipObj:
#         for year in range(1880, 2019):
#             file_name = f"yob{year}.txt"
#             with zipObj.open(file_name) as zipFile:
#                 reader = csv.reader(zipFile.read().decode('utf-8').splitlines())
#                 for row in reader:
#                     name, sex, birth = row
#                     yob = Yob(name=name, sex=sex, birth=int(birth), year=year)
#                     batch.append(yob)
#                     total_records += 1
#
#                     if len(batch) >= batch_size:
#                         Yob.objects.insert(batch, load_bulk=False)
#                         print(f"Traité {total_records} enregistrements")
#                         batch = []
#
#     if batch:
#         Yob.objects.insert(batch, load_bulk=False)
#
#     end_time = time.time()
#     print(f"Données insérées avec succès dans MongoDB en {end_time - start_time:.2f} secondes.")
#     print(f"Total des enregistrements traités : {total_records}")
#






def run_yob_import():
    insert_yob_data()