import db

def store_image(content):
    image_index = db(content)
    # image_index = 1;
    return image_index
