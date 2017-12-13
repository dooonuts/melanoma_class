import sys
import json
import controller
from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES

# app = Flask(__name__)

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'label_img'
configure_uploads(app, photos)

@app.route('/')
def home():
    """Template for home of webpage
       :rtype: home template on html
    """

    return render_template('home.html')

@app.route('/image', methods = ['GET','POST'])
def image():
    return render_template('image.html')

@app.route('/image/image_upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')



@app.route('/image_data', methods=['POST'])
def image_data():
    if(request.is_json):
        content = request.get_json()
        print(content)
    index = controller.store_image(content)
    print(index)
    return json.dumps(index)


@app.route('/image/<image_index>', methods=['GET'])
def image_index(image_index):
    return image_index


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
