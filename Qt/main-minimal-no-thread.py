
import cv2
from minimal import Ui_MainWindow
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
import time

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.low_th=30
        # self.high_th=70
        # self.lowSlider.setValue(self.low_th)
        # self.highSlider.setValue(self.high_th)
        self.cap=cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(33)
        self._running = True

    def update(self):
        if self._running:
            ret,cvImg=self.cap.read()
            # canny = cv2.Canny(cvImg,self.low_th,self.high_th)
            height, width, channel = cvImg.shape
            bytesPerLine = 3 * width
            qimg = QImage(cv2.cvtColor(cvImg,cv2.COLOR_BGR2RGB), width, height, bytesPerLine, QImage.Format_RGB888)
            # qimg = QImage(cvImg, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)

    # @pyqtSlot(int)
    # def on_lowSlider_valueChanged(self,val):
    #     # print(val)
    #     # val=min(val,self.high_th)
    #     self.low_th=val
    #     # self.lowSlider.setValue(self.low_th)
    #     if self.low_th > self.high_th:
    #         self.highSlider.setValue(self.low_th)

    # @pyqtSlot(int)
    # def on_highSlider_valueChanged(self,val):
    #     # print(val)
    #     val=max(val,self.low_th)
    #     self.high_th=val
    #     self.highSlider.setValue(self.high_th)

    @pyqtSlot()
    def on_pushButton_pressed(self):
        print('toggle')
        self._running = not self._running


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
