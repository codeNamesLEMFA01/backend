from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, IntField, DictField

# Define the embedded document
class GenderCount(EmbeddedDocument):
    F = IntField(required=True)
    M = IntField(required=True)
    total = IntField(required=True)

class YobsBySex(Document):
    year = StringField(required=True, unique=True)
    data = DictField(EmbeddedDocumentField(GenderCount))
    meta = {'collection': 'yobsBySex'}