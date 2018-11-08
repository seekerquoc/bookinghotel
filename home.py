import sys
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtCore
from datetime import datetime
import pyowm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor,QPixmap,QIcon,QMovie,QImage
from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt
from urllib import request
    
uifile_1 = 'home.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'plate.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)
        
class HomePage(base_1, form_1):
    def __init__(self):
        super(base_1,self).__init__()
        self.setupUi(self)
        #self.showFullScreen()

        self.btn_start = ClickLabel(self)
        self.movie = QMovie("down.png")
        self.btn_start.setMovie(self.movie)
        self.btn_start.setGeometry(25,310,672,114)
        self.movie.start()
        self.btn_start.clicked.connect(self.change)
        
        self._heightMask = self.height()
        self.animation = QPropertyAnimation(self, b"heightPercentage")
        self.animation.setDuration(1000)
        self.animation.setStartValue(self.height())
        self.animation.setEndValue(-1)
        self.animation.finished.connect(self.close)
        self.isStarted = False
        
    def change(self):
        self.main = MainPage()
        self.main.show()
        self.close()
        
    @pyqtProperty(int)
    def heightMask(self):
        return self._heightMask

    @heightMask.setter
    def heightPercentage(self, value):
        self._heightMask = value
        rect = QRect(0, 0, self.width(), self.heightMask)
        self.setMask(QRegion(rect))

    def closeEvent(self, event):
        if not self.isStarted:
            self.animation.start()
            self.isStarted = True
            event.ignore()
        else:   
            self.closeEvent(self, event)   

class MainPage(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = HomePage()
    home.show()
    sys.exit(app.exec_())
