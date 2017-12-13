import sys
import json
import controller
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    """Template for home of webpage
       
       :rtype: home template on html
    """

    return render_template('home.html')


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
