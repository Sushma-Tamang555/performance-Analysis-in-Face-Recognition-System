from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import mysql.connector
from datetime import datetime

class AttendanceLists:
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
        bgImg = bgImg.resize((1100,710), Image.ANTIALIAS)
        self.photoImage = ImageTk.PhotoImage(bgImg)
        bgLabel = Label(bgFrame, image=self.photoImage)
        bgLabel.place(x=0, y=0, width=1100, height=700)

        # add title label on top of the frame
        titleLabel = Label(bgFrame, text= "Attendance Lists", font=("times new roman", 35), bg="black",fg="green")
        titleLabel.place(x=20,y=10, width= 1080, height=50)
        
        # create left frame
        leftFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Attendance Lists", font=("times new roman",15,"bold"))
        leftFrame.place(x=20, y= 70, width= 600, height= (700-80))
        
        # create a horizontal scrollbar
        scrollX = ttk.Scrollbar(leftFrame, orient=HORIZONTAL)
        scrollX.pack(side=BOTTOM, fill=X)

        # create a vertical scrollbar
        scrollY = ttk.Scrollbar(leftFrame, orient=VERTICAL)
        scrollY.pack(side=RIGHT, fill=Y)

        # create the attendance table
        self.attendanceTable = ttk.Treeview(leftFrame,columns=("Name","Age","Address", "Attendance","Time"),xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
        # create a custom style for the Treeview
        self.customStyle = ttk.Style()
        self.customStyle.theme_use("default")
        self.customStyle.configure("Custom.Treeview", background="white", fieldbackground="white")


        # set the scrollbar commands
        scrollX.config(command=self.attendanceTable.xview)
        scrollY.config(command=self.attendanceTable.yview)

        # set the column headings for the attendance table
        self.attendanceTable.heading("Name", text="Name")
        self.attendanceTable.heading("Age", text="Age")
        self.attendanceTable.heading("Address", text="Address")
        self.attendanceTable.heading("Attendance", text="Attendance")
        self.attendanceTable.heading("Time", text="Time")
        self.attendanceTable["show"]="headings"

        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)  
        
         # bind the <<TreeviewSelect>> event to the onSelect method
        self.attendanceTable.bind("<<TreeviewSelect>>", self.onSelect)
        
        # pack the attendance table
        self.attendanceTable.pack(fill=BOTH, expand=1)
        self.getAttendanceList()

        # right frame 
        # create left frame
        rightFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Attendance Lists", font=("times new roman",15,"bold"))
        rightFrame.place(x=650, y= 150, width= 420, height= (500))

        # Create variables to hold user input
        self.nameVal = StringVar()
        self.ageVal = StringVar()
        self.AddressVal = StringVar()
        self.AttendanceVal = StringVar()

        # name label and textfield
        nameLabel = Label(rightFrame, text="Name:", font=("times new roman", 15, "bold"),bg="white", fg="black")
        nameLabel.grid(row=0,column=0, padx=30, pady=20)
        nameText = Entry(rightFrame, font=("times new roman", 15), bd=0, relief=RIDGE, bg="white",fg="black",textvariable=self.nameVal,state="readonly")
        nameText.grid(row=0,column=1, padx=0, pady=20)

        # age label and textfield
        ageLabel = Label(rightFrame, text="Age:", font=("times new roman", 15, "bold"), bg="white", fg="black")
        ageLabel.grid(row=1,column=0, padx=30, pady=20)
        ageText = Entry(rightFrame, font=("times new roman", 15), bd=0, relief=RIDGE, bg="white",fg="black", textvariable=self.ageVal)
        ageText.grid(row=1,column=1, padx=0, pady=20)

        # address label and textfield
        addressLabel = Label(rightFrame, text="Address:", font=("times new roman", 15, "bold"), bg="white", fg="black")
        addressLabel.grid(row=2,column=0, padx=30, pady=20)
        addressText = Entry(rightFrame, font=("times new roman", 15), bd=0, relief=RIDGE, bg="white",fg="black", textvariable=self.AddressVal)
        addressText.grid(row=2,column=1, padx=0, pady=20)

        # attendance label and combobox
        attendanceLabel = Label(rightFrame, text="Attendance:", font=("times new roman", 15, "bold"), bg="white", fg="black")
        attendanceLabel.grid(row=3,column=0, padx=30, pady=20)
        attendanceCombo = ttk.Combobox(rightFrame, values=["Absent", "Present"], font=("times new roman", 15), state="readonly",textvariable=self.AttendanceVal)
        attendanceCombo.current(0) # set default value to "Absent"
        attendanceCombo.grid(row=3, column=1, padx=0, pady=20)
       
        updateButton = Button(rightFrame, text="Update Record", font=("times new roman", 15, "bold"), bg="green", bd=0, cursor="hand2",height=2, command=self.checkForEmptyField)
        updateButton.place(relx=0.4, rely= 0.8)

          
    def onSelect(self, event):
        # get the selected row
        selected_item = self.attendanceTable.focus()
        # get the name of the selected row
        if len(self.attendanceTable.item(selected_item)['values']) > 0:
            name = self.attendanceTable.item(selected_item)['values'][0]
            print(name)
            self.getAttendanceDetail(name)

    def checkForEmptyField(self):
        name = self.nameVal.get()
        address = self.AddressVal.get()
        age = self.ageVal.get()
       
        if name == "" or address == "" or age == "":
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return
        
        elif not age.isdigit():
            messagebox.showerror("Error", "Invalid age: please enter a integer")
            return

        elif int(age) <= 0:
             messagebox.showerror("Error", "Invalid age: please enter a value greater than 0.")
             return
        
        else:
            self.updateDetail()


    def getAttendanceList(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="AttendanceSystem"
        )

        cursor = connection.cursor()
        sql_query = "SELECT * FROM MyTable"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        for row in results:
            if row is None or len(row) == 0:
                print("empty")
            else:
                self.attendanceTable.insert("", "end", values=row)
            
        # Closing the cursor and database connection
        cursor.close()
        connection.close()


    def getAttendanceDetail(self,name):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="AttendanceSystem"
        )
        cursor = connection.cursor()
        sql = "SELECT * FROM MyTable WHERE name = %s"
        val = (name,)
        cursor.execute(sql,val)
        results = cursor.fetchall()

        for row in results:
            print(row)
            name = row[0]
            age = row[1]
            address = row[2]

            self.nameVal.set(name)
            self.ageVal.set(age)
            self.AddressVal.set(address)

            if row[3] == "Absent":
               self.AttendanceVal.set("Absent")
            else:
                self.AttendanceVal.set("Present")

        cursor.close()
        connection.close()

    def updateDetail(self):
        name = self.nameVal.get()
        address = self.AddressVal.get()
        attendance = self.AttendanceVal.get()
        age = self.ageVal.get()

        # get current datetime
        now = datetime.now()
        currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="AttendanceSystem"
        )
        cursor = connection.cursor()

        # execute SQL query to update record
        sql = "UPDATE MyTable SET age = %s, address = %s, attendance = %s, time= %s WHERE name = %s"
        val = (age, address, attendance,currentTime,name)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Record updated Successfully.", "Record has been updated successfully.")
        self.attendanceTable.delete(*self.attendanceTable.get_children())
        self.getAttendanceList()
    

if __name__ == "__main__":
    root = Tk()
    obj = AttendanceLists(root)
    root.mainloop()
