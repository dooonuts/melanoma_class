import datetime
import string
import random
from pymongo import MongoClient
from pymodm import MongoModel, fields, connect

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bm590
connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")

class User(MongoModel):
    patient_name   = fields.CharField()
    user_id        = fields.CharField()
    password       = fields.CharField()
    dimension1     = fields.IntegerField()
    dimension2     = fields.IntegerField()
    classification = fields.FloatField()
    image_content  = fields.CharField()
    unique_id      = fields.IntegerField()

def insert(content, patient_name, user_id, password, dimension1, dimension2, prob):
    unique_id = ''.join(random.choice(string.digits) for _ in range(12))
    user = User(patient_name, user_id, password, dimension1, dimension2, prob, \
         content, unique_id)
    user.save()
    return user.unique_id 

def change_params(name, param, value):
    user = User.objects.get({'patient_name':name})
    if param == 'image content':
        user.image_content = value
        user.save()
    elif param == 'patient name':
        user.patient_name = value
        user.save()
    elif param == 'user id':
        user.user_id = value
        user.save()
    elif param == 'password':
        user.password = value
        user.save()
    elif param == 'dimension1':
        if value.type() != int:
            raise ValueError('Can only enter integers')
        user.dimension1 = value
        user.save()
    elif param == 'dimension2':
        if value.type() != int:
            raise ValueError('Can only enter integers')
        user.dimension2 = value
        user.save()


#if __name__ == '__main__':
#    insert(12345, 'Daniel Wu', 'dwu', 'ilikebunnies', '1200', '1080', '0.95')
#    change_params('Daniel Wu', 'user id', 'dwu<3')
