from platform import release
from pymongo import MongoClient

from data.config import MONGO_HOST, MONGO_DB_NAME

client = MongoClient(MONGO_HOST)
db = client[MONGO_DB_NAME]



