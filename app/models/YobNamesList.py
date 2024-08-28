from mongoengine import Document, StringField

class YobNamesList(Document):
  name = StringField(required=True)
  meta = {'collection': 'yobNamesList',
          'indexes': [
            {'fields': ['name'], 'unique': True}
        ]}

  def to_list(self):
    return self