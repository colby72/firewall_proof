from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.firewall import *
from utils import *


class DialogEditFirewall(QDialog):
    def __init__(self, main_window, company, fw):
        super().__init__()
        self.main_window = main_window
        self.company = company
        self.fw = fw
        self.setWindowTitle("Edit Firewall")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.fw_name = QLineEdit()
        self.fw_name.setMaxLength(50)
        self.fw_name.setText(self.fw.name)
        self.fw_name.setPlaceholderText("Firewall name ...")
        layout.addWidget(self.fw_name, 0, 1)
        layout.addWidget(QLabel("Vendor : "), 1, 0)
        self.fw_vendor = QLineEdit()
        self.fw_vendor.setMaxLength(50)
        self.fw_vendor.setText(self.fw.vendor)
        self.fw_vendor.setPlaceholderText("Firewall vendor ...")
        layout.addWidget(self.fw_vendor, 1, 1)
        layout.addWidget(QLabel("Address : "), 2, 0)
        self.fw_address = QLineEdit()
        self.fw_address.setMaxLength(15)
        self.fw_address.setText(self.fw.address)
        self.fw_address.setPlaceholderText("Firewall address ...")
        self.fw_address.setInputMask('000.000.000.000;_')
        layout.addWidget(self.fw_address, 2, 1)
        layout.addWidget(QLabel("Policy : "), 3, 0)
        self.fw_policy = QComboBox()
        labels = [policy.name for policy in self.company.policies]
        self.fw_policy.addItems(labels)
        self.fw_policy.setCurrentText(self.fw.policy.name)
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
        self.fw.set_name(fw_name)
        self.fw.set_vendor(fw_vendor)
        self.fw.set_address(fw_address)
        self.fw.set_policy(fw_policy)
        self.close()
    
    def when_cancel(self):
        self.close()