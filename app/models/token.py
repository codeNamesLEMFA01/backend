from pydantic import BaseModel
from mongoengine import Document, StringField

class Token(Document):
    access_token= StringField(required=True)
    token_type= StringField(required=True)


class TokenData(Document):
    email= StringField(required=True)