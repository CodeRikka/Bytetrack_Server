import sys
import socket
import struct
import numpy
import cv2
from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtGui import QImage, QPixmap

import random
import struct

class ThreadCapture(QThread):
    # 定义信号，用于传输图像
    signal_image = Signal(QPixmap)
    def __init__(self):
        super(ThreadCapture, self).__init__()
        self.qmutex = QMutex()  # 进行锁
        self.Threadopen = True

    def recv_all(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def imageCv2Qt(self, image):
        height, width, bytesPerComponent = image.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
        QImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        return pixmap
    
    def deal_data(self, addr):
        print("Accept new connection from {0}".format(addr))
        while self.Threadopen:
            
            # 读取图像是，锁住线程
            # self.qmutex.lock()
            
            buf = self.conn.recv(struct.calcsize('qq'))
            print(buf, type(buf))
            data_len, idx = struct.unpack('qq', buf)
            print(f"data_len = {data_len}, idx = {idx}")
            print(type(data_len), type(idx))
            stringData = self.recv_all(self.conn, data_len)
            # self.qmutex.unlock()
            
            
            # stringData = conn.recv(data_len)
            # print(stringData)
            data = numpy.frombuffer(stringData, dtype='uint8')
            tmp = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 解码处理，返回mat图片
            img = cv2.resize(tmp, (1280, 720))
            pixmap = self.imageCv2Qt(img)
            self.signal_image.emit(pixmap)
            self.sendFlag("OK")
            # self.videoLabel.setPixmap(pixmap)
            
            
            # cv2.imshow('SERVER', img)
            # if cv2.waitKey(1) == 27:
            #     break
        self.conn.close()
    
    def sendFlag(self, flag):
        self.conn.send(flag.encode())
    def run(self):
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('10.106.78.225', 8004))
            self.sock.listen(1)
        
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        print("Waiting...")
        # self.cap = cv2.VideoCapture(self.cameraNum, cv2.CAP_DSHOW) # cv2.CAP_DSHOW 可以消除警告
        
        while True:
            print('thread id:', QThread.currentThread())
            # 读取图像是，锁住线程
            # self.qmutex.lock()
            
            # ret, self.image = self.cap.read()
            print(self.sock)
            self.conn, addr = self.sock.accept() ######################### 这里出了问题，第二次按按钮，这一步执行不了，会卡住
            print("self.conn = ", self.conn)
            
            # self.qmutex.unlock()

            
            self.deal_data(addr)
            # if ret:
            #     # 处理图像
            #     self.dealImage()
            #     # 处理图像数据，符合算法要求后传入模型，等待返回结果
            #     if self.algDetectFlag:
            #         print('start alg detect')
            #         cv2.rectangle(self.image, (100, 100), (300, 300),
            #                       (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),)

            #     # 转换为qt的图像格式
            #     pixmap = self.imageCv2Qt(self.image)
            #     self.signal_image.emit(pixmap)

    def dealImage(self):
        self.image = cv2.resize(self.image, (400, 400))
        height, width, depth = self.image.shape
        # cv2.putText(self.image, 'height-{}:width-{}'.format(height, width), (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255 ,0))


    # 转换为qt的图像格式
    def imageCv2Qt(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, depth = rgb.shape
        bytesPerLine = width * depth
        qrgb = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qrgb)

        return pixmap
    
    def closeThread(self):
        self.sendFlag("Close")
        self.Threadopen = False
        self.conn.close()
        self.sock.close()