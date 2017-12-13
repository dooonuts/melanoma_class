import database
import numpy as np
import time
import base64
import tensorflow as tf
from tensorflow_for_poets.scripts import label_image

def store_image(content):
    image_index = database(content)
    image_index = 1;
    return image_index

def convert_image(filename):
    image = open(filename,'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    print(image_64_encode)
    return image_64_encode

def decode_image(image_64_encode):
    image_decoded = base64.decodestring(image_64_encode)
    image_results = open('labeled_image.jpg','wb')
    image_results.write(image_decoded)

def label():
    labels = label_image.load_labels("retrained_labels.txt")
    print(labels)
    return labels

def graph():
    retrained_graph = label_image.load_graph("retrained_graph.pb")
    return retrained_graph

def retrain(graph): # develop this later
    graph = label_image.load_graph("retrained_graph.pb")

def labeling(file_name):
    graph = label_image.load_graph("retrained_graph.pb")
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"
    t = label_image.read_tensor_from_image_file(file_name, input_height=input_height,
                                    input_width=input_width,
                                    input_mean=input_mean,
                                    input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

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
    # converted_image = convert_image("tensorflow_for_poets/tf_files/melanoma_photos/benign/ISIC_0010892.jpg")
    # decode_image(converted_image)
    # [labels, results] = labeling("tensorflow_for_poets/tf_files/melanoma_photos/benign/ISIC_0010892.jpg")
    [finallabel, results] = labeling("labeled_image.jpg")