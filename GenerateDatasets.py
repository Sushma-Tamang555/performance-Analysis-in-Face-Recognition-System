from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import math
import cv2
import os
import mysql.connector

class MyDataset:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        
        width = 1100
        height = 700

        x = math.floor((screen_width / 2) - (width / 2))
        self.root.geometry(f"{width}x{height}+{x}+0")
        self.root.title("Attendance System")
        
        # create a frame widget
        bgFrame = Frame(self.root, bg="black")
        bgFrame.place(x=0, y=0, width=1100, height=700)
        bgFrame.columnconfigure(0, weight=1)
        
        # add background image inside the frame
        bgImg = Image.open("StaticImages/background.jpg")
        bgImg = bgImg.resize((1100,710), Image.Resampling.LANCZOS)
        self.photoImage = ImageTk.PhotoImage(bgImg)
        bgLabel = Label(bgFrame, image=self.photoImage)
        bgLabel.place(x=0, y=0, width=1100, height=700)

        # add title label on top of the frame
        titleLabel = Label(bgFrame, text= "Generate Dataset", font=("times new roman", 35), bg="black",fg="green")
        titleLabel.place(x=10,y=10, width= 1080, height=50)

        # make a center label Frame 
        centerFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Generate Datasets", font=("times new roman",15,"bold"))
        centerFrame.place(x=20, y= 70, width= 1040, height= (600))

        # Create variables to hold user input
        self.nameVal = StringVar()
        self.ageVal = StringVar()
        self.AddressVal = StringVar()

        # Name Label and Entry
        nameLabel = Label(centerFrame, text="Name:", font=("times new roman", 20), bg="white", fg="black")
        nameLabel.place(relx=0.3, rely=0.2, anchor=W)
        nameEntry = Entry(centerFrame, font=("times new roman", 20), textvariable=self.nameVal, bg="white",fg="black")
        nameEntry.place(relx=0.6, rely=0.2, anchor=CENTER)

        # Age Label and Entry
        ageLabel = Label(centerFrame, text="Age:", font=("times new roman", 20), bg="white",fg="black")
        ageLabel.place(relx=0.3, rely=0.3, anchor=W)
        ageEntry = Entry(centerFrame, font=("times new roman", 20), textvariable=self.ageVal, bg="white",fg="black")
        ageEntry.place(relx=0.6, rely=0.3, anchor=CENTER)

        # Address Label and Entry
        AddressLabel = Label(centerFrame, text="Address:", font=("times new roman", 20), bg="white",fg="black")
        AddressLabel.place(relx=0.3, rely=0.4, anchor=W)
        AddressEntry = Entry(centerFrame, font=("times new roman", 20), textvariable=self.AddressVal, bg="white",fg="black")
        AddressEntry.place(relx=0.6, rely=0.4, anchor=CENTER)

        # Generate Datasets Button
        generateButton = Button(centerFrame, text="Generate Datasets",bg="yellow", fg='green', font=("times new roman", 25), height=1, highlightthickness=0, command=self.checkForEmptyField)     
        generateButton.place(relx=0.5, rely=0.7, anchor=CENTER)


    # Functions
    # function to check the field is empty or not 
    def checkForEmptyField(self):
        name = self.nameVal.get()
        age = self.ageVal.get()
        address = self.AddressVal.get()

        userFolder = './newImages/' + name

        # Check if any field is empty
        if name == "" or age == "" or address == "":
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return
        elif not age.isdigit():
            messagebox.showerror("Error", "Invalid age: please enter a integer.")
            return
        elif int(age) <=0 :
            messagebox.showerror("Error", "please enter a positive integer greater than 0.")
            return
        elif os.path.exists(userFolder):
            messagebox.showwarning("Warning", "User already exists. Please try a different name.")
            self.nameVal.set("")
            self.ageVal.set("")
            self.AddressVal.set("")
            return
        else:
            self.insertData(name, age, address)
            self.generateDataset()


    # insert data to mysql
    def insertData(self, name,age, address):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="AttendanceSystem"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MyTable")
        results = cursor.fetchall()

        attendance = "Absent"
        time = None

        # left here
        sql = "INSERT INTO MyTable(name, age, address, attendance, time) VALUES (%s, %s, %s, %s, %s)"
        values = (name, age, address, attendance, time)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        print("Data inserted successfully.")


    # function to generate datasets
    def generateDataset(self):
        def CropFace(img):
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_classifier.detectMultiScale(img, 1.3, 5)

            if len(faces) == 0:
                return None
            for (x,y,w,h) in faces:
                croppedFace = img[y:y+h,x:x+w]
                return croppedFace

        cap = cv2.VideoCapture(0)
        count = 0
        face = None

        name = self.nameVal.get()

        trainingFolder = './newImages/'+ name

        # Create a new folder for the user if it doesn't exist
        if not os.path.exists(trainingFolder):
            os.makedirs(trainingFolder)


        while True:
            ret, frame = cap.read()
            if CropFace(frame) is not None:
                count+= 1
                face = cv2.resize(CropFace(frame),(400,400))
                file_name_path = trainingFolder + '/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(count), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                cv2.imshow("Collecting Images", face)

            if cv2.waitKey(1)==13 or int(count)>=110: #13 is the ASCII character of Enter
                break

        cap.release()
        cv2.destroyAllWindows()

        messagebox.showinfo("Sample Collection Completed", "Collecting samples is completed....")
        self.nameVal.set("")
        self.ageVal.set("")
        self.AddressVal.set("")
