import datetime
import string
import random
from pymongo import MongoClient
from pymodm import MongoModel, fields, connect

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bm590
connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")

class User(MongoModel):
    """Model for user to show in database

       Based off of the Mongo Model

    """
    patient_name   = fields.CharField()
    user_id        = fields.CharField()
    password       = fields.CharField()
    dimension1     = fields.IntegerField()
    dimension2     = fields.IntegerField()
    classification = fields.CharField()
    image_content  = fields.CharField()
    unique_id      = fields.IntegerField()
    date           = fields.DateTimeField()

    def insert(self,content, patient_name, user_id, password, dimension1, dimension2, classfication, date):
        """Function to allow the user to import photo for the database

            Creates a user object for the database and assigns it a
            unique id

            :param content: the image photo data, passed as a string
            :param patient_name: name of the patient
            :param user_id(char): the user id for the patient logged in
            :param password(char): password for the user
            :param dimension1(int): 1st dimension for photo
            :param dimension2(int): 2nd dimension for photo
            :param classification(string): array of prob for the tensor flowi
            :rtype: the unique id of the user registered
        """

        unique_id = ''.join(random.choice(string.digits) for _ in range(12))
        user = User(patient_name, user_id, password, dimension1, dimension2, classfication, \
            content, unique_id, date)
        user.save()
        return user.unique_id

    def change_params(self, name, param, value):
        """Function to change the parameters of the user in database

           :param name(str): Name of person want to change
           :param param(str): Name of param you want to change
           :param value(varies): What you want to change the att to
           :rtype: None
        """

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

    def get_user_by_unique_ID(self,unique_id):
         """Function to print out the data after giving unique id

            :param unique_id(int): the unique digit for each entry
            :rtype: ret_dict the dictionary holding the info
         """

         user = User.objects.get({'unique_id':unique_id})
         ret_dict = {'name':user.patient_name, 'user_id':user.user_id, \
                 'password':user.password, 'dimension1':user.dimension1, \
                 'dimension2':user.dimension2, 'classification':user.classification, \
                 'image_content':user.image_content, 'date/time':user.date}
         return ret_dict


    def get_user_by_user_ID(self,user_id):
        """Function to get the user by giving the user id

            :param user_id(string): the user_id for each entry
            :rtype: returns a dicitonary with all of the information
        """

        user = User.objects.get({'user_id':user_id})
        ret_dict = {'name': user.patient_name, 'unique_id': user.unique_id, \
                'password': user.password, 'dimension1': user.dimension1, \
                'dimension2': user.dimension2, 'classification': user.classification, \
                'image_content':user.image_content, 'date/time':user.date}
        return ret_dict

if __name__ == '__main__':
    print("hello")
#    insert(12345, 'Daniel Wu', 'dwu', 'ilikebunnies', '1200', '1080', '0.95')
#    change_params('Daniel Wu', 'user id', 'dwu<3') get_user_by_user_ID("dwu<3")
