import os
from pymongo import mongo_client
from dotenv import load_dotenv


def get_mongoclient():
    return mongo_client.MongoClient(os.getenv('mongo_connection_string'))
