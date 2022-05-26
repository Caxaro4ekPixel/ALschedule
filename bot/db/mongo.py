import logging
from pymongo import MongoClient

from config import MONGO_HOST

client = MongoClient(MONGO_HOST)
db = client.al_schedule


def check_user(user_id):
    if db.users.find_one({"_id": user_id}):
        return True
    return False


def add_new_user(user_id, user_name, full_name):
    if not check_user(user_id):
        if user_name is None:
            user_name = ""

        try:
            db.users.insert_one({
                "_id": user_id, 
                "user_name": user_name,
                "full_name": full_name
            })
            return True

        except Exception as e:
            logging.error(e)
            return False
    else:
        return False


def add_user_to_whitelist(user_id, user_name, full_name):
    try:
        db.whitelist.insert_one({
            "_id": user_id, 
            "user_name": user_name,
            "full_name": full_name
        })
        return True

    except Exception as e:
        logging.error(e)
        return False


def get_user(user_id):
    return db.users.find_one({"_id": user_id})
