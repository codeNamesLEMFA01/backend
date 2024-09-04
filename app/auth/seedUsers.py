from ..models.users import User

def seedUsers():
    seed_users_db = [
        {
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
        {
            "email": "alice@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
        {
            "email": "bob@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            # password is "secret"
            "disabled": False,
        },
    ]

    for user in seed_users_db:
        try :
            if not User.objects(email=user['email']):
                User.objects.create(**user)
                return "User seeded"
        except:
            print("Error inserting users to db")