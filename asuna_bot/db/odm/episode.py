from mongoengine import (
    Document,
    StringField,
    BooleanField,
    IntField,
    ListField,
    DateTimeField,
    EmbeddedDocumentField
)
from .torrent import NyaaTorrent

class Episode(Document):
    submitter       = StringField()
    title           = StringField()
    episode_number  = IntField(min_value=0, max_value=1000)
    release_date    = DateTimeField()
    deadline_date   = DateTimeField()
    in_progress     = BooleanField()
    uploaded_date   = DateTimeField()
    minutes_work_on = IntField()
    torrent         = ListField(EmbeddedDocumentField(NyaaTorrent))