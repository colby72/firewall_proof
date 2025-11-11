from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.company import *


class DialogEditStatus(QDialog):
    def __init__(self, main_window, company, status):
        super().__init__()
        self.main_window = main_window
        self.company = company
        self.status = status
        self.setWindowTitle("Edit Status")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Label : "), 0, 0)
        self.status_label = QLineEdit()
        self.status_label.setMaxLength(10)
        self.status_label.setText(self.status.label)
        self.status_label.setPlaceholderText("Status label ...")
        layout.addWidget(self.status_label, 0, 1, 1, 2)
        layout.addWidget(QLabel("Color : "), 1, 0)
        self.html_color = QLabel(self.status.color)
        layout.addWidget(self.html_color, 1, 1)
        self.color_button = QPushButton("Edit color")
        self.color_button.clicked.connect(self.get_color)
        layout.addWidget(self.color_button, 1, 2)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 4, 1)

    def get_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.html_color.setText(color.name())

    def when_ok(self):
        status_label = self.status_label.text()
        color = self.html_color.text()
        self.status.set_label(status_label)
        self.status.set_color(color)
        self.close()
    
    def when_cancel(self):
        self.close()