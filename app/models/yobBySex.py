from mongoengine import Document, StringField, IntField

class YobsBySex(Document):
    M = IntField(required=True)
    F = IntField(required=True)
    total = IntField(required=True)
    year = IntField(required=True)
    meta = {'collection': 'yobsBySex'}

    def to_dict(self):
        return {
            'M': self.M,
            'F': self.F,
            'total': self.total,
            'year': self.year
            }