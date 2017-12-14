import datetime
from pymongo import MongoClient
from pymodm import MongoModel, fields, connect

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bm590
connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")

class Doctor(MongoModel):
    """Model for doctor to show in database

       Based off of the Mongo Model

    """
    patient_names = fields.ListField()
    doctor_name   = fields.CharField()
    user_id       = fields.CharField()
    password      = fields.CharField()

def add_doctor(patients, name, user_id, password):
    """Function to add a doctor to the database

       :param patients: list of patients the doctor has
       :param name: Name of doctor
       :param user_id: User id of the doctor
       :param password: password of the doctor
       :rtype: none
    """

    doctor = Doctor(patients, name, user_id, password).save()

def add_patient_names(patients, name):
    """Function to add patients to the doctor

       :param patients: list of patients to add to doctor
       :param name: Name of doctor
       :rtype: None
    """

    doctor = Doctor.objects.get({'doctor_name':name})
    list_names = doctor.patient_names
    list_names.extend(patients)
    doctor.patient_names = list_names
    doctor.save()

def delete_patient_names(patients, name):
    """Function to delete patient name from doctor list

       :param patients: list of patients to delete
       :param name: name of doctor
       :rtype: None
    """

    doctor = Doctor.objects.get({'doctor_name':name})
    old_list = doctor.patient_names 
    new_list = [pat_name for pat_name in old_list if pat_name not in patients]
    doctor.patient_names = new_list
    doctor.save()

if __name__ == '__main__':
    delete_patient_names(['Brianna'], 'Arjun')

