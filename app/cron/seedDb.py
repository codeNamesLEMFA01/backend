from ..etl.load import load


def seedDb():
    try:
        print("Starting seedDb")
        result = load()
        print("seedDb completed successfully")
        return result
    except Exception as e:
        print(f"Error in seedDb: {e}")
        return False
