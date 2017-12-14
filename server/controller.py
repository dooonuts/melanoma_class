import databaseUser
import string
import databaseDoctor
import numpy as np
import time
import base64
from random import *
import tensorflow as tf
from PIL import Image
from pymongo import MongoClient
from tensorflow_for_poets.scripts import label_image

client = MongoClient("mongodb://vcm-1915.vm.duke.edu:27017")
db = client.bme590


def store_image(
        doctor_id,
        filename,
        first_name,
        last_name,
        classification,
        date):
    """Function to store image for a specific patient, returns a specific username and password for the patient
        NOTE: Currently only accepts one patient per image, duplicate images for the
        same patient will be stored as separate entities
       :param content: the content of the imge to store
       :rtype: the image of the index
    """
    width = None
    height = None
    # image_64_encoded= convert_image(filename)
    with Image.open("static/" + filename) as img:
        width, height = img.size
    [user_id, password] = userid_password_generator()
    fullname = first_name + " " + last_name
    user = databaseUser.User()
    doctor = databaseDoctor.Doctor()
    unique_id = user.insert(
        filename,
        fullname,
        user_id,
        password,
        width,
        height,
        classification,
        date)
    doctor.add_patient_names(unique_id, doctor_id)

    return unique_id, user_id, password


def get_patient(unique_id):
    patient = databaseUser.User()
    patient_dict = patient.get_user_by_unique_ID(int(unique_id))
    return patient_dict


def get_patients(doctor_id):
    doctor = databaseDoctor.Doctor()
    patient_names = doctor.get_patient_names(doctor_id)
    patient_dicts = []
    for p in range(len(patient_names)):
        patient = databaseUser.User()
        patient_dict = patient.get_user_by_unique_ID(patient_names[p])
        patient_dicts.append(patient_dict)
    return patient_dicts


def check_doctors(user_id, password):
    doctor = databaseDoctor.Doctor()
    try:
        doctor_info = doctor.get_doctor_by_doctor_id(user_id)
        if doctor_info.password == password:
            return True
        else:
            return False
    except BaseException:
        return False


def add_doctor(doctor_name, user_id, password):
    doctor = databaseDoctor.Doctor()
    doctor.add_doctor(doctor_name, user_id, password)
    return


def convert_image(filename):
    """Function to convert the image

       :param filename: the name of the file to open
       :rtype: returning the base64 encodement
    """
    image = open(filename, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    return image_64_encode


def decode_image(image_64_encode, filename):
    """Function to decode the image

       :param image_64_encode: the encoded image
    """
    print(image_64_encode)
    image_decoded = base64.decodebytes(image_64_encode)
    # image_decoded = base64.decodestring(image_64_encode)
    image_results = open(filename, "w+b")
    image_results.write(image_decoded)


def userid_password_generator():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.digits
    user_id = "".join(choice(allchar)
                      for x in range(randint(min_char, max_char)))
    password = "".join(choice(allchar)
                       for x in range(randint(min_char, max_char)))
    return user_id, password


def retrain(graph):  # develop this later
    """Function to train the graph

       :param graph: the graph made in the previous fun
    """

    graph = label_image.load_graph("retrained_graph.pb")


def labeling(file_name):
    """Function to label image

       :param file_name: Name of file
       :rtype: DANIEL WHAT THIS
    """

    graph = label_image.load_graph("retrained_graph.pb")
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"
    t = label_image.read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                           {input_operation.outputs[0]: t})
        end = time.time()
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = label_image.load_labels("retrained_labels.txt")

    print('\nEvaluation time (1-image): {:.3f}s\n'.format(end - start))

    for i in top_k:
        print(labels[i], results[i])

    finallabel = None

    if (results[0] > results[1]):
        # print(labels[0])
        finallabel = labels[0]
    else:
        print(labels[1])
        finallabel = labels[1]

    return finallabel, results


if __name__ == '__main__':
    print(get_patients("iruvdonuts"))
    # [user_id, password]=userid_password_generator()
    # [labels, results] = labeling("tensorflow_for_poets/tf_files/melanoma_photos/benign/ISIC_0010892.jpg")
    # [finallabel, results] = labeling("labeled_image.jpg")
    # check_users('ilikebunnies2','stuff')
