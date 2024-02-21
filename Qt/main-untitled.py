from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, QTimer, pyqtSlot
import time

from untitled import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.low_th = 30
        self.high_th = 70
        self.lowSlider.setValue(self.low_th)
        self.highSlider.setValue(self.high_th)
        self.cap = cv2.VideoCapture(2)
        self.running = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)


    def update(self):
        if self.running:
            ret, cvImg = self.cap.read() 
            height, width, channel = cvImg.shape

            canny=cv2.Canny(cvImg,self.low_th,self.high_th)

            bytesPerLine = width 

            qimg = QImage(canny, width, height, bytesPerLine, QImage.Format_Grayscale8)
            
            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)


    @pyqtSlot()
    def on_pushButton_pressed(self):
        self.running = not self.running
        print("pressed")

    @pyqtSlot(int)        
    def on_lowSlider_valueChanged(self,val):
        self.low_th = val
        m,M = min(self.low_th,self.high_th), max(self.low_th,self.high_th)
        self.lowSlider.setValue(m)
        self.highSlider.setValue(M)

    @pyqtSlot(int)        
    def on_highSlider_valueChanged(self,val):
        self.high_th = val
        m,M = min(self.low_th,self.high_th), max(self.low_th,self.high_th)
        self.lowSlider.setValue(m)
        self.highSlider.setValue(M)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
        


# designer         