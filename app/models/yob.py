from mongoengine import Document, StringField, IntField, FloatField


class Yob(Document):
    name = StringField(required=True)
    sex = StringField(required=True, choices=["M", "F"])
    birth = IntField(required=True)
    year = IntField(required=True)
    ratio = FloatField(required=True)

    meta = {
        "collection": "yobs",
        "indexes": [{"fields": ["name", "sex", "year", "ratio"], "unique": True}],
    }
