from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from gui.dialogs.add_policy_rule import *
from gui.dialogs.edit_policy_rule import *


class PolicyGUI(QWidget):
    def __init__(self, main_window, policy):
        QWidget.__init__(self)
        self.main_window = main_window
        self.policy = policy
        self.main_window.setWindowTitle(f"{self.policy.name} - Firewall Proof {self.main_window.version}")
        # update menu actions
        enabled_actions = [self.main_window.policy_submenu]
        self.main_window.enable_actions(enabled_actions)
        disabled_actions = [self.main_window.firewall_submenu]
        self.main_window.disable_actions(disabled_actions)
        
        # widget design
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # summary
        layout.addWidget(QLabel("Name : "), 0, 0, 1, 1)
        layout.addWidget(QLabel(self.policy.name), 0, 1, 1, 1)
        layout.addWidget(QLabel("Default : "), 1, 0, 1, 1)
        default_label = QLabel(str(self.policy.default.label))
        default_label.setStyleSheet(f"""
            color: {self.policy.default.color};
            font-weight: bold;
        """)
        layout.addWidget(default_label, 1, 1, 1, 1)

        # rules box
        rules = QGroupBox("Policy rules")
        rules_layout = QGridLayout()
        rules.setLayout(rules_layout)
        headers = ["Source zone", "Destination zone", "Services", "VPN", "Status"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            rules_layout.addWidget(label, 0, i)
        for i in range(len(self.policy.rules)):
            r = self.policy.rules[i]
            src_zone = QLabel(r.src_zone.name)
            src_zone.setStyleSheet(f"color: {r.src_zone.color}")
            rules_layout.addWidget(src_zone, i+1, 0)
            dest_zone = QLabel(r.dest_zone.name)
            dest_zone.setStyleSheet(f"color: {r.dest_zone.color}")
            rules_layout.addWidget(dest_zone, i+1, 1)
            services = '\n'.join(r.services) if r.services else "all"
            rules_layout.addWidget(QLabel(services), i+1, 2)
            rules_layout.addWidget(QLabel(str(r.vpn)), i+1, 3)
            status_label = QLabel(str(r.status.label))
            status_label.setStyleSheet(f"""
                color: {r.status.color};
                font-weight: bold;
            """)
            rules_layout.addWidget(status_label, i+1, 4)
            edit_button = QPushButton('Edit')
            edit_button.setIcon(QIcon("img/edit_icon.png"))
            edit_button.clicked.connect(
                lambda checked, rule=r:
                self.edit_policy_rule(rule)
            )
            rules_layout.addWidget(edit_button, i+1, 5)
        
        # add policy rule button
        add_policy_rule_button = QPushButton("Policy Rule")
        add_policy_rule_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_policy_rule_button.clicked.connect(self.add_policy_rule)
        
        layout.addWidget(rules, 2, 0, 1, 3)
        layout.addWidget(QLabel(), 2, 3, 1, 1)
        layout.addWidget(add_policy_rule_button, 3, 0, 1, 1)
        layout.setRowStretch(layout.rowCount(), 1)
    
    def add_policy_rule(self):
        self.add_policy_rule_dialog = DialogAddPolicyRule(self.main_window, self.policy)
        self.add_policy_rule_dialog.exec()
        self.main_window.show_policy()
    
    def edit_policy_rule(self, policy_rule):
        self.edit_policy_rule_dialog = DialogEditPolicyRule(self.main_window, self.policy, policy_rule)
        self.edit_policy_rule_dialog.exec()
        self.main_window.show_policy()