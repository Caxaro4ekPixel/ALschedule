from mongoengine import (
    Document,
    StringField,
    BooleanField,
    IntField,
    ReferenceField,
    ListField
)
from .episode import Episode

class Release(Document):
    _id        = IntField(primary_key=True)
    chat_id    = IntField()
    ru_title   = StringField()
    en_title   = StringField()
    code       = StringField()
    total_ep   = IntField(min_value=0, max_value=1000)
    is_ongoing = BooleanField(default=True)
    is_top     = BooleanField(default=False)
    episode    = ListField(ReferenceField(Episode))