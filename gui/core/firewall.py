from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from gui.dialogs.add_interface import *
from gui.dialogs.add_host import *
from gui.dialogs.add_rule import *


class FirewallGUI(QWidget):
    def __init__(self, main_window, fw):
        QWidget.__init__(self)
        self.main_window = main_window
        self.fw = fw
        self.main_window.setWindowTitle(f"{self.fw.name} - Firewall Proof {self.main_window.version}")
        # update menu actions
        enabled_actions = [self.main_window.firewall_submenu]
        self.main_window.enable_actions(enabled_actions)
        
        # widget design
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # summary box
        summary = QGroupBox("Firewall summary")
        summary_layout = QGridLayout()
        summary_layout.setContentsMargins(10, 10, 10, 10)
        summary_layout.setSpacing(10)
        summary_layout.addWidget(QLabel("Name : "), 0, 0)
        summary_layout.addWidget(QLabel(self.fw.name), 0, 1)
        summary_layout.addWidget(QLabel("Vendor : "), 1, 0)
        summary_layout.addWidget(QLabel(self.fw.vendor), 1, 1)
        summary_layout.addWidget(QLabel("Address : "), 2, 0)
        summary_layout.addWidget(QLabel(self.fw.address), 2, 1)
        summary_layout.addWidget(QLabel("Policy : "), 3, 0)
        summary_layout.addWidget(QLabel(self.fw.policy.name), 3, 1)
        summary_layout.addWidget(QLabel("Interfaces : "), 4, 0)
        summary_layout.addWidget(QLabel(str(len(self.fw.interfaces))), 4, 1)
        summary_layout.addWidget(QLabel("Hosts (Groups) : "), 5, 0)
        summary_layout.addWidget(QLabel(f"{len(self.fw.hosts)} ({len(self.fw.groups)})"), 5, 1)
        summary_layout.addWidget(QLabel("Rules : "), 6, 0)
        summary_layout.addWidget(QLabel(str(len(self.fw.rules))), 6, 1)
        summary.setLayout(summary_layout)

        # interface box
        interface = QGroupBox("Interfaces")
        interface_layout = QGridLayout()
        interface.setLayout(interface_layout)
        headers = ["Name", "Address", "Hosts"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            interface_layout.addWidget(label, 0, i)
        for i in range(len(self.fw.interfaces)):
            ifce = self.fw.interfaces[i]
            interface_layout.addWidget(QLabel(ifce['name']), i+1, 0)
            interface_layout.addWidget(QLabel(ifce['address']), i+1, 1)
            interface_layout.addWidget(QLabel("n/a"), i+1, 2)
        add_iface_button = QPushButton("Add Interface")
        add_iface_button.clicked.connect(self.add_interface)

        add_host_button = QPushButton("Add Host")
        add_host_button.clicked.connect(self.add_host)

        # rules box
        rules = QGroupBox("Firewall rules")
        rules_layout = QGridLayout()
        rules.setLayout(rules_layout)
        headers = ["ID", "Source", "Destination", "Service", "VPN", "Status"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            rules_layout.addWidget(label, 0, i)
        for i in range(len(self.fw.rules)):
            r = self.fw.rules[i]
            rules_layout.addWidget(QLabel(str(r.number)), i+1, 0)
            src = '\n'.join([host.name for host in r.src])
            rules_layout.addWidget(QLabel(src), i+1, 1)
            dest = '\n'.join([host.name for host in r.dest])
            rules_layout.addWidget(QLabel(dest), i+1, 2)
            services = '\n'.join(r.services) if r.services else "all"
            rules_layout.addWidget(QLabel(services), i+1, 3)
            rules_layout.addWidget(QLabel(str(r.vpn)), i+1, 4)
            rules_layout.addWidget(QLabel(str(r.status)), i+1, 5)
        add_rule_button = QPushButton("Add Rule")
        add_rule_button.clicked.connect(self.add_rule)

        layout.addWidget(summary)
        layout.addWidget(interface)
        layout.addWidget(add_iface_button)
        layout.addWidget(add_host_button)
        layout.addWidget(rules)
        layout.addWidget(add_rule_button)
        layout.addStretch()
    
    def add_interface(self):
        self.add_iface_dialog = DialogAddInterface(self.main_window, self.fw)
        self.add_iface_dialog.exec()
        self.main_window.show_firewall()
    
    def add_host(self):
        self.add_host_dialog = DialogAddHost(self.main_window, self.fw)
        self.add_host_dialog.exec()
        self.main_window.show_firewall()
    
    def add_rule(self):
        self.add_rule_dialog = DialogAddRule(self.main_window, self.fw)
        self.add_rule_dialog.exec()
        self.main_window.show_firewall()