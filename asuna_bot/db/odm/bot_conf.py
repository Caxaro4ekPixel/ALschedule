from mongoengine import (
    Document,
    StringField,
    IntField
)


class BotConfig(Document):
    rss_interval = IntField(default=180)
    rss_last_id  = IntField()
    timezone     = StringField()

