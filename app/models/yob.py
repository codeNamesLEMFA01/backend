from mongoengine import Document, StringField, IntField

class Yob(Document):
    name = StringField(required=True)
    sex = StringField(required=True, choices=['M', 'F'])
    birth = IntField(required=True)
    year = IntField(required=True)


    meta = {
        'collection': 'yobs',
        'indexes': [
            {'fields': ['name', 'sex', 'year'], 'unique': True}
        ]
    }