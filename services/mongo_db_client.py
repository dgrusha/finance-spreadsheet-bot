from pymongo import MongoClient
from config import Config


class MongoDB:
    def __init__(
        self, uri: str = Config.MONGO_DB_URI, db_name: str = Config.MONGO_DB_NAME
    ):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find_documents(self, collection_name, query={}):
        collection = self.get_collection(collection_name)
        return collection.find(query)

    def find_one_document(self, collection_name, query={}):
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def update_document(self, collection_name, query, update_values):
        collection = self.get_collection(collection_name)
        return collection.update_one(query, {"$set": update_values})

    def close_connection(self):
        self.client.close()


mongo_db = MongoDB()
