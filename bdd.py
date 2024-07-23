import os
from pymongo import MongoClient
import mongomock

def get_database():
    if os.getenv('TESTING') == 'true':
        # Use mongomock if in testing mode
        return mongomock.MongoClient().db
    else:
        # Use real MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        return client['mydatabase']