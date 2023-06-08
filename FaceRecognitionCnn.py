import cv2
import numpy as np
import pickle
from keras.models import load_model
import mysql.connector
from datetime import datetime

def faceDetectionCnn():
    # Load the model and cascade classifier
    model = load_model('myModel.h5')
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
     
    connection = mysql.connector.connect(host="localhost", user="root", password="", database="AttendanceSystem")
    cursor=connection.cursor()

    # Load the ResultMap from file
    # with open("resultsMap.pkl", 'rb') as fileReadStream:
    #     resultMap = pickle.load(fileReadStream)
        
    with open('resultsMap.pkl', 'rb') as f:
        resultMap = pickle.load(f)

    # Open the video capture device
    videoCapture = cv2.VideoCapture(0)

    # Set the frame width and height to capture high-quality images
    videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Loop through each frame of the video
    while True:
        # Read the frame from the video capture device
        _, frame = videoCapture.read()

        # Detect the faces in the frame and make a prediction for each face
        faces = faceCascade.detectMultiScale(frame, 1.3, 5)
        for (x, y, w, h) in faces:
            # Crop the face and preprocess it for the model
            croppedFace = cv2.resize(frame[y:y+h, x:x+w], (224, 224))
            croppedFace = np.expand_dims(croppedFace, axis=0)
            croppedFace = np.expand_dims(croppedFace, axis=-1)

            # Make a prediction for the face and get the label with the highest score
            pred = model.predict(croppedFace, verbose = 0)
            predId = np.argmax(pred)  # get the index of the highest predicted probability value
            
            # convert predId to int type and use it to access resultMap
            # Get the confidence score (highest predicted probability value)
            confidence = int(100*(1-np.max(pred)/300))
            name = resultMap[int(predId)]

            # Draw a rectangle around the face and label it with the predicted name if confidence is > 70%
            if confidence > 80:
                now = datetime.now()
                currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

                updateQuery = "UPDATE MyTable SET attendance = %s, time = %s WHERE name = %s"
                val = ("Present", currentTime,name)
                
                cursor.execute(updateQuery,val)
                connection.commit()
                            
                text = f'{name} ({confidence:.2f})'
                color = (0, 255, 0)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                              
            else:
                label = "unknown face"
                text = f'{label} ({confidence:.2f})'
                color = (0, 255, 0)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                
        # Show the frame with the detected faces and predicted labels
        cv2.imshow('Video', frame)

        # Exit the loop if the 'Enter' key is pressed
        if cv2.waitKey(1) == 13:  # 13 is the ASCII code for Enter key
            break

    # Release the video capture device and close all windows
    videoCapture.release()
    cv2.destroyAllWindows()
    cursor.close()
    connection.close()


# faceDetection()