import PyQt5
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import time
import Assistant
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QDate, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import CreateDataset
from FridayGUI import Ui_FridayGUI

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    def run(self):
        self.recog()
        Assistant.TaskExecution()

    def recog(self):
        cnt=0
        face_classifier = cv2.CascadeClassifier('.\haarcascade_frontalface_default.xml')
        model = cv2.face.LBPHFaceRecognizer_create()
        # Reading the trained model file
        model.read("TrainedModel.yml")

        def face_detector(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            arr = np.array(faces)
            if np.array_equal(arr, []):
                return img, []

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi = img[y:y + h, x:x + w]
                roi = cv2.resize(roi, (200, 200))
            return img, roi

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, frame = cap.read()
            image, face = face_detector(frame)
            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                # "results" has a tuple containing the label and the confidence value
                results = model.predict(face)  # Passing face to the prediction model

                if results[1] < 500:
                    confidence = int(100 * (1 - (results[1]) / 400))

                if confidence > 70:
                    if cnt==0:
                        Assistant.speak("Authenticating...")
                        cnt+=1
                    self.query = Assistant.takeCommand().lower()
                    if 'wake up' in self.query or 'wake up friday' in self.query or 'friday' in self.query or 'fri day' in self.query:
                        Assistant.wishMe()
                        Assistant.TaskExecution()
            except:
                pass


class MainThread_2(QThread):
    def __init__(self):
        super(MainThread_2,self).__init__()
    def run(self):
        self.trainingModel()

    def trainingModel(self):
        CreateDataset.datasetCreation()
        # Get the training data which is previously made
        data_path = 'Dataset/'
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

        # Arrays for training data and labels
        Training_Data, Labels = [], []

        # Open training images in the datapath and Create a numpy array for training data
        for i, files in enumerate(onlyfiles):
            image_path = data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)

        # Create a numpy array for training data and labels
        Labels = np.asarray(Labels, dtype=np.int32)
        # Initialize face recognizer model
        model = cv2.face.LBPHFaceRecognizer_create()

        print(Labels)
        print("Training The Model...")

        # Train The model
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        model.write("TrainedModel.yml")
        print("Model trained sucessefully")
        print("TrainedModel.yml Created in the directory")

startExecution = MainThread()
startExecution_2=MainThread_2()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_FridayGUI()
        self.ui.setupUi(self)

        self.ui.movie = PyQt5.QtGui.QMovie("GUI Resources/BG.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = PyQt5.QtGui.QMovie("GUI Resources/Initializing.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = PyQt5.QtGui.QMovie("GUI Resources/Compass.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = PyQt5.QtGui.QMovie("GUI Resources/Loading.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.ui.pushButton.clicked.connect(self.trainTask)
        self.ui.pushButton_2.clicked.connect(self.startTask)

    def startTask(self):
        startExecution.start()

    def trainTask(self):
        startExecution_2.start()

    def showTime(self):
        current_Date=QDate.currentDate()
        label_time=time.strftime("%I:%M:%S %p")
        label_date=current_Date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app =QApplication(sys.argv)
main = Main()
main.show()
sys.exit(app.exec_())
