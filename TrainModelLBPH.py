import os
import cv2
import numpy as np
import pickle
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


def TrainModelLbph():
    training_image_path = 'newImages/'
    # Load face detection and recognition models
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Create empty lists to store faces and labels
    faces = []
    labels = []
    label_id = 0
    label_map = {}

    for root, dirs, files in os.walk(training_image_path):
        for file in files:
            if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg'):
                path = os.path.join(root, file)
                label = os.path.basename(root).lower()

                if label not in label_map:
                    label_map[label] = label_id
                    label_id += 1

                # Load image and convert to grayscale
                image = cv2.imread(path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces in the image
                faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                # Extract faces and labels
                for (x, y, w, h) in faces_rect:
                    face = gray[y:y + h, x:x + w]
                    faces.append(face)
                    labels.append(label_map[label])

    # Save label map to a file using pickle
    with open('ResultsMap.pkl', 'wb') as f:
        pickle.dump(label_map, f)

    # Train the recognizer using faces and labels
    recognizer.train(faces, np.array(labels))

    # Save the trained recognizer to a file
    recognizer.save('LbphModel.yml')
    messagebox.showinfo("Model Saved", "Successfully Trained model")


# TrainModelLbph()
