from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from PIL import Image
import pytesseract
from imageprocessing import preprocess_image, convert_image_to_pixmap
import re
from docx import Document

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Scanner App")
        self.setGeometry(100, 100, 500, 800)
        self.preprocessed_image = None
        self.file_path = ""
        self.extracted_text = ""

        self.create_main_layout()

    def create_main_layout(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(200, 200)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        browse_button = QPushButton("Insert Image", self)
        browse_button.clicked.connect(self.browse_image)
        browse_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        main_layout.addWidget(browse_button)

        scan_button = QPushButton("Scan Image", self)
        scan_button.clicked.connect(self.scan_image)
        scan_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        main_layout.addWidget(scan_button)

        clear_button = QPushButton("Clear Text", self)
        clear_button.clicked.connect(self.clear_text)
        main_layout.addWidget(clear_button)

        language_label = QLabel("Select Language:", self)
        main_layout.addWidget(language_label)

        self.language_dropdown = QComboBox(self)
        self.language_dropdown.addItems(["eng", "rus"])
        main_layout.addWidget(self.language_dropdown)

        self.autodetect_language_checkbox = QCheckBox("Auto Detect Language")
        self.autodetect_language_checkbox.stateChanged.connect(self.update_language_selection)
        main_layout.addWidget(self.autodetect_language_checkbox)


        self.filter_dropdown = QComboBox(self)
        self.filter_dropdown.addItems(["No Filter", "Black and White Filter"])
        self.filter_dropdown.currentIndexChanged.connect(self.apply_filter)
        main_layout.addWidget(self.filter_dropdown)

        save_button = QPushButton("Save Text", self)
        save_button.clicked.connect(self.save_text)
        main_layout.addWidget(save_button)

        save_format_label = QLabel("Select Save Format:", self)
        main_layout.addWidget(save_format_label)

        self.save_format_dropdown = QComboBox(self)
        self.save_format_dropdown.addItems(["Text File (.txt)", "Word Document (.docx)"])
        main_layout.addWidget(self.save_format_dropdown)

        checkbox_layout = QHBoxLayout()
        main_layout.addLayout(checkbox_layout)

        self.display_text_checkbox = QCheckBox("Text")
        checkbox_layout.addWidget(self.display_text_checkbox)

        self.display_email_checkbox = QCheckBox("Email")
        checkbox_layout.addWidget(self.display_email_checkbox)

        self.display_dates_checkbox = QCheckBox("Dates")
        checkbox_layout.addWidget(self.display_dates_checkbox)

        self.display_phone_numbers_checkbox = QCheckBox("Phone Numbers")
        checkbox_layout.addWidget(self.display_phone_numbers_checkbox)

        self.text_entry = QTextEdit(self)
        self.text_entry.setReadOnly(True)
        main_layout.addWidget(self.text_entry)


    def browse_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(filter="Image Files (*.jpg *.jpeg *.png)")
        if file_path:
            self.file_path = file_path
            image = QPixmap(file_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(image)
            self.clear_text()

    def scan_image(self):
        if self.file_path:
            img = self.preprocessed_image if self.filter_dropdown.currentText() == "Black and White Filter" else Image.open(self.file_path)
            if self.autodetect_language_checkbox.isChecked():
                languages = '+'.join([self.language_dropdown.itemText(i) for i in range(self.language_dropdown.count())])
            else:
                languages = self.language_dropdown.currentText()
            extracted_text = pytesseract.image_to_string(img, lang=languages)
            filtered_text = self.filter_text(extracted_text)
            self.text_entry.setPlainText(filtered_text)
    def update_language_selection(self, state):
        enabled = state != Qt.Checked
        self.language_dropdown.setEnabled(enabled)

    def apply_filter(self):
        if self.file_path:
            if self.filter_dropdown.currentText() == "Black and White Filter":
                img = Image.open(self.file_path)
                preprocessed_img = preprocess_image(img)
                preprocessed_pixmap = convert_image_to_pixmap(preprocessed_img)
                scaled_pixmap = preprocessed_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)
                self.preprocessed_image = preprocessed_img
            else:
                image = QPixmap(self.file_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(image)

    def clear_text(self):
        self.text_entry.clear()

    def save_text(self):
        file_dialog = QFileDialog(self)
        if self.save_format_dropdown.currentText() == "Text File (.txt)":
            file_path, _ = file_dialog.getSaveFileName(filter="Text Files (*.txt)")
        elif self.save_format_dropdown.currentText() == "Word Document (.docx)":
            file_path, _ = file_dialog.getSaveFileName(filter="Text Files (*.docx)")
        if file_path:
            if file_path.endswith(".txt"):
                with open(file_path, "w") as file:
                    file.write(self.text_entry.toPlainText())
            elif file_path.endswith(".docx"):
                document = Document()
                document.add_paragraph(self.text_entry.toPlainText())
                document.save(file_path)

    def filter_text(self, text):
        filtered_text = ""

        if self.display_text_checkbox.isChecked():
            filtered_text += "Text:\n"
            filtered_text += text

        if self.display_email_checkbox.isChecked():
            email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            if email_addresses:
                filtered_text += "\n\nEmail Addresses:\n"
                filtered_text += "\n".join(email_addresses)

        if self.display_dates_checkbox.isChecked():
            dates = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', text)
            if dates:
                filtered_text += "\n\nDates:\n"
                filtered_text += "\n".join(dates)

        if self.display_phone_numbers_checkbox.isChecked():
            phone_numbers = re.findall(r'(\+?\d{1,4}?\s?\(?\d{1,3}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9})', text)
            if phone_numbers:
                filtered_text += "\n\nPhone Numbers:\n"
                valid_phone_numbers = []
                for phone_number in phone_numbers:
                    if self.is_valid_phone_number(phone_number):
                        valid_phone_numbers.append(phone_number)
                if valid_phone_numbers:
                    filtered_text += "\n".join(valid_phone_numbers)

        if not filtered_text:
            filtered_text = "Nothing Found"

        return filtered_text

    def is_valid_phone_number(self, phone_number):
        # Remove all non-digit characters from the phone number
        digits = re.sub(r'\D', '', phone_number)

        # Check the length of the phone number
        if len(digits) < 10 or len(digits) > 15:
            return False

        # Check the phone number format
        if not re.match(r'^\+?\d{1,4}?\s?\(?\d{1,3}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}$', phone_number):
            return False

        # Additional checks if necessary
        # ...

        return True
