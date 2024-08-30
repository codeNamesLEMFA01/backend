from mongoengine import Document, EmbeddedDocument, ListField, IntField, FloatField, ObjectIdField, StringField, DictField, EmbeddedDocumentField

class DataSection(EmbeddedDocument):
    years = ListField(IntField(), required=True)
    length = ListField(FloatField(), required=True)

class MetaMax(EmbeddedDocument):
    name = StringField(required=True)
    sex = StringField(required=True, choices=["M", "F"])
    birth = IntField(required=True)
    year = IntField(required=True)
    ratio = FloatField(required=True)
    name_length = IntField(required=True)

class MetaEvolution(EmbeddedDocument):
    male = FloatField(required=True)
    female = FloatField(required=True)
    global_ = FloatField(required=True)

class MetaDescribe(EmbeddedDocument):
    count = FloatField(required=True)
    mean = FloatField(required=True)
    std = FloatField(required=True)
    min = FloatField(required=True)
    q25 = FloatField(db_field='25%', required=True)
    q50 = FloatField(db_field='50%', required=True)
    q75 = FloatField(db_field='75%', required=True)
    max = FloatField(required=True)

class MetaSection(EmbeddedDocument):
    max = DictField(EmbeddedDocumentField(MetaMax), required=True)
    evolution = DictField(EmbeddedDocumentField(MetaEvolution), required=True)
    describe = DictField(EmbeddedDocumentField(MetaDescribe), required=True)

class YobLengthName(Document):
    data = DictField(EmbeddedDocumentField(DataSection), required=True)
    meta_data = EmbeddedDocumentField(MetaSection, required=True)

    meta = {'collection': 'yobLengthName'}