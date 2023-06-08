from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPool2D, Flatten, Dense
import time
import pickle
import numpy as np
import os
import cv2
from tkinter import messagebox

def preprocess_image(image_path, target_size):
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_resized = cv2.resize(image_gray, target_size)
    image_normalized = image_resized / 255.0
    return image_normalized

def load_dataset(directory, target_size):
    images = []
    labels = []

    for label_name in os.listdir(directory):
        label_dir = os.path.join(directory, label_name)
        if not os.path.isdir(label_dir):
            continue

        for image_name in os.listdir(label_dir):
            image_path = os.path.join(label_dir, image_name)
            image = preprocess_image(image_path, target_size)
            if image is None:
                continue

            images.append(image)
            labels.append(label_name)

    return np.array(images), np.array(labels)


def TrainModelCnn():
    # Specifying the folder where images are present
    TrainingImagePath = 'newImages/'
    # TestingImagePath = 'FaceImages/Testing'

    imageSize = [224, 224]

    # Defining pre-processing transformations on raw images of training data
    trainDatagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

    # Defining pre-processing transformations on raw images of testing data
    testDatagen = ImageDataGenerator(rescale=1./255)

    # Generating the Training Data
    trainingSet = trainDatagen.flow_from_directory(TrainingImagePath, target_size=imageSize, batch_size=32, class_mode='categorical')

    # Generating the Testing Data
    testSet = testDatagen.flow_from_directory(TrainingImagePath, target_size=imageSize, batch_size=32, class_mode='categorical')

    trainClasses = testSet.class_indices

    # Storing the face and the numeric tag for future reference
    ResultMap = {}
    for faceValue, faceName in zip(trainClasses.values(), trainClasses.keys()):
        ResultMap[faceValue] = faceName

    with open("ResultsMap.pkl", 'wb') as fileWriteStream:
        pickle.dump(ResultMap, fileWriteStream)

    # This mapping will help to get the corresponding face name for it
    print("Mapping of Face and its ID", ResultMap)

    totalClasses = len(trainingSet.class_indices)
    print('\n The Number of classes: ', totalClasses)

    # The number of neurons for the output layer is equal to the number of faces
    OutputNeurons = trainingSet.num_classes

    # Create CNN deep learning model
    classifier = Sequential()
    classifier.add(Convolution2D(32, kernel_size=(5, 5), strides=(1, 1), input_shape=(*imageSize, 3), activation='relu'))
    classifier.add(MaxPool2D(pool_size=(2, 2)))
    classifier.add(Convolution2D(64, kernel_size=(5, 5), strides=(1, 1), activation='relu'))
    classifier.add(MaxPool2D(pool_size=(2, 2)))
    classifier.add(Flatten())
    classifier.add(Dense(64, activation='relu'))
    classifier.add(Dense(OutputNeurons, activation='softmax'))
    classifier.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

    # Measuring the time taken by the model to train
    StartTime = time.time()

    # Starting the model training
    classifier.fit(trainingSet, steps_per_epoch=trainingSet.samples//trainingSet.batch_size, epochs=5, validation_data=testSet, validation_steps=testSet.samples//testSet.batch_size)

    EndTime = time.time()
    print("Total Time Taken: ", round((EndTime-StartTime)/60), 'Minutes')

    classifier.save("mymodel.h5")
    messagebox.showinfo("Model Saved", "Successfully Trained model")



# trainModel()