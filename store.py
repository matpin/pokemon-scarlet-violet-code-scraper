from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

uri = os.environ.get('MONGO_URI')
client = MongoClient(uri)
codes_db = client.codes
collection = codes_db.codes


def add_codes(codes):
    if len(codes) != 0:
        collection.insert_many(codes)
    else:
        print("No new codes")


def find_code(criteria):
    return collection.find_one(criteria)
