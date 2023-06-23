# This Python file uses the following encoding: utf-8

import sys
import cv2
import socket
import struct
import numpy

from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout

def recv_all(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
def deal_data(conn, addr):
    print("Accept new connection from {0}".format(addr))
    while True:
        buf = conn.recv(struct.calcsize('qq'))
        print(buf, type(buf))
        data_len, idx = struct.unpack('qq', buf)
        print(f"data_len = {data_len}, idx = {idx}")
        print(type(data_len), type(idx))
        stringData = recv_all(conn, data_len)
        # stringData = conn.recv(data_len)
        # print(stringData)
        data = numpy.frombuffer(stringData, dtype='uint8')
        tmp = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 解码处理，返回mat图片
        img = cv2.resize(tmp, (1280, 720))
        cv2.imshow('SERVER', img)
        if cv2.waitKey(1) == 27:
            break
    # conn.close()
    cv2.destroyAllWindows()

def ReceiveVideo():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('10.106.78.225', 8004))
        s.listen(1)
    
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")
    while True:
        conn, addr = s.accept()
        deal_data(conn, addr)

class Widget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.button = QPushButton("ReceiveVideo")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.ReceiveVideo)
    
    def ReceiveVideo(self):
        ReceiveVideo()


if __name__ == "__main__":
    app = QApplication([])
    window = Widget()
    window.show()
    sys.exit(app.exec())
