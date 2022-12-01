from pymongo import MongoClient

client = MongoClient('localhost', 27017)

class Database:
    DB_NAME = 'ConfigEditor'

    def __int__(self):
        self.categoies = []

    @staticmethod
    def database_exist():
        return Database.DB_NAME in client.list_database_names()

    @staticmethod
    def create_databse(data):
        db = client.ConfigEditor
        categories = db.categories
        for category in data:
            categories.insert_one(category)

    @staticmethod
    def get_cagetogries():
        db = client.ConfigEditor
        categories = db.categories
        return categories

