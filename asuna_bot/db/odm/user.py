from mongoengine import (
    Document,
    StringField,
    IntField
)


class User(Document):
    _id       = IntField(primary_key=True)
    full_name = StringField(max_length=100)
    user_name = StringField(max_length=100)