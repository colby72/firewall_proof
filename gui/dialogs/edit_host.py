from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.host import *
from algorithms.policy_check import *


class DialogEditHost(QDialog):
    def __init__(self, main_window, fw, host):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.host = host
        self.setWindowTitle("Edit Host")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.host_name = QLineEdit()
        self.host_name.setMaxLength(50)
        self.host_name.setText(self.host.name)
        self.host_name.setPlaceholderText("Host name ...")
        layout.addWidget(self.host_name, 0, 1)
        layout.addWidget(QLabel("Address : "), 1, 0)
        self.host_address = QLineEdit()
        self.host_address.setMaxLength(18)
        self.host_address.setText(self.host.address)
        self.host_address.setInputMask('000.000.000.000/00;_')
        layout.addWidget(self.host_address, 1, 1)
        layout.addWidget(QLabel("Zone : "), 2, 0)
        self.host_zone = QComboBox()
        self.zones_list = dict()
        for z in self.fw.company.zones:
            self.zones_list[z.name] = z
        self.host_zone.addItems(self.zones_list.keys())
        self.host_zone.setCurrentText(self.host.zone.name)
        layout.addWidget(self.host_zone, 2, 1)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 3, 1)
    
    def when_ok(self):
        host_name = self.host_name.text()
        host_address = self.host_address.text()
        host_zone = self.zones_list[self.host_zone.currentText()]
        self.host.set_name(host_name)
        self.host.set_address(host_address)
        self.host.set_zone(host_zone)
        self.close()
    
    def when_cancel(self):
        self.close()