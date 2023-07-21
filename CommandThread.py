import sys
import socket
import struct
import numpy
import cv2
from PySide6.QtCore import QThread, Signal, QMutex

import struct


class CommandThread(QThread):
    def __init__(self):
        super(CommandThread, self).__init__()
        self.qmutex = QMutex()  # 进行锁
        self.Threadopen = True
        self.cmd_sock = None
        self.class_list = []
        
    def InitPort(self, ip, cmdport):
        self.ip = ip
        self.cmdport = cmdport
    
    def InitSocket(self):
        cmd_address = (self.ip, self.cmdport)
        try:
            self.cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cmd_sock.settimeout(3)
            # 开启连接
            print("cmd socket start")
            self.cmd_sock.connect(cmd_address)
            print("cmd socket connected")
            
            # receive classes 
            buf = self.cmd_sock.recv(struct.calcsize('I'))
            class_len = struct.unpack('I', buf)[0]
            print(class_len)
            SEPERATOR = "\n"
            class_list = self.cmd_sock.recv(class_len).decode().split(SEPERATOR)
            print(class_list)
            
            
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
    
    def send_command(self, cmd):
        print(cmd)
        self.cmd_sock.send(cmd.encode())