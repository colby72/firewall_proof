from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.policy import *


class DialogEditPolicy(QDialog):
    def __init__(self, main_window, company, policy):
        super().__init__()
        self.main_window = main_window
        self.company = company
        self.policy = policy
        self.setWindowTitle("Edit Policy")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        layout.addWidget(QLabel("Name : "), 0, 0)
        self.policy_name = QLineEdit()
        self.policy_name.setMaxLength(15)
        self.policy_name.setText(policy.name)
        self.policy_name.setPlaceholderText("Policy name ...")
        layout.addWidget(self.policy_name, 0, 1)
        layout.addWidget(QLabel("Default status : "), 1, 0)
        self.policy_default = QComboBox()
        labels = [status.label for status in company.status_list]
        self.policy_default.addItems(labels)
        self.policy_default.setCurrentText(self.policy.default.label)
        layout.addWidget(self.policy_default, 1, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 2, 1)
    
    def when_ok(self):
        policy_default = get_status_by_label(self.company, self.policy_default.currentText())
        self.policy.set_name(self.policy_name.text())
        self.policy.set_default(policy_default)
        self.close()
    
    def when_cancel(self):
        self.close()