from PIL import ImageOps
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
def preprocess_image(image):
    # ���������� ������������� ��� ��������� �������� OCR
    image = image.convert("L")  # ����������� � ������� ������
    image = ImageOps.invert(image)  # �������������� ������ (������ ���������� ����� � ��������)
    image = image.point(lambda x: 0 if x < 128 else 255, "1")  # ��������� ���������

    return image

def convert_image_to_pixmap(image):
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")
    qimage = QtGui.QImage(data, image.size[0], image.size[1], QtGui.QImage.Format_RGBA8888)
    pixmap = QtGui.QPixmap.fromImage(qimage)

    return pixmap
