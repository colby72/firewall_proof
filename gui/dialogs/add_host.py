from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.host import *


class DialogAddHost(QDialog):
    def __init__(self, main_window, fw):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle("Add new Host")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.host_name = QLineEdit()
        self.host_name.setMaxLength(20)
        self.host_name.setPlaceholderText("Host name ...")
        layout.addWidget(self.host_name, 0, 1)
        layout.addWidget(QLabel("Address : "), 1, 0)
        self.host_address = QLineEdit()
        self.host_address.setMaxLength(18)
        self.host_address.setInputMask('000.000.000.000/00;_')
        layout.addWidget(self.host_address, 1, 1)
        layout.addWidget(QLabel("Zone : "), 2, 0)
        self.host_zone = QComboBox()
        self.zones_list = dict()
        for z in self.fw.company.zones:
            self.zones_list[z.name] = z
        self.host_zone.addItems(self.zones_list.keys())
        layout.addWidget(self.host_zone, 2, 1)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 3, 1)
    
    def when_ok(self):
        host_name = self.host_name.text()
        host_address = self.host_address.text()
        host_zone = self.zones_list[self.host_zone.currentText()]
        new_host = Host(self.fw, host_name, host_zone, host_address)
        self.fw.add_host(new_host)
        self.close()
    
    def when_cancel(self):
        self.close()