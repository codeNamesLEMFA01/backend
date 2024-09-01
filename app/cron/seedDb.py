from ..etl.load import load
import os


def seedDb():
    try:
        if os.getenv("SEEDER") == "True":
            print("Starting seedDb")
            result = load()
            print("seedDb completed successfully")
            return result
        else:
            print("SEEDER environment variable is not set to True. Skipping seedDb.")
            return False
    except Exception as e:
        print(f"Error in seedDb: {e}")
        return False
