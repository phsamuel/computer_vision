
import cv2
from canny import Ui_MainWindow
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import time

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.low_th=30
        self.high_th=70
        self.lowSlider.setValue(self.low_th)
        self.highSlider.setValue(self.high_th)
        self.cap=cv2.VideoCapture(0)
        self.movieThread=MovieThread(self.cap,self)
        self.movieThread.start()

    def closeEvent(self, event): 
        self.movieThread.stop()

        event.accept()

    @pyqtSlot(int)
    def on_lowSlider_valueChanged(self,val):
        # print(val)
        # val=min(val,self.high_th)
        self.low_th=val
        # self.lowSlider.setValue(self.low_th)
        if self.low_th > self.high_th:
            self.highSlider.setValue(self.low_th)

    @pyqtSlot(int)
    def on_highSlider_valueChanged(self,val):
        # print(val)
        val=max(val,self.low_th)
        self.high_th=val
        self.highSlider.setValue(self.high_th)

    @pyqtSlot()
    def on_pushButton_pressed(self):
        # self.close()
        # self.movieThread.stop()
        print('toggle')
        self.movieThread.toggle()

class MovieThread(QThread):
    def __init__(self, cap, win):
        super().__init__()
        self.cap = cap
        self.win = win
        self._running = True
        self._pause = False

    def run(self):
        while self._running:
            if not self._pause: 
                ret,cvImg=self.cap.read()
                canny = cv2.Canny(cvImg,self.win.low_th,self.win.high_th)
                height, width, channel = cvImg.shape
                bytesPerLine = 3 * width
                # qimg = QImage(cv2.cvtColor(cvImg,cv2.COLOR_BGR2RGB), width, height, bytesPerLine, QImage.Format_RGB888)
                qimg = QImage(canny, width, height, width, QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(qimg)
                # pixmap = QPixmap('cat.png')
                self.win.label.setPixmap(pixmap)
                # print('run')
                time.sleep(0.05)

    def stop(self):
        self._running = False

    def toggle(self):
        self._pause = not self._pause

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
