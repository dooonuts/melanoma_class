# melanoma_class

This is a Doctor's Portal meant to classify and track their patient's skin conditions. There is a simple and intuitive UI for the doctor to use. 

Features: Sessions, Login/Logout, Unique Identification, MongoDB, TensorFlow Classfication, Security

Main Endpoints
- Home
- Upload 
  * Uploads images to be classified as either benign or malignant
  * Stores the classification and the name in the database
  * Only accepts png, jpeg, or jpg files
  * All parameters must be complete to be stored in the database
  * For percentages, the first refers to probability benign and the second, malignant
- Images
  * A slideshow of images that the doctor has uploaded will be displayed here
  * The slideshow can be controlled by arrows on the sides of the image
  * The patient name will be displayed on the bottom right
- Patients
  * A list of the doctor's patients will be displayed here
  * Each patient can be referenced by their patient unique number which is randomly assigned
- Logout
  * Signs out of the session

NOTE: Currently does not support multiple images for the same patient. The patient portal has also not been completed and is still in development.
