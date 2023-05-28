import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
import pytesseract
from PIL import Image
from imageprocessing import *
from mainwindow import MainWindow
from pytesseract import Output

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    

    window = MainWindow()
    

    window.preprocess_image = preprocess_image
    

    window.pytesseract = pytesseract
    
    window.show()
    sys.exit(app.exec_())

