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


import requests

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
    
    
    def submit_Post(self):
        url = "http://10.105.114.11:25000/export"  # 应用程序的 URL
        
        response = requests.post(url)  # 发送 POST 请求

        if response.status_code == 200:
            print("Send Post Success!")
        else:
            print("Request failed with status code:", response.status_code)
    
    def actionPushButton(self):
        if self.PushButton.text() == self.openThreadText:
            self.submit_Post()
            # 创建线程
            self.threadCapture = ThreadCapture()
            self.threadCapture.Threadopen = True
            self.threadCapture.signal_image.connect(self.showImage)
            self.threadCapture.start()
            self.PushButton.setText(self.closeThreadText)
        else:
            self.threadCapture.closeThread()
            self.threadCapture.terminate()
            self.threadCapture.quit()
            self.PushButton.setText(self.openThreadText)
        
    def showImage(self, image):
        self.imageScene.addPixmap(image)
    
if __name__ == "__main__":
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
