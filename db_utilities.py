from pymongo import MongoClient
from pymongo.errors import BulkWriteError

DB_CONNECTION_STRING = 'mongodb+srv://admin123:admin123@cluster0.y16pf.mongodb.net/finalproject?retryWrites=true&w=majority'

class DbUtiltity:

    def __init__(self):
        self.client = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def connect_to_db(self):
        if not self.client:
            self.client = MongoClient(DB_CONNECTION_STRING)
    
    def drop_cars_collection(self):
        db = self.client.finalproject
        db.cars.drop()
    
    def find_all_cars(self, criteria):
        if not self.client:
            self.connect_to_db()
        db = self.client.finalproject
        return db.cars.find(criteria)
    
    def find_one_car(self, criteria):
        if not self.client:
            self.connect_to_db()
        db = self.client.finalproject
        return db.cars.find_one(criteria)

    def save_cars_to_db(self, cars):
        if not self.client:
            self.connect_to_db()
        db = self.client.finalproject

        if cars and len(cars) > 0:
            try:
                db.cars.insert_many(documents=cars, ordered=False)
            except BulkWriteError as e:
                print(type(e))
    
    def close_connection(self):
        if self.client:
            self.client.close()