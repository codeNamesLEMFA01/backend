from pydantic import BaseModel
from mongoengine import Document, StringField, BooleanField, UUIDField
import uuid

class User(Document):
    uuid= UUIDField(binary=False, required=True, default=uuid.uuid4, unique=True)
    username= StringField(required=True)
    email= StringField(required=False)
    full_name= StringField(required=False)
    disabled= BooleanField(default=False)
    hashed_password= StringField(required=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        return super(User, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "disabled": self.disabled,
            "hashed_password": self.hashed_password
        }

    meta = {
        "collection": "users",
        "allow_inheritance": True,
        "indexes": [{"fields": ["username", "email", "full_name"],"unique": True }]
    }