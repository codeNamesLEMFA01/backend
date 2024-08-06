import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

MONGO_ROOT_USER = os.environ.get("MONGO_ROOT_USER")
MONGO_ROOT_PASSWORD = os.environ.get("MONGO_ROOT_PASSWORD")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")

# Construire l'URL de connexion MongoDB
MONGO_URL = f"mongodb://{MONGO_ROOT_USER}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE_NAME}?authSource=admin"

# Établir la connexion à MongoDB avec MongoEngine
db = connect(host=MONGO_URL)
