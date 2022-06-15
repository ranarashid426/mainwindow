
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource



from out_window import Ui_OutputDialog


class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        self.logolabel = QtWidgets.QLabel(Dialog)
        self.logolabel.setGeometry(QtCore.QRect(0, 0, 501, 151))
        self.logolabel.setText("")
        self.logolabel.setPixmap(QtGui.QPixmap("logo.png"))
        self.logolabel.setObjectName("logolabel")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("mainwindow", "mainwindow"))
        self.dataset.setText(_translate("mainwindow", "DataSET For new Student"))
        self.dataset.clicked.connect(self.newUser)
        
    
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("mainwindow.ui", self)
        



        self.runButton.clicked.connect(self.runSlot)
        
        self.dataset.clicked.connect(self.dataSlot)

        
        

        self._new_window = None
        self.Videocapture_ = None
    

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.Videocapture_ = "0"

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        self.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

   

 
    @pyqtSlot()
    def dataSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        self.hide()  # hide the main window
        self.dataWindow_()  # Create and open new output window
    
    def dataWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.dataset(self.Videocapture_)

   

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()

        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")
  
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
