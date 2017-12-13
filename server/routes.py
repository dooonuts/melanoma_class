import sys
import json
import controller
import numpy as np
from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES

# app = Flask(__name__)

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'label_img'
configure_uploads(app, photos)

@app.route('/')
def login():
    """Template for home of webpage

       :rtype: home template on html
    """

    return render_template('homepage.html')

@app.route('/login_verification', methods= ['GET','POST'])
def login_verification():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    return json.dumps(password)

@app.route('/image', methods = ['GET','POST'])
def image():
    return render_template('image.html')

@app.route('/image/image_upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        [classification, probabilities] = controller.labeling("label_img/" + filename)
        return classification

@app.route('/image_data', methods=['POST'])
def image_data():
    """Routing that will post the image data

       :rtype: the index of the image
    """

    if(request.is_json):
        content = request.get_json()
        print(content)
    index = controller.store_image(content)
    print(index)
    return json.dumps(index)


@app.route('/image/<image_index>', methods=['GET'])
def image_index(image_index):
    """Routing to get the image index???

       :param image_index: image of the index
       :rtype: the index image???
       Daniel pls help
    """

    return image_index


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
