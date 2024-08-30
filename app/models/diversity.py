from mongoengine import Document, IntField, FloatField


class Diversity(Document):
    year = IntField(required=True)
    F = FloatField(required=True)
    M = FloatField(required=True)
    total = FloatField(required=True)
    total_name = IntField(required=True)

    meta = {
        "collection": "diversity",
        "indexes": [
            {"fields": ["year", "F", "M", "total", "total_name"], "unique": True}
        ],
    }

    def to_dict(self):
        return {
            "M": self.M,
            "F": self.F,
            "total": self.total,
            "year": self.year,
            "total_name": self.total_name,
        }
