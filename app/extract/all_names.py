from zipfile import ZipFile
import pandas as pd

zip_path = "./data/names.zip"
columns = ["name", "sex", "birth"]
yobs = []

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

names = pd.concat(yobs, ignore_index=True)