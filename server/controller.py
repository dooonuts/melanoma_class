import db
from tensorflow_for_poets.scripts import label_image

def store_image(content):
    image_index = db(content)
    # image_index = 1;
    return image_index







if __name__ == '__main__':
    main()
