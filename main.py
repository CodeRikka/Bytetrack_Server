# This Python file uses the following encoding: utf-8

import sys
import cv2
import socket
import struct
import numpy
import threading
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QWidget, QGraphicsScene
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QScreen, QImage, QPixmap
from Ui_server import Ui_Form
from qframelesswindow import FramelessWindow
from qfluentwidgets import setThemeColor, Theme
from ThreadCapture import ThreadCapture
class MainWindow(FramelessWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')
        
        # 窗口居中
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        # self.ReceiveVideo()
        # self.videoLabel.setPixmap(QPixmap("./resource/images/background.jpg"))
        self.PushButton.clicked.connect(self.actionPushButton)
        self.imageScene = QGraphicsScene()
        self.imageView.setScene(self.imageScene)
        
        self.openThreadText = "Select Camera"
        self.closeThreadText = "Close Thread"
        self.PushButton.setText(self.openThreadText)
        
    def actionPushButton(self):
        if self.PushButton.text() == self.openThreadText:
            # 创建线程
            self.threadCapture = ThreadCapture()
            self.threadCapture.signal_image.connect(self.showImage)
            self.threadCapture.start()
            self.PushButton.setText(self.closeThreadText)
        else:
            self.threadCapture.terminate()
            self.threadCapture.quit()
            self.PushButton.setText(self.openThreadText)
        
    def showImage(self, image):
        self.imageScene.addPixmap(image)
        self.imageScene
    
    # @staticmethod
    # def recv_all(sock, count):
    #     buf = b''
    #     while count:
    #         newbuf = sock.recv(count)
    #         if not newbuf: return None
    #         buf += newbuf
    #         count -= len(newbuf)
    #     return buf
    # def deal_data(self, conn, addr):
    #     print("Accept new connection from {0}".format(addr))
    #     while True:
    #         buf = conn.recv(struct.calcsize('qq'))
    #         print(buf, type(buf))
    #         data_len, idx = struct.unpack('qq', buf)
    #         print(f"data_len = {data_len}, idx = {idx}")
    #         print(type(data_len), type(idx))
    #         stringData = MainWindow.recv_all(conn, data_len)
    #         # stringData = conn.recv(data_len)
    #         # print(stringData)
    #         data = numpy.frombuffer(stringData, dtype='uint8')
    #         tmp = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 解码处理，返回mat图片
    #         img = cv2.resize(tmp, (1280, 720))
    #         pixmap = MainWindow.imageCv2Qt(img)
    #         self.videoLabel.setPixmap(pixmap)
    #         # cv2.imshow('SERVER', img)
    #         # if cv2.waitKey(1) == 27:
    #         #     break
    #     conn.close()
    #     cv2.destroyAllWindows()

    # def ReceiveVideo(self):
    #     try:
    #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         s.bind(('10.106.78.225', 8004))
    #         s.listen(1)
        
    #     except socket.error as msg:
    #         print(msg)
    #         sys.exit(1)
    #     print("Waiting...")
    #     while True:
    #         conn, addr = s.accept()
    #         self.deal_data(conn, addr)
            
    # @staticmethod
    # def imageCv2Qt(image):
    #     height, width, bytesPerComponent = image.shape
    #     bytesPerLine = 3 * width
    #     cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
    #     QImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(QImg)
    #     return pixmap
        
if __name__ == "__main__":
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
