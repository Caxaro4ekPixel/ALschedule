from mongoengine import (
    Document,
    StringField,
    IntField,
    DateTimeField
)


class File(Document):
    user_id       = IntField()
    user_fullname = StringField()
    file_type     = StringField()
    file_size     = StringField()
    file_name     = StringField()
    sent_date     = DateTimeField()