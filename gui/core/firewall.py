from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class FirewallGUI(QWidget):
    def __init__(self, main_window, fw):
        QWidget.__init__(self)
        self.main_window = main_window
        self.fw = fw
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
        summary_layout.addWidget(QLabel("Interfaces : "), 3, 0)
        summary_layout.addWidget(QLabel(str(len(self.fw.interfaces))), 3, 1)
        summary_layout.addWidget(QLabel("Hosts (Groups) : "), 4, 0)
        summary_layout.addWidget(QLabel(f"{len(self.fw.hosts)} ({len(self.fw.groups)})"), 3, 1)
        summary_layout.addWidget(QLabel("Rules : "), 5, 0)
        summary_layout.addWidget(QLabel(str(len(self.fw.rules))), 5, 1)
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

        # rules box
        rules = QGroupBox("Firewall rules")
        rules_layout = QGridLayout()
        rules.setLayout(rules_layout)
        headers = ["ID", "Source", "Destination", "Service", "Status"]
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
            rules_layout.addWidget(QLabel('\n'.join(r.services)), i+1, 3)
            rules_layout.addWidget(QLabel(str(r.status)), i+1, 4)

        layout.addWidget(summary)
        layout.addWidget(interface)
        layout.addWidget(rules)
        layout.addStretch()