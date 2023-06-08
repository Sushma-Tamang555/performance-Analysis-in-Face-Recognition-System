from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import math
from Comparision import ComparisionScreen
from AttendanceLists import AttendanceLists
from UploadImage import UploadImage
import mysql.connector
from tkinter import messagebox

class Home:
    def __init__(self, root):
        self.root = root
        self.algorithmVal = StringVar()
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
        titleLabel = Label(bgFrame, text= "Home Screen", font=("times new roman", 35), bg="black",fg="green")
        titleLabel.place(x=20,y=10, width= rootWidth-40, height=50)
        
        # adding left frame
        frameWidth = 1350
        frameHeight = rootHeight - 100
        centerFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Home Screen", font=("times new roman",30,"bold"))
        centerFrame.place(x=50, y= 70, width= frameWidth, height= frameHeight)
        
        # button to clear the attendance in database
        clearButton = Button(centerFrame, text="Clear Attendance", cursor="hand2", bd=1, command=self.clearAttendance)
        clearButton.place(relx=0.94, rely=0, anchor=CENTER)
        
        # Button to Mark Attendancee
        image1 = Image.open("StaticImages/trainUsingCnn.PNG")
        image1 = image1.resize((200, 170),resample=Image.Resampling.LANCZOS)
        self.Photoimage1 = ImageTk.PhotoImage(image1)
        b1 = Button(centerFrame,image=self.Photoimage1,command=self.markAttendance, cursor="hand2")
        b1.place(relx=0.25, rely=0.27, anchor=CENTER)
        l1 = Label(centerFrame,text="MarkAttendance", cursor="hand2", height=2, bd=1, relief="solid",bg="white",fg="black")
        l1.place(relx=0.25, rely=0.38, anchor=CENTER)

        # Button to View Attendance
        image2 = Image.open("StaticImages/attendanceDetails.PNG")
        image2 = image2.resize((200, 170), resample=Image.Resampling.LANCZOS)
        self.Photoimage2 = ImageTk.PhotoImage(image2)
        b2 = Button(centerFrame,image=self.Photoimage2, cursor="hand2",command=self.AttendanceView)
        b2.place(relx=0.5, rely=0.27, anchor=CENTER)
        l2 = Label(centerFrame,text="View Attendance", cursor="hand2", height=2, bd=1, relief="solid",bg="white",fg="black")
        l2.place(relx=0.5, rely=0.38, anchor=CENTER)

        # Button to Show the Comparision Analysis
        image3 = Image.open("StaticImages/trainCnn.PNG")
        image3 = image3.resize((200, 170), resample=Image.Resampling.LANCZOS)
        self.Photoimage3 = ImageTk.PhotoImage(image3)
        b3 = Button(centerFrame,image=self.Photoimage3, cursor="hand2", command=self.comparision)
        b3.place(relx=0.75, rely=0.27, anchor=CENTER)
        l3 = Label(centerFrame,text="Performance Analysis", cursor="hand2", height=2, bd=1, relief="solid",bg="white",fg="black")
        l3.place(relx=0.75, rely=0.38, anchor=CENTER)
        
        
        # Button to MarkAttendance with real time images 
        image4 = Image.open("StaticImages/cnnMarkAttendance.PNG")
        image4 = image4.resize((200, 170), resample=Image.Resampling.LANCZOS)
        self.Photoimage4 = ImageTk.PhotoImage(image4)
        b4 = Button(centerFrame,image=self.Photoimage4, cursor="hand2", command=self.LiveAttendance)
        b4.place(relx=0.5, rely=0.6, anchor=CENTER)
        l4 = Label(centerFrame,text="Live Attendance", cursor="hand2", height=2, bd=1, relief="solid",bg="white",fg="black")
        l4.place(relx=0.5, rely=0.71, anchor=CENTER)
        
        chooseAlgorithmLabel = Label(centerFrame, text="Choose Model:", font=("times new roman", 15, "bold"), bg="white", fg="black")
        chooseAlgorithmLabel.place(relx=0.43, rely= 0.8, anchor=CENTER)
        
        algoCombo = ttk.Combobox(centerFrame, values=["LBPHModel", "CNNModel"], font=("times new roman", 15), state="readonly",textvariable=self.algorithmVal)
        algoCombo.current(0) # set default value to "CNN"
        algoCombo.place(relx=0.54, rely= 0.8, anchor=CENTER)
        
               
    def markAttendance(self):
        self.new_window = Toplevel(self.root)
        self.app = UploadImage(self.new_window)

    def comparision(self):
        self.new_window = Toplevel(self.root)
        self.app = ComparisionScreen(self.new_window)
        
    def AttendanceView(self):
        self.new_window = Toplevel(self.root)
        self.app = AttendanceList(self.new_window) 
    
    def LiveAttendance(self):
        algorithm = self.algorithmVal.get()
        print(algorithm)
        import FaceRecognitionCNN, FaceRecognitionLbph
        if algorithm == "CNNModel":
            FaceRecognitionCNN.faceDetectionCnn()     
        elif algorithm == "LBPHModel":
            FaceRecognitionLbph.faceDetectionLbph()
            
    def clearAttendance(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="AttendanceSystem")
        cursor=connection.cursor()
        updateQuery = "UPDATE MyTable SET attendance = %s, time = %s WHERE 1=1"
        values = ("Absent", None)
        cursor.execute(updateQuery, values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("", "Attendance Cleared Successfully")
        
if __name__ == "__main__":
    root = Tk()
    obj = Home(root)
    root.mainloop()
