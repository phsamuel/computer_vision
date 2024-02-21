import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot as pyQtSlot
from PyQt5.QtCore import QTimer,QDateTime,Qt,QRect, QThread
from PyQt5.QtGui import QPainter, QPen, QFont, QImage

from PyQt5.QtGui import QPixmap

import cv2
import time
import os


from minimal import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.cap = cv2.VideoCapture(0)
        self.movie_thread = MovieThread(self.cap, self.label)
        self.movie_thread.start()

            # print(self.bibs)

    @pyQtSlot()
    def on_pushButton_pressed(self):
        print('hello')

        self.movie_thread = MovieThread(self.cap, self.label)
        self.movie_thread.start()

        # os.system('xclip -selection clipboard -t image/png -o > dummy.png')
        # pixmap = QPixmap('dummy.png')
        # self.label.setPixmap(pixmap)


class MovieThread(QThread):
    def __init__(self, cap, label):
        super().__init__()
        self.cap = cap
        self.label = label

    def run(self):
        while True:
            ret,cvImg=self.cap.read()
            height, width, channel = cvImg.shape
            bytesPerLine = 3 * width
            qimg = QImage(cv2.cvtColor(cvImg,cv2.COLOR_BGR2RGB), width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            # pixmap = QPixmap('cat.png')
            self.label.setPixmap(pixmap)
            print('run')
            time.sleep(0.05)

        # self.camera.acquire_movie(200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

