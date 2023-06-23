import socket
import struct
import cv2
import numpy as np
import time
import sys

def recvall(sock, count):
    buf = b''  # buf是一个byte类型
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
    
def SendVideo():
    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    address = ('10.106.78.225', 8004)
    try:
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 开启连接
        print("start")
        sock.connect(address)
        print("connect")
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    # 建立图像读取对象pr
    # capture = cv2.VideoCapture('./test.mp4')
    capture = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink", cv2.CAP_GSTREAMER)
    print ("CSI camera capture get FPS : ",capture.get(cv2.CAP_PROP_FPS))
    print(capture.isOpened())
    # capture.set(3, 640)
    # capture.set(4, 480)
    # 读取一帧图像，读取成功:ret=1 frame=读取到的一帧图像；读取失败:ret=0
    ret, frame = capture.read()
    # 压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
    i = 0  #模拟识别结果
    while ret:
        boxInfoStr = str(i)
        i += 1
        t1 = time.time()
        # 停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
        # time.sleep(0.1)
        # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
        # '.jpg'表示将图片按照jpg格式编码。
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # 建立矩阵
        data = np.array(imgencode)
        # 将numpy矩阵转换成字符形式，以便在网络中传输
        stringData = data.tostring()
        print(f"stringData {len(stringData)}")
        fhead = struct.pack('qq',
                    len(stringData),
                    i
                    )
        sock.send(fhead)
        # 发送数据
        sock.send(stringData)
        #读取服务器返回值
        # receive = sock.recv(29)
        # print(str(receive,encoding="utf-8"))
        # 读取下一帧图片
        ret, frame = capture.read()
        # cv2.imshow('show', frame)
        if cv2.waitKey(10) == 27:
            break

        print('process time = ',time.time() - t1)
    sock.close()


if __name__ == "__main__":
    SendVideo()