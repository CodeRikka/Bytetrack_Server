import sys
import socket
import struct
import numpy
import cv2
from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtGui import QImage, QPixmap

import random
import struct

from ImageObject import ImageObject

def imageCv2Qt(image):
    height, width, bytesPerComponent = image.shape
    bytesPerLine = 3 * width
    cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
    QImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(QImg)
    return pixmap


class CaptureThread(QThread):
    signal_image = Signal(QPixmap)
    def __init__(self):
        super(CaptureThread, self).__init__()
        self.qmutex = QMutex()  # 进行锁
        self.Threadopen = True
        self.img_sock = None
        
    def InitPort(self, ip, imgport):
        self.ip = ip
        self.imgport = imgport
    
    def InitSocket(self):
        img_address = (self.ip, self.imgport)
        if self.img_sock == None:
            try:
                self.img_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.img_sock.settimeout(3)
                # 开启连接
                print("img socket start")
                self.img_sock.connect(img_address)
                print("img socket connected")
            except (socket.error, socket.timeout) as msg:
                print(msg)
                # sys.exit(1)

    
    def recv_all(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def run(self):
        self.InitSocket()
        
        while self.Threadopen:
            
            # self.qmutex.lock()
            image_data_len = None
            while self.Threadopen:
                buf = self.img_sock.recv(struct.calcsize('I'))
                image_data_len = struct.unpack('I', buf)[0]
                if (image_data_len == 0):
                    continue
                else:
                    break
                
            image_data = self.recv_all(self.img_sock, image_data_len) # ??????
            # print(image_data)
            data = numpy.frombuffer(image_data, dtype='uint8')
            tmp = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 解码处理，返回mat图片
            img = cv2.resize(tmp, (1280, 720))
            # self.qmutex.unlock()
            # cv2.imshow("test", img)
            # cv2.imwrite("E://test.jpeg", img)
            buf = self.img_sock.recv(struct.calcsize('I'))
            num_boxes = struct.unpack('I', buf)[0]
            boxes = [] # tlwhs
            box_data_length = struct.calcsize('ffff')
            for _ in range(num_boxes):
                box_data = self.img_sock.recv(box_data_length)
                box = struct.unpack('ffff', box_data)
                boxes.append(box)
            ids = []
            for _ in range(num_boxes):
                id_data = self.img_sock.recv(struct.calcsize('I'))
                id = struct.unpack('I', id_data)[0]
                ids.append(id)
                
            scores = []
            for _ in range(num_boxes):
                score_data = self.img_sock.recv(struct.calcsize('f'))
                score = struct.unpack('f', score_data)[0]
                scores.append(score)
                
            labels = []
            for _ in range(num_boxes):
                label_data = self.img_sock.recv(struct.calcsize('f'))
                label = struct.unpack('f', label_data)[0]
                labels.append(label)
            
            pixmap = imageCv2Qt(img)
            # image = ImageObject(img, boxes, ids, scores, labels)
            self.signal_image.emit(pixmap)
            
            
            
            