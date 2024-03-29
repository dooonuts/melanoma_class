import datetime
from pymongo import MongoClient
from pymodm import MongoModel, fields, connect

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bme590
connect("mongodb://vcm-1915.vm.duke.edu:27017/bme590")


class Doctor(MongoModel):
    """Model for doctor to show in database

       Based off of the Mongo Model

    """
    patient_names = fields.ListField(blank=True)
    doctor_name = fields.CharField()
    user_id = fields.CharField()
    password = fields.CharField()

    def add_doctor(self, name, user_id, password):
        """Function to add a doctor to the database

            :param name: Name of doctor
            :param user_id: User id of the doctor
            :param password: password of the doctor
            :rtype: none
        """

        doctor = Doctor(list(), name, user_id, password).save()

    def add_patient_names(self, patients, doctor_id):
        """Function to add patients to the doctor

            :param patients: list of patients to add to doctor
            :param name: Name of doctor
            :rtype: None
        """
        doctor = Doctor.objects.get({'user_id': doctor_id})
        list_names = doctor.patient_names
        list_names.extend([patients])
        doctor.patient_names = list_names
        doctor.save()

    def get_patient_names(self, doctor_id):
        """Function to get patient names

           :param doctor_id: id of the doctor
           :rtype: the list of patients the doc sees
        """

        doctor = Doctor.objects.get({'user_id': doctor_id})
        list_names = doctor.patient_names
        return list_names

    def get_doctor_by_doctor_id(self, doctor_id):
        """Function to get doctor by id

           :param doctor_id: id of the doctor
           :rtype: the doctor object
        """

        doctor = Doctor.objects.get({'user_id': doctor_id})
        return doctor

    def delete_patient_names(self, patients, name):
        """Function to delete patient name from doctor list

            :param patients: list of patients to delete
            :param name: name of doctor
            :rtype: None
        """

        doctor = Doctor.objects.get({'doctor_name': name})
        old_list = doctor.patient_names
        new_list = [
            pat_name for pat_name in old_list if pat_name not in patients]
        doctor.patient_names = new_list
        doctor.save()


def mongo_add_patient_names(doctor_id, unique_id):
    """Function to add patient names for mongo

       :param doctor_id: the id of the doctor
       :param unique_id: Unique id of the person
    """

    doctor = db.doctor.find_one({"user_id": doctor_id})
    patients_list = doctor['patient_names']
    patients_list.extend([unique_id])
    db.doctor.update({"user_id": doctor_id},
                     {"$set": {"patient_names": patients_list}})


if __name__ == '__main__':
    bessie = Doctor()
    stuff = Doctor.objects.raw({'user_id': 'ilikebunnies'})
    print(stuff)
    print(stuff.first().password)
    # add_patient_names([123561790], 'ilikebunnies')
