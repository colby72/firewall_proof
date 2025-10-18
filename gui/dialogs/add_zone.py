from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.zone import *


class DialogAddZone(QDialog):
    def __init__(self, main_window, company):
        super().__init__()
        self.main_window = main_window
        self.company = company
        self.setWindowTitle("Add new Zone")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.zone_name = QLineEdit()
        self.zone_name.setMaxLength(10)
        self.zone_name.setPlaceholderText("Policy name ...")
        layout.addWidget(self.zone_name, 0, 1, 1, 2)
        layout.addWidget(QLabel("Purdue Level : "), 1, 0)
        self.purdue_level = QComboBox()
        self.purdue_level.addItems(['5', '4', '3.5', '3', '2', '1'])
        layout.addWidget(self.purdue_level, 1, 1, 1, 2)
        layout.addWidget(QLabel("Description : "), 2, 0)
        self.zone_desc = QLineEdit()
        self.zone_desc.setMaxLength(60)
        self.zone_desc.setPlaceholderText("Zone description ...")
        layout.addWidget(self.zone_desc, 2, 1, 1, 2)
        layout.addWidget(QLabel("Color : "), 3, 0)
        self.html_color = QLabel("#174EFF")
        layout.addWidget(self.html_color, 3, 1)
        self.color_button = QPushButton("Edit color")
        self.color_button.clicked.connect(self.get_color)
        layout.addWidget(self.color_button, 3, 2)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 4, 1)

    def get_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.html_color.setText(color.name())

    def when_ok(self):
        zone_name = self.zone_name.text()
        purdue_level = self.purdue_level.currentText()
        zone_desc = self.zone_desc.text()
        color = self.html_color.text()
        new_zone = Zone(zone_name, purdue_level, zone_desc, color)
        self.company.add_zone(new_zone)
        self.close()
    
    def when_cancel(self):
        self.close()