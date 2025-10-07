from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from gui.dialogs.add_policy import *


class CompanyGUI(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        self.company = self.main_window.company
        #print(f"Main window's company : '{self.main_window.company.name}'")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # summary box
        summary = QGroupBox("Company summary")
        summary_layout = QGridLayout()
        summary_layout.setContentsMargins(10, 10, 10, 10)
        summary_layout.setSpacing(10)
        summary_layout.addWidget(QLabel("Name : "), 0, 0)
        summary_layout.addWidget(QLabel(self.company.name), 0, 1)
        summary_layout.addWidget(QLabel("Zones : "), 1, 0)
        summary_layout.addWidget(QLabel(str(len(self.company.zones))), 1, 1)
        summary_layout.addWidget(QLabel("Firewalls : "), 2, 0)
        summary_layout.addWidget(QLabel(str(len(self.company.fw_inventory))), 2, 1)
        summary.setLayout(summary_layout)

        # zones box
        zone = QGroupBox("Zones")
        zone.setFlat(False)
        zone_layout = QGridLayout()
        zone_layout.setSpacing(10)
        zone.setLayout(zone_layout)
        headers = ["Name","PURDUE level", "Description"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            zone_layout.addWidget(label, 0, i)
        for i in range(len(self.company.zones)):
            z = self.company.zones[i]
            zone_layout.addWidget(QLabel(z.name), i+1, 0, 1, 1)
            zone_layout.addWidget(QLabel(str(z.level)), i+1, 1, 1, 1)
            zone_layout.addWidget(QLabel(z.description), i+1, 2, 1, 1)
        #zone_layout.setRowStretch(zone_layout.rowCount(), 1)
        #zone_layout.setColumnStretch(zone_layout.columnCount(), 1)

        # policies box
        policies = QGroupBox("Company policies")
        policies_layout = QGridLayout()
        policies_layout.setSpacing(10)
        policies.setLayout(policies_layout)
        headers = ["Name", "Default", "# Rules"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            policies_layout.addWidget(label, 0, i)
        for i in range(len(self.company.policies)):
            p = self.company.policies[i]
            policies_layout.addWidget(QLabel(p.name), i+1, 0, 1, 1)
            policies_layout.addWidget(QLabel(str(p.default)), i+1, 1, 1, 1)
            policies_layout.addWidget(QLabel(str(len(p.rules))), i+1, 2, 1, 1)
            view_button = QPushButton("View")
            view_button.clicked.connect(
                lambda checked, pol=p:
                self.view_policy(pol)
            )
            policies_layout.addWidget(view_button, i+1, 3, 1, 1)
        add_policy_button = QPushButton("Add Policy")
        add_policy_button.clicked.connect(self.add_policy)

        # frewalls box
        firewall = QGroupBox("Firewalls")
        firewall_layout = QGridLayout()
        firewall.setLayout(firewall_layout)
        headers = ["Name", "Vendor", "Address", "Policy"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            #label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            firewall_layout.addWidget(label, 0, i*3)
        for i in range(len(self.company.fw_inventory)):
            fw = self.company.fw_inventory[i]
            firewall_layout.addWidget(QLabel(fw.name), i+1, 0, 1, 3)
            firewall_layout.addWidget(QLabel(fw.vendor), i+1, 3, 1, 3)
            firewall_layout.addWidget(QLabel(fw.address), i+1, 6, 1, 3)
            firewall_layout.addWidget(QLabel(str(fw.policy)), i+1, 9, 1, 3)
            view_button = QPushButton("View")
            view_button.clicked.connect(
                lambda checked, f=fw:
                self.view_firewall(f)
            )
            firewall_layout.addWidget(view_button, i+1, 12, 1, 1)

        layout.addWidget(summary)
        layout.addWidget(zone)
        layout.addWidget(policies)
        layout.addWidget(add_policy_button)
        layout.addWidget(firewall)
        layout.addStretch()
        self.setLayout(layout)
    
    def view_policy(self, policy):
        self.main_window.policy = policy
        self.main_window.show_policy()
    
    def view_firewall(self, fw):
        self.main_window.firewall = fw
        self.main_window.show_firewall()
    
    def add_policy(self):
        self.add_policy_dialog = DialogAddPolicy(self.main_window, self.company)
        self.add_policy_dialog.exec()
        self.main_window.show_company()