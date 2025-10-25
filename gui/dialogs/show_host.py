from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class DialogShowHost(QDialog):
    def __init__(self, main_window, host):
        QWidget.__init__(self)
        self.main_window = main_window
        self.host = host
        self.setWindowTitle(f"{self.host.name}")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        layout.addWidget(QLabel(self.host.name), 0, 1)
        layout.addWidget(QLabel("Address : "), 1, 0)
        layout.addWidget(QLabel(self.host.address), 1, 1)
        layout.addWidget(QLabel("Zone : "), 2, 0)
        layout.addWidget(QLabel(self.host.zone.name), 2, 1)
        #layout.setRowStretch(layout.rowCount(), 1)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttons.accepted.connect(self.when_ok)
        layout.addWidget(self.buttons, 3, 1)
    
    def when_ok(self):
        self.close()