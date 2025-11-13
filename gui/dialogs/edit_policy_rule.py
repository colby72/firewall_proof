from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from utils import *
from core.policy import *


class DialogEditPolicyRule(QDialog):
    def __init__(self, main_window, policy, policy_rule):
        super().__init__()
        self.main_window = main_window
        self.policy = policy
        self.policy_rule = policy_rule
        self.setWindowTitle("Edit Policy Rule")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.zones_list = dict()
        for z in self.policy.company.zones:
            self.zones_list[z.name] = z
        # rule source zone
        layout.addWidget(QLabel("Source zone : "), 0, 0)
        self.src_zone = QComboBox()
        self.src_zone.addItems(self.zones_list)
        self.src_zone.setCurrentText(self.policy_rule.src_zone.name)
        layout.addWidget(self.src_zone, 0, 1)
        # rule destination zone
        layout.addWidget(QLabel("Destination zone : "), 1, 0)
        self.dest_zone = QComboBox()
        self.dest_zone.addItems(self.zones_list)
        self.dest_zone.setCurrentText(self.policy_rule.dest_zone.name)
        layout.addWidget(self.dest_zone, 1, 1)
        # rule services
        service_box = QGroupBox("Services")
        service_layout = QGridLayout()
        service_box.setLayout(service_layout)
        self.services_list = QListWidget()
        self.services_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        if self.policy_rule.services:
            self.services_list.addItems(self.policy_rule.services)
        self.add_tcp = QPushButton("TCP")
        self.add_tcp.setIcon(QIcon("img/add_sign_icon.png"))
        self.add_tcp.clicked.connect(
            lambda checked, proto="TCP":
            self.add_service(proto)
        )
        self.add_udp = QPushButton("UDP")
        self.add_udp.setIcon(QIcon("img/add_sign_icon.png"))
        self.add_udp.clicked.connect(
            lambda checked, proto="UDP":
            self.add_service(proto)
        )
        self.add_icmp = QPushButton("ICMP")
        self.add_icmp.setIcon(QIcon("img/add_sign_icon.png"))
        self.add_icmp.clicked.connect(
            lambda checked, proto="ICMP":
            self.add_service(proto)
        )
        service_layout.addWidget(self.services_list, 0, 0, 3, 3)
        service_layout.addWidget(self.add_tcp, 3, 0, 1, 1)
        service_layout.addWidget(self.add_udp, 3, 1, 1, 1)
        service_layout.addWidget(self.add_icmp, 3, 2, 1, 1)
        self.remove_select_button = QPushButton("Remove")
        self.remove_select_button.setIcon(QIcon("img/minus_red_remove_icon.png"))
        self.remove_select_button.clicked.connect(self.remove_selected_services)
        self.clear_all_button = QPushButton("Clear")
        self.clear_all_button.setIcon(QIcon("img/error_exit_remove_icon.png"))
        self.clear_all_button.clicked.connect(self.clear_all_services)
        service_layout.addWidget(self.remove_select_button, 0, 4, 1, 1)
        service_layout.addWidget(self.clear_all_button, 1, 4, 1, 1)
        layout.addWidget(service_box, 2, 0, 2, 2)
        # rule vpn tunnel
        layout.addWidget(QLabel("VPN tunnel : "), 4, 0)
        self.vpn = QComboBox()
        self.vpn.addItems(["Yes", "No"])
        vpn_default = "Yes" if self.policy_rule.vpn else "No"
        self.vpn.setCurrentText(vpn_default)
        layout.addWidget(self.vpn, 4, 1)
        # rule status
        layout.addWidget(QLabel("Status : "), 5, 0)
        self.status = QComboBox()
        status_labels = [s.label for s in self.policy.company.status_list]
        self.status.addItems(status_labels)
        self.status.setCurrentText(self.policy_rule.status.label)
        layout.addWidget(self.status, 5, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 6, 1)
    
    def add_service(self, proto):
        self.port = None
        # get new service value
        add_service_dialog = DialogAddService(self, proto)
        add_service_dialog.exec()
        # add + display new service
        if self.port:
            new_service = f"{proto}/{self.port}"
            self.services_list.addItem(new_service)
    
    def remove_selected_services(self):
        for item in self.services_list.selectedItems():
            self.services_list.takeItem(self.services_list.row(item))
    
    def clear_all_services(self):
        self.services_list.clear()
        self.services = []

    def when_ok(self):
        src_zone = get_zone_by_name(self.policy.company, self.src_zone.currentText())
        dest_zone = get_zone_by_name(self.policy.company, self.dest_zone.currentText())
        services = [self.services_list.item(i).text() for i in range(self.services_list.count())]
        vpn = True if self.vpn.currentText()=="Yes" else False
        status = get_status_by_label(self.policy.company, self.status.currentText())
        self.policy_rule.set_src_zone(src_zone)
        self.policy_rule.set_dest_zone(dest_zone)
        self.policy_rule.set_services(services)
        self.policy_rule.set_vpn(vpn)
        self.policy_rule.set_status(status)
        self.close()
    
    def when_cancel(self):
        self.close()


class DialogAddService(QDialog):
    def __init__(self, add_rule_dialog, proto):
        super().__init__()
        self.add_rule_dialog = add_rule_dialog
        self.setWindowTitle(f"Add {proto} service")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.setLayout(layout)

        if proto == "TCP":
            range_min = 1
            range_max = 65000
            prefix = "TCP/"
        elif proto == "UDP":
            range_min = 1
            range_max = 65000
            prefix = "UDP/"
        elif proto=="ICMP":
            range_min = 1
            range_max = 8
            prefix = "ICMP/"
            
        self.service = QSpinBox()
        self.service.setRange(range_min, range_max)
        self.service.setPrefix(prefix)
        layout.addWidget(self.service)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons)
    
    def when_ok(self):
        self.add_rule_dialog.port = self.service.value()
        self.close()
    
    def when_cancel(self):
        self.close()