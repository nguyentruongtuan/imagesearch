import pymongo
import os

CLIENT = pymongo.MongoClient(
    os.environ["DB_URL"])
DB = CLIENT["searchimage"]
