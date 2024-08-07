from zipfile import ZipFile
import csv
import time
from ..models.yob import Yob

zip_path = "./data/names.zip"
def insert_yob_data(mongo_client):
    start_time = time.time()
    mongo_client
    batch_size = 2000
    batch = []
    total_records = 0

    with ZipFile(zip_path, "r") as zipObj:
        for year in range(1880, 2019):
            file_name = f"yob{year}.txt"
            with zipObj.open(file_name) as zipFile:
                reader = csv.reader(zipFile.read().decode('utf-8').splitlines())
                for row in reader:
                    name, sex, birth = row
                    yob = Yob(name=name, sex=sex, birth=int(birth), year=year)
                    batch.append(yob)
                    total_records += 1

                    if len(batch) >= batch_size:
                        Yob.objects.insert(batch, load_bulk=False)
                        print(f"Traité {total_records} enregistrements")
                        batch = []

    if batch:
        Yob.objects.insert(batch, load_bulk=False)

    end_time = time.time()
    print(f"Données insérées avec succès dans MongoDB en {end_time - start_time:.2f} secondes.")
    print(f"Total des enregistrements traités : {total_records}")


def run_yob_import(db):
    insert_yob_data(db)