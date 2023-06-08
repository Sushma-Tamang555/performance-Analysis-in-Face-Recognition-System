from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import math
from keras.models import load_model
import pickle
import numpy as np
from tensorflow.keras.preprocessing import image
import cv2
import os   

import EvaluateModel

class ComparisionScreen:
    def __init__(self, root):
        self.root = root

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
        self.photoImage = ImageTk.PhotoImage(bgImg)
        bgLabel = Label(bgFrame, image=self.photoImage)
        bgLabel.place(x=0, y=0, width=rootWidth, height=rootHeight)

        # add title label on top of the frame
        titleLabel = Label(bgFrame, text= "Analysis", font=("times new roman", 35), bg="black",fg="green")
        titleLabel.place(x=20,y=10, width= rootWidth-40, height=50)
        
        # adding left frame
        frameWidth = 700
        frameHeight = rootHeight - 100
        leftFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Result with CNN", font=("times new roman",30,"bold"))
        leftFrame.place(x=20, y= 70, width= frameWidth, height= frameHeight)

       # create a canvas inside the labelFrame for scrollable content
        leftCanvas = Canvas(leftFrame, bg='white', scrollregion=(0, 0, 2000, 2000))
        leftCanvas.pack(side=LEFT, fill=BOTH, expand=True)

        # create a scrollbar for the canvas
        leftScrollY = ttk.Scrollbar(leftFrame, orient=VERTICAL, command=leftCanvas.yview)
        leftScrollY.pack(side=LEFT, fill=Y)

        # configure the canvas to use the scrollbar
        leftCanvas.configure(yscrollcommand=leftScrollY.set)

        # bind the canvas to the scrollbars
        leftScrollY.configure(command=leftCanvas.yview)

        leftImageFrame = Frame(leftCanvas, bg='white')
        leftCanvas.create_window((0,0), window=leftImageFrame, anchor='nw')
        
        imagesPerRow = 6
        leftFrameRow = 0
        resultArray, metrics = self.analysisCNN()
        leftPhotoimages = []

        for i in range(len(resultArray)):
            if i % imagesPerRow == 0:
                leftFrameRow = leftFrameRow + 2
                leftFrameLabelRow = leftFrameRow + 1
                
            img_path = resultArray[i][0]
            image1 = Image.open(img_path)
            image1 = image1.resize((80, 80), resample=Image.Resampling.LANCZOS)
            photoimage = ImageTk.PhotoImage(image1)
            leftPhotoimages.append(photoimage)  # store the PhotoImage object in the list
            l1 = Label(leftImageFrame, image=photoimage, cursor="hand2")
            l1.image = photoimage  # keep a reference to the PhotoImage object
            l1.grid(row= leftFrameRow, column=i % imagesPerRow, padx=5, pady = 5)
            l11 = Label(leftImageFrame, text=f"Predicted: {resultArray[i][1]}\nActual: {resultArray[i][2]}", font=("times new roman", 12))
            l11.grid(row= leftFrameLabelRow, column=i % imagesPerRow, padx=5, pady=5)
            
        
        # Get the evaluation metrics
        cnnTP = metrics[1]
        cnnTN = metrics[2]
        cnnFP = metrics[3]
        cnnFN = metrics[4]
        cnnAccuracy = metrics[5]
        cnnPrecision = metrics[6]
        cnnRecall = metrics[7]
        cnnF1 = metrics[8]


        # Create a new label to display the metrics
        metricsLabel = Label(leftImageFrame, text=f"TP: {cnnTP}  \n  FP: {cnnFP}  \n  TN: {cnnTN}  \n  FN: {cnnFN}\nAccuracy: {cnnAccuracy}\nPrecision: {cnnPrecision}\nRecall: {cnnRecall}\nF1: {cnnF1}", font=("times new roman", 20), bd=2, relief="solid", bg="white", fg="black")
        metricsLabel.grid(row=leftFrameRow + 3, column=0, columnspan=imagesPerRow, padx=5, pady=30, sticky="w")      
# =========================================================================================================================================        
# =========================================================================================================================================        
        # adding right frame 
        
        rightFrame = LabelFrame(bgFrame, bd=3,relief = RIDGE, bg='white', fg="gray",text="Result with LBPH", font=("times new roman",30,"bold"))
        rightFrame.place(x=frameWidth + 30, y= 70, width= frameWidth, height= frameHeight)
        
        # create a canvas inside the labelFrame for scrollable content
        rightCanvas = Canvas(rightFrame, bg='white', scrollregion=(0, 0, 2000, 2000))
        rightCanvas.pack(side=LEFT, fill=BOTH, expand=True)

        # create a scrollbar for the canvas
        rightScrollY = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=rightCanvas.yview)
        rightScrollY.pack(side=LEFT, fill=Y)

        # configure the canvas to use the scrollbar
        rightCanvas.configure(yscrollcommand=rightScrollY.set)

        # bind the canvas to the scrollbars
        rightScrollY.configure(command=rightCanvas.yview)

        rightImageFrame = Frame(rightCanvas, bg='white')
        rightCanvas.create_window((0,0), window=rightImageFrame, anchor='nw')
        
        rightFrameRow = 0
        resultArray, metrics = self.analysisLBPH()
        rightPhotoimages = []
        
        for i in range(len(resultArray)):
            if i % imagesPerRow == 0:
                rightFrameRow = rightFrameRow + 2
                rightFrameLabelRow = rightFrameRow + 1
                
            img_path = resultArray[i][0]
            image1 = Image.open(img_path)
            image1 = image1.resize((80, 80), resample=Image.Resampling.LANCZOS)
            photoimage = ImageTk.PhotoImage(image1)
            rightPhotoimages.append(photoimage)  # store the PhotoImage object in the list
            l1 = Label(rightImageFrame, image=photoimage, cursor="hand2")
            l1.image = photoimage  # keep a reference to the PhotoImage object
            l1.grid(row= rightFrameRow, column=i % imagesPerRow, padx=5, pady = 5)
            l11 = Label(rightImageFrame, text=f"Predicted: {resultArray[i][1]}\nActual: {resultArray[i][2]}", font=("times new roman", 12))
            l11.grid(row= rightFrameLabelRow, column=i % imagesPerRow, padx=5, pady=5)
        
        # Get the evaluation metrics
        LbphTP = metrics[1]
        LbphTN = metrics[2]
        LbphFP = metrics[3]
        LbphFN = metrics[4]
        LbphAccuracy = metrics[5]
        LbphPrecision = metrics[6]
        LbphRecall = metrics[7]
        LbphF1 = metrics[8]

        # Create a new label to display the metrics
        rightMetricsLabel = Label(rightImageFrame, text=f"TP: {LbphTP} \n  FP: {LbphFP}  \n  TN: {LbphTN}  \n  FN: {LbphFN}\nAccuracy: {LbphAccuracy}\nPrecision: {LbphPrecision}\nRecall: {LbphRecall}\nF1: {LbphF1}", font=("times new roman", 20), bd=2, relief="solid", bg="white", fg="black")
        rightMetricsLabel.grid(row=rightFrameRow + 3, column=0, columnspan=imagesPerRow, padx=5, pady=30, sticky="w") 
                
    #   Functions ========================================================================================================================================================    
    def analysisCNN(self):
        model = load_model('myModel.h5')
        with open('MapCnn.pkl', 'rb') as f:
            resultMap = pickle.load(f)

        # Initialize the true labels and predicted labels
        true_labels = []
        pred_labels = []
        results = []

        # Loop over all the folders and images in the TestImages directory
        test_image_dir = 'TestImages'
        for username in os.listdir(test_image_dir):
            user_dir = os.path.join(test_image_dir, username)
            if os.path.isdir(user_dir):
                for filename in os.listdir(user_dir):
                    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                        # Load the image and predict its label
                        image_path = os.path.join(user_dir, filename)
                        test_image = image.load_img(image_path, target_size=(224, 224))
                        test_image = image.img_to_array(test_image)
                        test_image = np.expand_dims(test_image, axis=0)
                        pred = model.predict(test_image, verbose=0)
                        predId = np.argmax(pred)
                        pred_label = resultMap[int(predId)]
                        true_label = username

                        # Add the true label and predicted label to the lists
                        true_labels.append(true_label)
                        pred_labels.append(pred_label)
                        
                        # Add the result to the results list
                        result = [image_path, pred_label, true_label]
                        results.append(result)

        metrics = EvaluateModel.evaluate_predictions(true_labels, pred_labels)
        # print(metrics)
        
        return results, metrics
    
    def analysisLBPH(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('LbphModel.yml')
        
        # Load the label map
        with open('MapLbph.pkl', 'rb') as f:
            resultMap = pickle.load(f)
            
        # Initialize the true labels and predicted labels
        true_labels = []
        pred_labels = []
        results = []
        
        # Loop over all the folders and images in the TestImages directory
        test_image_dir = 'TestImages'
        for username in os.listdir(test_image_dir):
            user_dir = os.path.join(test_image_dir, username)
            if os.path.isdir(user_dir):
                for filename in os.listdir(user_dir):
                    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                        # Load the image and predict its label
                        image_path = os.path.join(user_dir, filename)
                        img = Image.open(image_path).convert('RGB')
                        gray = img.convert('L')  # convert to grayscale

                        label_id, pred = recognizer.predict(np.array(gray))
                        name = next(name for name, id in resultMap.items() if id == label_id)

                        pred_label = name
                        true_label = username

                        # Add the true label and predicted label to the lists
                        true_labels.append(true_label)
                        pred_labels.append(pred_label)

                        # Add the result to the results list
                        result = [image_path, pred_label, true_label]
                        results.append(result)
        metrics = EvaluateModel.evaluate_predictions(true_labels, pred_labels)
        return results, metrics

        
if __name__ == "__main__":
    root = Tk()
    obj = ComparisionScreen(root)
    root.mainloop()
