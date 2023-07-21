import cv2
from PySide6.QtGui import QImage, QPixmap

class ImageObject(object):
    def __init__(self, frame, tlwhs, ids, scores, labels):
        self.frame = frame
        self.tlwhs = tlwhs
        self.ids = ids
        self.scores = scores
        self.labels = labels
    
    def imageCv2Qt(self):
        height, width, bytesPerComponent = self.frame.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        return pixmap
