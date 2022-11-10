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
    medium_quality       = BooleanField(default=False)
    lowest_quality       = BooleanField(default=True)
    end_to_end_numbering = BooleanField(default=False)
    magnet               = BooleanField(default=True)


class Chat(Document):
    _id     = IntField(primary_key=True)
    name    = StringField(max_length=100)
    config  = EmbeddedDocumentField(ChatConfig, default=ChatConfig)
    release = ListField(ReferenceField(Release))