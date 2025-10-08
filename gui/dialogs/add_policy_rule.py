from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class DialogAddPolicyRule(QDialog):
    def __init__(self, main_window, policy):
        super().__init__()
        self.main_window = main_window
        self.policy = policy
        self.setWindowTitle("Add new Policy Rule")
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
        layout.addWidget(self.src_zone, 0, 1)
        # rule destination zone
        layout.addWidget(QLabel("Destination zone : "), 1, 0)
        self.dest_zone = QComboBox()
        self.dest_zone.addItems(self.zones_list)
        layout.addWidget(self.dest_zone, 1, 1)
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
        layout.addWidget(service_box, 2, 0)
        # rule vpn tunnel
        layout.addWidget(QLabel("VPN tunnel : "), 3, 0)
        self.vpn = QComboBox()
        self.vpn.addItems(["Yes", "No"])
        layout.addWidget(self.vpn, 3, 1)
        # rule status
        layout.addWidget(QLabel("Status : "), 4, 0)
        self.status = QComboBox()
        self.status.addItems(["OK", "WARNING", "NOK"])
        layout.addWidget(self.status, 4, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 5, 1)
    
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
        services = self.services[:] if self.services else None
        vpn = True if self.vpn.currentText()=="Yes" else False
        new_policy_rule = {
            "src_zone": self.src_zone.currentText(),
            "dest_zone": self.dest_zone.currentText(),
            "services": services,
            "vpn": vpn,
            "status": self.status.currentText()
        }
        self.policy.rules.append(new_policy_rule)
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