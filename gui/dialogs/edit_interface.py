from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class DialogEditInterface(QDialog):
    def __init__(self, main_window, fw, interface):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.interface = interface
        self.setWindowTitle("Edit Interface")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.iface_name = QLineEdit()
        self.iface_name.setMaxLength(15)
        self.iface_name.setText(interface.name)
        self.iface_name.setPlaceholderText("Interface name ...")
        layout.addWidget(self.iface_name, 0, 1)
        layout.addWidget(QLabel("Address : "), 1, 0)
        self.iface_address = QLineEdit()
        self.iface_address.setMaxLength(18)
        self.iface_address.setInputMask('000.000.000.000/00;_')
        self.iface_address.setText(interface.address)
        layout.addWidget(self.iface_address, 1, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 2, 1)
    
    def when_ok(self):
        iface_name = self.iface_name.text()
        iface_address = self.iface_address.text()
        self.interface.set_name(iface_name)
        self.interface.set_address(iface_address)
        self.close()
    
    def when_cancel(self):
        self.close()