
from turtle import back
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QApplication, QDialog
import sys


from PyQt5 import QtCore, QtGui, QtWidgets
from pickle import FRAME
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QDialog
import cv2
from cv2 import VideoCapture
from cv2 import cvtColor
import face_recognition
from matplotlib import image
from matplotlib.pyplot import close, show
import numpy as np
import datetime
from datetime import datetime
import os

# from scipy.misc import face

# from mainwindow import UI_Dialog

# import mainwindow

TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'


class Ui_OutputDialog(QDialog):


    def __init__(self):

        # self.capturing = True
        # self.c = cv2.VideoCapture(0)

        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)
        self.image = None
        self.backBtn.clicked.connect(lambda:self.close())
        # from mainwindow import Ui_Dialog
        self.backBtn.clicked.connect(self.previous)
        # self.dataset.clicked.connect(self.newUser)
    
    
    
        
    def previous(self,camera_name):
        from mainwindow import Ui_Dialog
        self.back = Ui_Dialog()
        self.back.close()
        self.back.show()
        # sys.exit(1)


        

    @pyqtSlot()
    def dataset(self,camera_name):
        # self.timer = QTimer(self)  # Create Timer
        
       
    
        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        def face_crop(img):
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            faces = face_classifier.detectMultiScale(gray,1.3,5)
            
            if faces is ():
                return None
            for (x,y,w,h) in faces:
                cropped_face = img[y:y+h, x:x+w]
            return cropped_face
    
        # newUser = input('Enter New User Name: ')
        def newUser():
            newUser, done1 = QtWidgets.QInputDialog.getText(
			self, 'Input Dialog', 'Enter your newUser:')
            if done1:
			# Showing confirmation message along
			# with information provided by user.
                # self.label.setText('Information stored Successfully\nnewUser: '
                #                     +str(newUser))

                # Hide the pushbutton after inputs provided by the use.
                # self.dataset.hide()
                return newUser
		
        newUser = newUser()
        print(newUser)
            
        if newUser:
            parent_path = 'known_faces/'
            joined = os.path.join(parent_path,newUser)
            os.mkdir(joined)
  
        video_capture = cv2.VideoCapture(0)
        img_id = 0
        while True:
            ret,frame = video_capture.read()
         
            # Capture frame-by-frame
            frame = cv2.flip(frame,1)
            if face_crop(frame) is not None:
                img_id+=1
                face = cv2.resize(face_crop(frame),(200,200))
                file_name_path = f"{joined}/"+str(img_id)+'.jpg'
                cv2.imwrite(file_name_path,face)
                cv2.putText(face, str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX, 2,(0,255,0),2)
    
                qformat = QImage.Format_Indexed8
                if len(face.shape) == 3:
                    if face.shape[2] == 4:
                        qformat =QImage.Format_RGBA888
                    else:
                        qformat = QImage.Format_RGB888
                face = QImage(face, face.shape[1],face.shape[0],qformat)
                face = face.rgbSwapped()
                self.imgLabel.setPixmap(QPixmap.fromImage(face))
                self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)           
    
            if cv2.waitKey(1)==27 or img_id == 40:
                print("Dataset Collection Completed")
                break
                
        cv2.destroyAllWindows()
        video_capture.release()
        


    
            


    


    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        
        else:
            self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        

        
        
        KNOWN_FACES_DIR = 'known_faces'
        if not os.path.exists(KNOWN_FACES_DIR):
            os.mkdir(KNOWN_FACES_DIR)
        # known face encoding and known face name list
        images = []
        self.known_names = []
        self.known_faces = []
        attendance_list = os.listdir(KNOWN_FACES_DIR)
        # print(attendance_list)
        # Start from here
        for name in os.listdir(KNOWN_FACES_DIR):
        
            # Next we load every file of faces of known person
            for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):

                # Load an image
                image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

                # Get 128-dimension face encoding
                # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
                boxes = face_recognition.face_locations(image)
                
                try:
                    encoding = face_recognition.face_encodings(image)[0]
                    self.known_faces.append(encoding)
                    self.known_names.append(name)
                except IndexError as e:
                    print(e)
                    # sys.exit(1)
                # encoding = face_recognition.face_encodings(image,boxes)[0]

                # Append encodings and name
        print('Processing unknown faces...')



    # Below one is working


        
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms
        
        

    def face_rec_(self, frame, known_faces, known_names):
        """
        :param frame: frame from camera
        :param known_faces: known face encoding
        :param known_names: known face names
        :return:
        """
        # csv
        def mark_attendance(name):
            """
            :param name: detected face known or unknown one
            :return:
            """
            with open('Attendance.csv', 'r+') as f:
                
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString}')

        # self.ThreadActive = True
        locations = face_recognition.face_locations(frame, model="hog")
        # locations = face_recognition.face_locations(frame,number_of_times_to_upsample=2, model="hog")
        encodings = face_recognition.face_encodings(frame,locations)
    
        for face_encoding,face_location in zip(encodings,locations):
            results = face_recognition.compare_faces(known_faces,face_encoding,TOLERANCE)
            faceDis = face_recognition.face_distance(known_faces,face_encoding)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
    
            if results[matchIndex]:
                # if faceDis[matchIndex]< 0.50:
                name = known_names[matchIndex].upper()
                y1, x2, y2, x1 = face_location
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                mark_attendance(name)
            else:
                name = 'Unknown'
                y1, x2, y2, x1 = face_location
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            print(name)
                # y1,x2,y2,x1 = face_location
                # y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                # cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                # cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        return frame
   
        

    def update_frame(self):
        ret, self.image = self.capture.read()
   
        self.displayImage(self.image, self.known_faces, self.known_names, 1)

    def displayImage(self, image, known_faces, known_names, window=1):
        """
        :param image: frame from camera
        :param known_faces: known face encoding list
        :param known_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, known_faces, known_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ui = Ui_OutputDialog()
#     ui.show()
#     sys.exit(app.exec_())