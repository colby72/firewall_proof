from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


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
        zone_layout = QGridLayout()
        zone.setLayout(zone_layout)
        headers = ["Name","PURDUE level", "Description"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            zone_layout.addWidget(label, 0, i)
        for i in range(len(self.company.zones)):
            z = self.company.zones[i]
            zone_layout.addWidget(QLabel(z.name), i+1, 0)
            zone_layout.addWidget(QLabel(str(z.level)), i+1, 1)
            zone_layout.addWidget(QLabel(z.description), i+1, 2)

        # frewalls box
        firewall = QGroupBox("Firewalls")
        firewall_layout = QGridLayout()
        firewall.setLayout(firewall_layout)
        headers = ["Name", "Vendor", "Address", "Policy"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            firewall_layout.addWidget(label, 0, i)
        for i in range(len(self.company.fw_inventory)):
            fw = self.company.fw_inventory[i]
            firewall_layout.addWidget(QLabel(fw.name), i+1, 0)
            firewall_layout.addWidget(QLabel(fw.vendor), i+1, 1)
            firewall_layout.addWidget(QLabel(fw.address), i+1, 2)
            firewall_layout.addWidget(QLabel(str(fw.policy)), i+1, 3)

        layout.addWidget(summary)
        layout.addWidget(zone)
        layout.addWidget(firewall)
        layout.addStretch()
        self.setLayout(layout)