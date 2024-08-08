from .transform import transform
from ..models.yob import Yob
from json import loads
from mongoengine.context_managers import switch_db
import logging
import time


def load():
    start_time = time.time()
    df = transform()
    json_data = df.to_json(orient="records")
    data = loads(json_data)

    batch_size = 10000
    total_items = len(data)

    for i in range(0, total_items, batch_size):
        batch = data[i : i + batch_size]
        yob_instances = [Yob(**item) for item in batch]

        try:
            with switch_db(Yob, "default"):
                Yob.objects.insert(yob_instances, load_bulk=False)
        except Exception as e:
            logging.error(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
    end_time = time.time()
    logging.info(f"Data loading completed. {end_time - start_time:.2f}")
