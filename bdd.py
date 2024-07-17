from pymongo import MongoClient
"""On crée la base de données MangoDB"""
def get_database():
    client = MongoClient('localhost:27017')
    return client['scrapping_stackoverflow']