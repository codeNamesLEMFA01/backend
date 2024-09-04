from mongoengine import Document, StringField


class TokenData(Document):
    email= StringField(required=True)