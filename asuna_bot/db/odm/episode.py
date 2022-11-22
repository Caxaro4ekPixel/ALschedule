from mongoengine import (
    Document,
    StringField,
    BooleanField,
    IntField,
    ListField,
    DateTimeField,
    EmbeddedDocumentField,
    EmbeddedDocument
)
from .torrent import MongoTorrent

class Episode(EmbeddedDocument):
    submitter       = StringField()
    title           = StringField()
    number          = IntField(min_value=0, max_value=1000)
    released_at     = DateTimeField()
    deadline_at     = DateTimeField()
    in_progress     = BooleanField()
    uploaded_at     = DateTimeField()
    minutes_work_on = IntField()
    torrents        = ListField(EmbeddedDocumentField(MongoTorrent))