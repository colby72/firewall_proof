from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from utils import *
from core.rule import *
from algorithms.policy_check import *


class DialogAddRule(QDialog):
    def __init__(self, main_window, fw):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle("Add new Firewall rule")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # rule number
        layout.addWidget(QLabel("Number : "), 0, 0)
        self.rule_number = QSpinBox()
        self.rule_number.setRange(1,999)
        self.rule_number.setValue(10)
        self.rule_number.setPrefix('#')
        layout.addWidget(self.rule_number, 0, 1)
        # rule source hosts
        self.hosts_list = dict()
        for h in self.fw.hosts:
            self.hosts_list[h.name] = h
        layout.addWidget(QLabel("Source : "), 1, 0)
        self.rule_src = QListWidget()
        self.rule_src.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.rule_src.addItems(self.hosts_list.keys())
        layout.addWidget(self.rule_src, 2, 0)
        # rule destination hosts
        layout.addWidget(QLabel("Destination : "), 1, 1)
        self.rule_dest = QListWidget()
        self.rule_dest.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.rule_dest.addItems(self.hosts_list.keys())
        layout.addWidget(self.rule_dest, 2, 1)
        # rule services
        service_box = QGroupBox("Services")
        service_layout = QGridLayout()
        service_box.setLayout(service_layout)
        self.services_list = QListWidget()
        self.services_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
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
        layout.addWidget(service_box, 3, 0, 1, 1)
        # rule vpn
        layout.addWidget(QLabel("VPN tunnel : "), 4, 0)
        self.rule_vpn = QComboBox()
        self.rule_vpn.addItems(["No", "Yes"])
        layout.addWidget(self.rule_vpn, 4, 1)
        # rule status
        layout.addWidget(QLabel("Status : "), 5, 0)
        self.status_box = QGroupBox("Manual")
        self.status_box.setCheckable(True)
        self.status_box.setChecked(False)
        self.status_layout = QGridLayout()
        self.status_box.setLayout(self.status_layout)
        self.status_list = QComboBox()
        status_labels = [s.label for s in self.fw.company.status_list]
        self.status_list.addItems(status_labels)
        self.status_layout.addWidget(self.status_list, 0, 0)
        layout.addWidget(self.status_box, 5, 1)

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
        rule_number = self.rule_number.value()
        rule_src = [self.hosts_list[item.text()] for item in self.rule_src.selectedItems()]
        rule_dest = [self.hosts_list[item.text()] for item in self.rule_dest.selectedItems()]
        rule_services = [self.services_list.item(i).text() for i in range(self.services_list.count())]
        rule_vpn = True if self.rule_vpn.currentText()=="Yes" else False
        rule_manual = self.status_box.isChecked()
        new_rule = Rule(rule_number, rule_src, rule_dest, rule_services, rule_vpn, rule_manual)
        self.fw.add_rule(new_rule)
        if rule_manual:
            status = get_status_by_label(self.fw.company, self.status_list.currentText())
            new_rule.set_status(status)
        else:
            apply_policy(self.fw, self.fw.policy)
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