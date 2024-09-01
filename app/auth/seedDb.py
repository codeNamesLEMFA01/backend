from mongoengine.context_managers import switch_db
import logging
from ..models.users import User

def seed_users_db():
    seed_users_db = [
        {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
        {
            "username": "alice",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
        {
            "username": "bob",
            "full_name": "Bob Belcher",
            "email": "bob@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
    ]

    batch_size = 3
    total_items = len(seed_users_db)

    for i in range(0, total_items, batch_size):
        batch = seed_users_db[i : i + batch_size]
        users_instances = [User(**item) for item in batch]
        try:
            with switch_db(User, "default"):
                User.objects.insert(users_instances, load_bulk=False)
        except Exception as e:
            logging.error(f"Error inserting users to db: {str(e)}")