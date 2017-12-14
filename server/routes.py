import sys
import os
import json
import controller
import numpy as np
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.secret_key = os.urandom(24)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/label_img'
configure_uploads(app, photos)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def login():
    """Template for home of webpage

       :rtype: home template on html
    """
    session.clear()
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        logged_in = controller.check_doctors(user_id, password)
        if(logged_in):
            session['user_id'] = request.form['user_id']
            return redirect(url_for('home'))
        else:
            redirect(request.url)
            flash('Invalid Username or Password')
    return render_template('login.html')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register_user.html')
    if request.method == 'POST' and request.form['doctor_name'] == '' or request.form[
            'user_id'] == '' or request.form['password'] == '':
        return render_template('register_user.html')
    doctor_name = request.form['doctor_name']
    user_id = request.form['user_id']
    password = request.form['password']
    controller.add_doctor(doctor_name, user_id, password)
    return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
def home():
    if(session.get('user_id')):
        return render_template("homepage.html", user_id=session['user_id'])
    return redirect(url_for('login'))


@app.route('/image', methods=['GET', 'POST'])
def image():
    if(session.get('user_id')):
        return render_template('upload.html')
    return redirect(url_for('login'))


@app.route('/image/image_upload', methods=['GET', 'POST'])
def upload():
    if(session.get('user_id')):
        user_id = session['user_id']
        # Checks to see if posting and if the photo exists in the files
        if request.method == 'POST' and 'photo' in request.files:
            # Checks to see if the file is null
            if request.files['photo'].filename == '' or request.form[
                    'firstname'] == '' or request.form['lastname'] == '' or request.form['date'] == '':
                flash('Invalid Parameters')
                return redirect(request.url)
            # Checks for Allowed Files
            if allowed_file(request.files['photo'].filename):
                filename = photos.save(request.files['photo'])
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                date = request.form['date']
                [classification, probabilities] = controller.labeling(
                    "static/label_img/" + filename)
                [unique_id, patient_id, patient_password] = controller.store_image(
                    user_id, "label_img/" + filename, firstname, lastname, classification, date)
                return render_template(
                    'results.html',
                    filename="../static/label_img/" + filename,
                    classification=classification,
                    probabilities=probabilities,
                    unique_id=unique_id,
                    patient_id=patient_id,
                    patient_password=patient_password)
            return redirect(url_for('image'))
        return redirect(url_for('image'))
    return redirect(url_for('login'))


@app.route('/image_base64', methods=['POST'])
def image_data():
    """Routing that will retrieve images from the Raspberry Pi

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
    """Returns the classification and index of a specfic image

       :param image_index: image of the index
       :rtype: the index image
       Daniel pls help
    """

    return image_index


@app.route('/image_data')
def images_data():
    if (session.get('user_id')):
        print(session['user_id'])
        patients = controller.get_images(session['user_id'])
        return render_template('image_data.html', patients=patients)
    return redirect(url_for('login'))


@app.route('/patients', methods=['GET'])
def patients():
    return


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
