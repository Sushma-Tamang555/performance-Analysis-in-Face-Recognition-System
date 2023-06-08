from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import math
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import os
from keras.models import load_model
import pickle
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import mysql.connector
from tkinter import messagebox
from datetime import datetime

class UploadImage:
    def __init__(self, root):
        self.root = root
        self.algorithmValue = StringVar()
        screen_width = root.winfo_screenwidth()

        rootWidth = 1450
        rootHeight = 900

        x = math.floor((screen_width / 2) - (rootWidth / 2))

        self.root.geometry(f"{rootWidth}x{rootHeight}+{x}+0")
        self.root.title("Attendance System")
        
        # create a frame widget
        bgFrame = Frame(self.root, bg="black")
        bgFrame.place(x=0, y=0, width=rootWidth, height=rootHeight)
        bgFrame.columnconfigure(0, weight=1)
        
        # add background image inside the frame
        bgImg = Image.open("StaticImages/background.jpg")
        bgImg = bgImg.resize((rootWidth,rootHeight), resample=Image.Resampling.LANCZOS)
        self.photoImage1 = ImageTk.PhotoImage(bgImg)
        bgLabel = Label(bgFrame, image=self.photoImage1)
        bgLabel.place(x=0, y=0, width=rootWidth, height=rootHeight)

        # add title label on top of the frame
        titleLabel = Label(bgFrame, text= "Mark Your Attendance", font=("times new roman", 35), bg="black",fg="green")
        titleLabel.place(x=20,y=10, width= rootWidth-40, height=50)
        
        # adding left frame
        frameWidth = 1350
        frameHeight = rootHeight - 100
        self.leftFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="", font=("times new roman",30,"bold"))
        self.leftFrame.place(x=50, y= 70, width= frameWidth, height= frameHeight)
        
        clearButton = Button(self.leftFrame, text="Clear Attendance", cursor="hand2", bd=1, command=self.clearAttendance)
        clearButton.place(relx=0.9, rely=0.11, anchor=CENTER)
        
        uploadButton = Button(self.leftFrame, text="Upload Image", cursor="hand2", bd=1, width=20, height=2, command=self.uploadFile)
        uploadButton.place(relx=0.5, rely=0.1, anchor=CENTER)

   
#    fuctions 
    def uploadFile(self):
        initial_dir = "TestImages"
        title = "Select file"
        file_types = [('Jpg files', '*.jpg'),('PNG files', '*.png'),('Jpeg files','*.jpeg')]
        file_path = tk.filedialog.askopenfilename(initialdir=initial_dir, title=title, filetypes=file_types)
        # print(file_path)
        if file_path:
            img = Image.open(file_path)
            img = img.resize((200, 200))
        
            self.photoImage = ImageTk.PhotoImage(img)
            imageLabel = Label(self.leftFrame, image=self.photoImage)
            imageLabel.place(relx=0.5, rely=0.3, anchor=CENTER)
            
            chooseAlgorithmLabel = Label(self.leftFrame, text="Choose Algorithm:", font=("times new roman", 15, "bold"), bg="white", fg="black")
            chooseAlgorithmLabel.place(relx=0.45, rely= 0.5, anchor=CENTER)
            
            algoCombo = ttk.Combobox(self.leftFrame, values=["CNN", "LBPH"], font=("times new roman", 15), state="readonly",textvariable=self.algorithmValue)
            algoCombo.current(0) # set default value to "CNN"
            algoCombo.place(relx=0.57, rely= 0.5, anchor=CENTER)
            
            attendanceButton = Button(self.leftFrame, text="Mark Attendance", cursor="hand2", bd=1, width=12, height=2, command=lambda: self.markAttendance(algorithm=self.algorithmValue.get(), path=file_path))
            attendanceButton.place(relx=0.5, rely=0.6, anchor=CENTER)
 
    def markAttendance(self, algorithm, path):
        predictedValue = ""
        # trueValue = os.path.basename(os.path.dirname(path))
        # print(trueValue)
        print(algorithm)
        if algorithm == "CNN":
            predictedValue = self.markWithCnn(imagePath=path)     
        else: 
            predictedValue = self.markWithLbph(imagePath=path) 
            
        predictedLabel = Label(self.leftFrame, text= "Predicted: " + predictedValue, font=("times new roman", 15, "bold"), bg="white", fg="black", width=30)
        predictedLabel.place(relx=0.4, rely=0.7)
                   
        
    def markWithCnn(self, imagePath):
        model = load_model('myModel.h5')
        with open('MapCnn.pkl', 'rb') as f:
            resultMap = pickle.load(f)
            print(resultMap)
            
        test_image = image.load_img(imagePath, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        pred = model.predict(test_image, verbose=0)
        predId = np.argmax(pred)
        name = resultMap[int(predId)]  
        confidence = round(float(pred[0][predId]), 2) * 100
        if confidence > 80:
            predictedValue = name 
            self.markAttendanceDatabase(predictedValue)
        else :
           predictedValue = "Face not recognized" 
        
        return predictedValue  
   

    def markWithLbph(self, imagePath):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('LbphModel.yml')
        
        # Load the label map
        with open('MapLbph.pkl', 'rb') as f:
            resultMap = pickle.load(f)
            print(resultMap)
            
        img = Image.open(imagePath).convert('L')
        label_id, pred = recognizer.predict(np.array(img))
        name = next(name for name, id in resultMap.items() if id == label_id)
        
        confidence = int(100*(1-pred/300))
        if confidence > 80 :
            predictedValue = name 
            self.markAttendanceDatabase(predictedValue)
        else:
            predictedValue = "Face not recognized"
       
        return predictedValue
    
    def clearAttendance(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="AttendanceSystem")
        cursor=connection.cursor()
        updateQuery = "UPDATE MyTable SET attendance = %s, time = %s WHERE 1=1"
        values = ("Absent", None)
        cursor.execute(updateQuery, values)
        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Attendance Cleared")
        
    def markAttendanceDatabase(self,name):
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="AttendanceSystem")
        cursor=connection.cursor()
        now = datetime.now()
        currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

        updateQuery = "UPDATE MyTable SET attendance = %s, time = %s WHERE name = %s"
        val = ("Present", currentTime,name)
        
        cursor.execute(updateQuery,val)
        connection.commit()

    
    
if __name__ == "__main__":
    root = Tk()
    obj = UploadImage(root)
    root.mainloop()
