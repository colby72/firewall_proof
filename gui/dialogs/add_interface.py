from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class DialogAddInterface(QDialog):
    def __init__(self, main_window, fw):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle("Add new Interface")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.iface_name = QLineEdit()
        self.iface_name.setMaxLength(15)
        self.iface_name.setPlaceholderText("Interface name ...")
        layout.addWidget(self.iface_name, 0, 1)
        layout.addWidget(QLabel("Address : "), 1, 0)
        self.iface_address = QLineEdit()
        self.iface_address.setMaxLength(18)
        self.iface_address.setInputMask('000.000.000.000/00;_')
        layout.addWidget(self.iface_address, 1, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 2, 1)
    
    def when_ok(self):
        iface_name = self.iface_name.text()
        iface_address = self.iface_address.text()
        self.fw.add_interface(iface_name, iface_address)
        self.close()
    
    def when_cancel(self):
        self.close()