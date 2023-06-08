import cv2
import pickle
import mysql.connector
from datetime import datetime

def faceDetectionLbph():
    # Load the trained recognizer and label map
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('LbphModel.yml')
    
    connection = mysql.connector.connect(host="localhost", user="root", password="", database="AttendanceSystem")
    cursor=connection.cursor()

    with open('ResultsMap.pkl', 'rb') as f:
        resultMap = pickle.load(f)

    # Load the face detection cascade classifier
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize the video capture device
    videoCapture = cv2.VideoCapture(0)
    # Set the frame width and height to capture high-quality images
    videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    while True:
        # Read a frame from the video capture device
        _ , frame = videoCapture.read()

        # Convert the frame to grayscale and detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Loop over the detected faces and recognize them
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extract the face region and predict the label
            face = gray[y:y + h, x:x + w]
            label_id, pred = recognizer.predict(face)

            # Get the label name from the label map
            name = next(name for name, id in resultMap.items() if id == label_id)
            
            confidence = int(100*(1-pred/300))
        
            # Display the predicted label and confidence score
            if confidence > 80:
                now = datetime.now()
                currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

                updateQuery = "UPDATE MyTable SET attendance = %s, time = %s WHERE name = %s"
                val = ("Present", currentTime,name)
                
                cursor.execute(updateQuery,val)
                connection.commit()
                
                # text = f'{name} ({confidence:.2f})'
                text = f'{name +  "(Marked)"}'
                color = (0, 255, 0)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            else:
                label = "Unknown Face"      
                text = f'{label}'
                color = (0, 255, 0)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        #  Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == 13:
            break

    # Release the video capture device and close all windows
    videoCapture.release()
    cv2.destroyAllWindows()
    cursor.close()
    connection.close()

# faceDetectionLbph()
