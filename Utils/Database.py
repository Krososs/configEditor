from pymongo import MongoClient
from Utils.Constants import Constants

client = MongoClient('localhost', 27017)


class Database:

    def __int__(self):
        self.categories = []

    @staticmethod
    def database_exist():
        return Constants.DB_NAME in client.list_database_names()

    @staticmethod
    def create_databse(data):
        db = client.ConfigEditor
        categories = db.categories
        for category in data:
            categories.insert_one(category)

    @staticmethod
    def get_categories():
        db = client.ConfigEditor
        categories = db.categories
        return categories
