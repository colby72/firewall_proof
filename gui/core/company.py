from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from gui.dialogs.add_zone import *
from gui.dialogs.edit_zone import *
from gui.dialogs.add_status import *
from gui.dialogs.edit_status import *
from gui.dialogs.add_policy import *
from gui.dialogs.edit_policy import *
from gui.dialogs.add_firewall import *
from gui.dialogs.edit_firewall import *


class CompanyGUI(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        self.company = self.main_window.company
        self.main_window.setWindowTitle(f"{self.company.name} - Firewall Proof {self.main_window.version}")
        # update menu actions
        enabled_actions = [self.main_window.company_submenu, self.main_window.company_report_action]
        self.main_window.enable_actions(enabled_actions)
        disabled_actions = [self.main_window.firewall_submenu, self.main_window.policy_submenu, self.main_window.firewall_report_action]
        self.main_window.disable_actions(disabled_actions)

        # widget design
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
            zone_label = QLabel(z.name)
            zone_label.setStyleSheet(f"color: {z.color}")
            zone_layout.addWidget(zone_label, i+1, 0, 1, 1)
            zone_layout.addWidget(QLabel(str(z.level)), i+1, 1, 1, 1)
            zone_layout.addWidget(QLabel(z.description), i+1, 2, 1, 1)
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon("img/pencil_icon.png"))
            edit_button.clicked.connect(
                lambda checked, zparam=z:
                self.edit_zone(zparam)
            )
            zone_layout.addWidget(edit_button, i+1, 3)
        add_zone_button = QPushButton("Zone")
        add_zone_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_zone_button.clicked.connect(self.add_zone)
        zone_layout.addWidget(add_zone_button, len(self.company.zones)+1, 0)

        # status box
        status_box = QGroupBox("Status list")
        status_layout = QGridLayout()
        status_layout.setSpacing(10)
        status_box.setLayout(status_layout)
        status_per_row = 3
        status_count = len(self.company.status_list)
        for i in range(status_count):
            status = self.company.status_list[i]
            status_item = QWidget()
            status_item_layout = QHBoxLayout()
            status_item.setLayout(status_item_layout)
            # status label
            label = QLabel(status.label)
            label.setStyleSheet(f"color: {status.color}")
            # status edit button
            edit_button = QPushButton('')
            edit_button.setIcon(QIcon("img/pencil_icon.png"))
            edit_button.setIconSize(QSize(16, 16))
            edit_button.setFixedSize(16, 16)
            edit_button.setToolTip("Edit Status")
            edit_button.clicked.connect(
                lambda checked, s=status:
                self.edit_status(s)
            )
            status_item_layout.addWidget(label)
            status_item_layout.addWidget(edit_button)
            status_item_layout.addStretch()
            status_layout.addWidget(status_item, i//status_per_row, i%status_per_row)
        add_status_button = QPushButton("Status")
        add_status_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_status_button.clicked.connect(self.add_status)
        status_layout.addWidget(add_status_button, status_count//status_per_row, status_count%status_per_row)

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
            policies_layout.addWidget(QLabel(str(p.default.label)), i+1, 1, 1, 1)
            policies_layout.addWidget(QLabel(str(len(p.rules))), i+1, 2, 1, 1)
            view_button = QPushButton("View")
            view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
            view_button.clicked.connect(
                lambda checked, pol=p:
                self.view_policy(pol)
            )
            policies_layout.addWidget(view_button, i+1, 3, 1, 1)
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon("img/pencil_icon.png"))
            edit_button.clicked.connect(
                lambda checked, pol=p:
                self.edit_policy(pol)
            )
            policies_layout.addWidget(edit_button, i+1, 4, 1, 1)
        add_policy_button = QPushButton("Policy")
        add_policy_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_policy_button.clicked.connect(self.add_policy)
        policies_layout.addWidget(add_policy_button, len(self.company.policies)+1, 0)

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
            firewall_layout.addWidget(QLabel(fw.policy.name), i+1, 9, 1, 3)
            view_button = QPushButton("View")
            view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
            view_button.clicked.connect(
                lambda checked, f=fw:
                self.view_firewall(f)
            )
            firewall_layout.addWidget(view_button, i+1, 12, 1, 1)
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon("img/pencil_icon.png"))
            edit_button.clicked.connect(
                lambda checked, f=fw:
                self.edit_firewall(f)
            )
            firewall_layout.addWidget(edit_button, i+1, 15, 1, 1)
        add_fw_button = QPushButton("Add Firewall")
        add_fw_button.clicked.connect(self.add_firewall)
        firewall_layout.addWidget(add_fw_button, len(self.company.fw_inventory)+1 ,0)

        layout.addWidget(summary)
        layout.addWidget(zone)
        layout.addWidget(status_box)
        layout.addWidget(policies)
        layout.addWidget(firewall)
        layout.addStretch()
        self.setLayout(layout)
    
    def view_policy(self, policy):
        self.main_window.policy = policy
        self.main_window.show_policy()
    
    def edit_policy(self, policy):
        self.edit_policy_dialog = DialogEditPolicy(self.main_window, self.company, policy)
        self.edit_policy_dialog.exec()
        self.main_window.show_company()
    
    def view_firewall(self, fw):
        self.main_window.firewall = fw
        self.main_window.show_firewall()
    
    def add_zone(self):
        self.add_zone_dialog = DialogAddZone(self.main_window, self.company)
        self.add_zone_dialog.exec()
        self.main_window.show_company()
    
    def edit_zone(self, zone):
        self.edit_zone_dialog = DialogEditZone(self.main_window, self.company, zone)
        self.edit_zone_dialog.exec()
        self.main_window.show_company()
    
    def add_status(self):
        self.add_status_dialog = DialogAddStatus(self.main_window, self.company)
        self.add_status_dialog.exec()
        self.main_window.show_company()
    
    def edit_status(self, status):
        self.edit_status_dialog = DialogEditStatus(self.main_window, self.company, status)
        self.edit_status_dialog.exec()
        self.main_window.show_company()
    
    def add_policy(self):
        self.add_policy_dialog = DialogAddPolicy(self.main_window, self.company)
        self.add_policy_dialog.exec()
        self.main_window.show_company()
    
    def add_firewall(self):
        self.add_fw_dialog = DialogAddFirewall(self.main_window, self.company)
        self.add_fw_dialog.exec()
        self.main_window.show_company()
    
    def edit_firewall(self, fw):
        self.edit_fw_dialog = DialogEditFirewall(self.main_window, self.company, fw)
        self.edit_fw_dialog.exec()
        self.main_window.show_company()