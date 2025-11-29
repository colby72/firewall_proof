from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.firewall import *
from utils import *


class DialogAddFirewall(QDialog):
    def __init__(self, main_window, company):
        super().__init__()
        self.main_window = main_window
        self.company = company
        self.setWindowTitle("Add new Firewall")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.fw_name = QLineEdit()
        self.fw_name.setMaxLength(50)
        self.fw_name.setPlaceholderText("Firewall name ...")
        layout.addWidget(self.fw_name, 0, 1)
        layout.addWidget(QLabel("Vendor : "), 1, 0)
        self.fw_vendor = QLineEdit()
        self.fw_vendor.setMaxLength(50)
        self.fw_vendor.setPlaceholderText("Firewall vendor ...")
        layout.addWidget(self.fw_vendor, 1, 1)
        layout.addWidget(QLabel("Address : "), 2, 0)
        self.fw_address = QLineEdit()
        self.fw_address.setMaxLength(15)
        self.fw_address.setPlaceholderText("Firewall address ...")
        self.fw_address.setInputMask('000.000.000.000;_')
        layout.addWidget(self.fw_address, 2, 1)
        layout.addWidget(QLabel("Policy : "), 3, 0)
        self.fw_policy = QComboBox()
        labels = [policy.name for policy in self.company.policies]
        self.fw_policy.addItems(labels)
        layout.addWidget(self.fw_policy, 3, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 4, 1)
    
    def when_ok(self):
        fw_name = self.fw_name.text()
        fw_vendor = self.fw_vendor.text()
        fw_address = self.fw_address.text()
        fw_policy = get_policy_by_name(self.company, self.fw_policy.currentText())
        new_fw = Firewall(self.company, fw_name, fw_vendor, fw_address, fw_policy)
        self.company.add_firewall(new_fw)
        self.close()
    
    def when_cancel(self):
        self.close()