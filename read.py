# Description: Reads MNIST dataset and save the images into test and train folders with the correct labels

import os
import codecs
import numpy
import cv2 as cv

datapath = 'C:/Users/DELL/Desktop/OpenCV/MNIST_Data/'

files = os.listdir(datapath)


def get_int(b):   # CONVERTS 4 BYTES TO A INT
    return int(codecs.encode(b, 'hex'), 16)


def read():
    data_dict = {}
    for file in files:
        if file.endswith('ubyte'):  # FOR ALL 'ubyte' FILES
            print('Reading ', file)
            with open(datapath+file, 'rb') as f:
                data = f.read()
                # 0-3: THE MAGIC NUMBER TO WHETHER IMAGE OR LABEL
                type = get_int(data[:4])
                # 4-7: LENGTH OF THE ARRAY  (DIMENSION 0)
                length = get_int(data[4:8])
                if (type == 2051):
                    category = 'images'
                    # NUMBER OF ROWS  (DIMENSION 1)
                    num_rows = get_int(data[8:12])
                    # NUMBER OF COLUMNS  (DIMENSION 2)
                    num_cols = get_int(data[12:16])
                    # READ THE PIXEL VALUES AS INTEGERS
                    parsed = numpy.frombuffer(
                        data, dtype=numpy.uint8, offset=16)
                    # RESHAPE THE ARRAY AS [NO_OF_SAMPLES x HEIGHT x WIDTH]
                    parsed = parsed.reshape(length, num_rows, num_cols)
                elif (type == 2049):
                    category = 'labels'
                    # READ THE LABEL VALUES AS INTEGERS
                    parsed = numpy.frombuffer(
                        data, dtype=numpy.uint8, offset=8)
                    # RESHAPE THE ARRAY AS [NO_OF_SAMPLES]
                    parsed = parsed.reshape(length)
                if (length == 10000):
                    set = 'test'
                elif (length == 60000):
                    set = 'train'
                # SAVE THE NUMPY ARRAY TO A CORRESPONDING KEY
                data_dict[set+'_'+category] = parsed
    return data_dict


def save():
    sets = ['train', 'test']
    data_dict = read()
    for set in sets:
        images = data_dict[set+'_images']
        labels = data_dict[set+'_labels']
        no_of_samples = images.shape[0]
        for i in range(no_of_samples):
            image = images[i]
            label = labels[i]
            # CREATE A FOLDER FOR EACH LABEL
            if not os.path.exists(datapath+set+'/'+str(label)):
                os.makedirs(datapath+set+'/'+str(label))
            # SAVE THE IMAGE TO THE CORRESPONDING FOLDER
            cv.imwrite(datapath+set+'/'+str(label)+'/'+str(i)+'.png', image)
