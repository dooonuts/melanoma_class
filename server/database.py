import datetime
from pymongo import MongoClient
from pymodm import MongoModel, fields

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bm590

class User(MongoModel):
    patient_name   = fields.CharField()
    user_id        = fields.CharField()
    object_id      = fields.ObjectIdField()
    password       = fields.CharField()
    dimensions     = fields.IntegerField()
    classification = fields.BooleanField()

def insert(content):
    content = {"image_data": content,
               "date": datetime.datetime.utcnow()}
    results = database.images.insert_one(content)
    return result.inserted_id

if __name__ == '__main__':
    insert(1234)
