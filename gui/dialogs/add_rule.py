from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.rule import *
from algorithms.policy_check import *


class DialogAddRule(QDialog):
    def __init__(self, main_window, fw):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle("Add new Host")
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
        self.services = []
        service_box = QGroupBox("Services")
        service_layout = QGridLayout()
        service_box.setLayout(service_layout)
        self.services_list = QListWidget()
        self.add_tcp = QPushButton("+ TCP")
        self.add_tcp.clicked.connect(
            lambda checked, proto="TCP":
            self.add_service(proto)
        )
        self.add_udp = QPushButton("+ UDP")
        self.add_udp.clicked.connect(
            lambda checked, proto="UDP":
            self.add_service(proto)
        )
        self.add_icmp = QPushButton("+ ICMP")
        self.add_icmp.clicked.connect(
            lambda checked, proto="ICMP":
            self.add_service(proto)
        )
        service_layout.addWidget(self.services_list, 0, 0, 1, 3)
        service_layout.addWidget(self.add_tcp, 1, 0, 1, 1)
        service_layout.addWidget(self.add_udp, 1, 1, 1, 1)
        service_layout.addWidget(self.add_icmp, 1, 2, 1, 1)
        layout.addWidget(service_box, 3, 0)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 4, 1)
    
    def add_service(self, proto):
        self.port = None
        # get new service value
        add_service_dialog = DialogAddService(self, proto)
        add_service_dialog.exec()
        # add + display new service
        if self.port:
            new_service = f"{proto}/{self.port}"
            self.services.append(new_service)
            self.services_list.addItem(new_service)

    def when_ok(self):
        rule_number = self.rule_number.value()
        rule_src = [self.hosts_list[item.text()] for item in self.rule_src.selectedItems()]
        rule_dest = [self.hosts_list[item.text()] for item in self.rule_dest.selectedItems()]
        new_rule = Rule(rule_number, rule_src, rule_dest, self.services)
        self.fw.add_rule(new_rule)
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