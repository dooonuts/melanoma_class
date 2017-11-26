from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")
print("connected to mongodb")
