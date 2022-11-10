from mongoengine import (
    StringField,
    IntField,
    DateTimeField,
    EmbeddedDocument,
    URLField
)

class NyaaTorrent(EmbeddedDocument):
    # основные атрибуты торрента
    id       = IntField(primary_key=True)
    quality  = StringField(max_length=10)
    url      = URLField()
    file_url = URLField()
    magnet   = StringField()
    size     = StringField()

    # доп атрибуты, мб понадобятся где-нибудь
    title     = StringField()
    type      = StringField()
    category  = StringField()
    seeders   = IntField()
    leechers  = IntField()
    downloads = IntField()
    date      = DateTimeField()