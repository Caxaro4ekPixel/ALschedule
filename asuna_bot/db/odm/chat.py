from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    BooleanField,
    IntField,
    ReferenceField,
    ListField
)
from .release import Release


class ChatConfig(EmbeddedDocument):
    submitter            = StringField(default="[SubsPlease]")
    deadline_alert       = BooleanField(default=True)
    direct_links         = BooleanField(default=True)
    torrent_files        = BooleanField(default=True)
    show_hd              = BooleanField(default=False)
    ete_num              = BooleanField(default=False)
    magnet_links         = BooleanField(default=True)


class MongoChat(Document):
    _id     = IntField(primary_key=True)
    name    = StringField(max_length=100)
    config  = EmbeddedDocumentField(ChatConfig, default=ChatConfig)
    release = ReferenceField(Release)