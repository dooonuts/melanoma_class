#from pymodm import connect
#from pymodm import MongoModel, fields
import datetime
from pymongo import MongoClient
from pymodm  import MongoModel, fields

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bme590

class User(MongoModel):
	patient_name = fields.CharField()
	user_id      = fields.CharField()
	object_id    = fields.ObjectIdField()
	password     = fields.CharField()
	

def insert(content):
	# db = connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")
	# print(db)
	print("connected to mongodb")
	content = {"image_data": content,
		   "date": datetime.datetime.utcnow()}  
	result = db.images.insert_one(content)
	print(result.inserted_id)
	return result.inserted_id
	
if __name__ == '__main__':
     insert(1234)

