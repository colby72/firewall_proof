from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class PolicyGUI(QWidget):
    def __init__(self, main_window, policy):
        QWidget.__init__(self)
        self.main_window = main_window
        self.policy = policy
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # summary
        layout.addWidget(QLabel("Name : "), 0, 0, 1, 1)
        layout.addWidget(QLabel(self.policy.name), 0, 1, 1, 1)
        layout.addWidget(QLabel("Default : "), 1, 0, 1, 1)
        layout.addWidget(QLabel(self.policy.default), 1, 1, 1, 1)

        # rules box
        rules = QGroupBox("Policy rules")
        rules_layout = QGridLayout()
        rules.setLayout(rules_layout)
        headers = ["Source zone", "Destination zone", "Services", "Status"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            rules_layout.addWidget(label, 0, i)
        for i in range(len(self.policy.rules)):
            r = self.policy.rules[i]
            rules_layout.addWidget(QLabel(r['src_zone']), i+1, 0)
            rules_layout.addWidget(QLabel(r['dest_zone']), i+1, 1)
            services = '\n'.join(r['services']) if r['services'] else "all"
            rules_layout.addWidget(QLabel(services), i+1, 2)
            rules_layout.addWidget(QLabel(r['status']), i+1, 3)
        
        layout.addWidget(rules, 2, 0, 1, 3)
        layout.addWidget(QLabel(), 2, 3, 1, 1)
        layout.setRowStretch(layout.rowCount(), 1)