import datetime
from pymongo import MongoClient
from pymodm import MongoModel, fields, connect

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bm590
connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")

class User(MongoModel):
    patient_name   = fields.CharField()
    user_id        = fields.CharField()
    #object_id      = fields.ObjectIdField()
    password       = fields.CharField()
    dimension1     = fields.IntegerField()
    dimension2     = fields.IntegerField()
    classification = fields.BooleanField()

def insert(content):
    content = {"image_data": content,
               "date": datetime.datetime.utcnow()}
    result = db.images.insert_one(content)
    User('Testname','345','password', '1080', '2400','True').save()
    return result.inserted_id

if __name__ == '__main__':
    insert(1234)
