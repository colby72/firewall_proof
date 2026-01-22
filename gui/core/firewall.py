from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from gui.dialogs.add_interface import *
from gui.dialogs.edit_interface import *
from gui.dialogs.add_host import *
from gui.dialogs.edit_host import *
from gui.dialogs.show_host import *
from gui.dialogs.add_rule import *
from gui.dialogs.edit_rule import *

from reporting.generate_graphs import *

from superqt import QCollapsible
import json


class FirewallGUI(QWidget):
    def __init__(self, main_window, fw):
        QWidget.__init__(self)
        self.main_window = main_window
        self.fw = fw
        self.main_window.setWindowTitle(f"{self.fw.name} - Firewall Proof {self.main_window.version}")
        # update menu actions
        self.main_window.enable_actions(self.main_window.fw_specific_actions)
        if self.main_window.policy:
            self.main_window.enable_actions(self.main_window.policy_specific_actions)
        # load common ports dictionary
        with open("algorithms/common_ports.json", 'r', encoding="utf8") as f:
            self.common_ports = json.loads(f.read())

        # widget design
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # summary box
        summary = QGroupBox("Firewall summary")
        summary_layout = QGridLayout()
        summary_layout.setContentsMargins(10, 10, 10, 10)
        summary_layout.setSpacing(10)
        summary.setLayout(summary_layout)
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
        summary_layout.addWidget(QLabel("Compliance rate : "), 7, 0)
        summary_layout.addWidget(QLabel(f"{self.fw.compliance_rate()}%"), 7, 1)
        summary_layout.setColumnStretch(summary_layout.columnCount(), 1)
        summary_layout.setRowStretch(summary_layout.rowCount(), 1)

        chart_file, chart_path = status_pie_chart("Firewall compliance", self.fw.company, self.fw.status_stats())
        summary_chart = QLabel()
        summary_chart.resize(300, 300)
        chart_pixmap = QPixmap(chart_path)
        chart_scaled = chart_pixmap.scaled(summary_chart.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        summary_chart.setPixmap(chart_scaled)
        summary_layout.addWidget(summary_chart, 0, 2, 8, 1)

        # interface box
        interface = QGroupBox("Interfaces")
        interface_layout = QGridLayout()
        interface_layout.setContentsMargins(10, 10, 10, 10)
        interface_layout.setSpacing(20)
        interface.setLayout(interface_layout)
        headers = ["Name", "Address", "Hosts"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            interface_layout.addWidget(label, 0, i)
        for i, ifce in enumerate(self.fw.interfaces):
            interface_layout.addWidget(QLabel(ifce.name), i+1, 0)
            interface_layout.addWidget(QLabel(ifce.address), i+1, 1)
            interface_layout.addWidget(QLabel("n/a"), i+1, 2)
            edit_button = QPushButton("Edit")
            edit_button.setIcon(QIcon("img/edit_icon.png"))
            edit_button.clicked.connect(
                lambda checked, interface=ifce:
                self.edit_interface(interface)
            )
            edit_button.setFixedSize(120, 30)
            edit_button.setIconSize(QSize(18, 18))
            interface_layout.addWidget(edit_button, i+1, 3)

            remove_button = QPushButton("Remove")
            remove_button.setIcon(QIcon("img/delete.png"))
            remove_button.clicked.connect(
                lambda checked, interface=ifce:
                self.remove_interface(interface)
            )
            remove_button.setFixedSize(120, 30)
            remove_button.setIconSize(QSize(18, 18))
            interface_layout.addWidget(remove_button, i+1, 4)
        #interface_layout.setColumnStretch(interface_layout.columnCount(), 1)
        
        add_iface_button = QPushButton("Interface")
        add_iface_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_iface_button.clicked.connect(self.add_interface)
        add_iface_button.setFixedSize(140, 40)
        add_iface_button.setIconSize(QSize(20, 20))
        #interface_layout.addWidget(add_iface_button, len(self.fw.interfaces)+1, 0)

        # collapsible hosts box
        hosts_collapse = QCollapsible("List of hosts")
        hosts_widget = QWidget()
        hosts_layout = QGridLayout()
        hosts_layout.setSpacing(10)
        hosts_widget.setLayout(hosts_layout)
        hosts_collapse.addWidget(hosts_widget)

        hosts_per_row = self.main_window.hosts_per_row
        for i, h in enumerate(self.fw.hosts):
            host_widget = QWidget()
            host_layout = QGridLayout()
            host_widget.setLayout(host_layout)
            view_button = QPushButton('')
            view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
            view_button.setIconSize(QSize(16, 16))
            view_button.setFixedSize(16, 16)
            view_button.setToolTip("View Host")
            view_button.clicked.connect(
                lambda checked, host=h:
                self.show_host(host)
            )
            edit_button = QPushButton('')
            edit_button.setIcon(QIcon("img/edit_icon.png"))
            edit_button.setIconSize(QSize(16, 16))
            edit_button.setFixedSize(16, 16)
            edit_button.setToolTip("Edit Host")
            edit_button.clicked.connect(
                lambda checked, host=h:
                self.edit_host(host)
            )
            label = QLabel(h.name)
            label.setToolTip(f"Zone: {h.zone.name}\n{h.address}")
            label.setStyleSheet(f"color: {h.zone.color}")
            host_layout.addWidget(view_button, 0, 0)
            host_layout.addWidget(edit_button, 0, 1)
            host_layout.addWidget(label, 0, 2)
            hosts_layout.addWidget(host_widget, i//hosts_per_row, i%hosts_per_row)

        add_host_button = QPushButton("Host")
        add_host_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_host_button.clicked.connect(self.add_host)
        add_host_button.setFixedSize(140, 40)
        add_host_button.setIconSize(QSize(20, 20))

        # rules box
        rules = QGroupBox("Firewall rules")
        rules_layout = QGridLayout()
        rules_layout.setContentsMargins(10, 10, 10, 10)
        rules_layout.setSpacing(20)
        rules.setLayout(rules_layout)
        headers = ["ID", "Source", "Destination", "Service", "VPN", "Status"]
        for i in range(len(headers)):
            label = QLabel(headers[i])
            label.setStyleSheet("font-weight: bold;")
            #label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            rules_layout.addWidget(label, 0, i)
        for i, r in enumerate(self.fw.rules):
            rules_layout.addWidget(QLabel(str(r.number)), i+1, 0)
            
            # rule source
            src = QWidget()
            src_layout = QVBoxLayout()
            src_layout.addStretch(1)
            src.setLayout(src_layout)
            for j, host in enumerate(r.src):
                view_button = QPushButton('')
                view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
                view_button.setIconSize(QSize(16, 16))
                view_button.setFixedSize(16, 16)
                view_button.setToolTip("View Host")
                view_button.clicked.connect(
                    lambda checked, h=host:
                    self.show_host(h)
                )
                edit_button = QPushButton('')
                edit_button.setIcon(QIcon("img/edit_icon.png"))
                edit_button.setIconSize(QSize(16, 16))
                edit_button.setFixedSize(16, 16)
                edit_button.setToolTip("Edit Host")
                edit_button.clicked.connect(
                    lambda checked, h=host:
                    self.edit_host(h)
                )
                label = QLabel(host.name)
                label.setToolTip(f"Zone: {host.zone.name}\n{host.address}")
                label.setStyleSheet(f"color: {host.zone.color}")
                #src_layout.addWidget(view_button, j, 0)
                #src_layout.addWidget(edit_button, j, 1)
                src_layout.addWidget(label)
            src_layout.addStretch(1)
            rules_layout.addWidget(src, i+1, 1)
            
            # rule destination
            dest = QWidget()
            dest_layout = QVBoxLayout()
            dest_layout.addStretch(1)
            dest.setLayout(dest_layout)
            for j, host in enumerate(r.dest):
                view_button = QPushButton('')
                view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
                view_button.setIconSize(QSize(16, 16))
                view_button.setFixedSize(16, 16)
                view_button.setToolTip("View Host")
                view_button.clicked.connect(
                    lambda checked, h=host:
                    self.show_host(h)
                )
                edit_button = QPushButton('')
                edit_button.setIcon(QIcon("img/edit_icon.png"))
                edit_button.setIconSize(QSize(16, 16))
                edit_button.setFixedSize(16, 16)
                edit_button.setToolTip("Edit Host")
                edit_button.clicked.connect(
                    lambda checked, h=host:
                    self.edit_host(h)
                )
                label = QLabel(host.name)
                label.setToolTip(f"Zone: {host.zone.name}\n{host.address}")
                label.setStyleSheet(f"color: {host.zone.color}")
                #dest_layout.addWidget(view_button, j, 0)
                #dest_layout.addWidget(edit_button, j, 1)
                dest_layout.addWidget(label)
            dest_layout.addStretch(1)
            rules_layout.addWidget(dest, i+1, 2)
            
            # rule service
            services = QWidget()
            services_layout = QVBoxLayout()
            services_layout.addStretch(1)
            services.setLayout(services_layout)
            if r.services:
                for j, svc in enumerate(r.services):
                    label = QLabel(svc)
                    if svc in self.common_ports.keys():
                        label.setToolTip(self.common_ports[svc])
                    services_layout.addWidget(label)
            else:
                services_layout.addWidget(QLabel("all"))
            services_layout.addStretch(1)
            rules_layout.addWidget(services, i+1, 3)
            
            # rule vpn
            rules_layout.addWidget(QLabel(str(r.vpn)), i+1, 4)
            
            # rule status
            status = QLabel(str(r.status.label))
            status.setStyleSheet(f"""
                color: {r.status.color};
                font-weight: bold;
            """)
            rules_layout.addWidget(status, i+1, 5)
            
            edit_button = QPushButton('Edit')
            edit_button.setIcon(QIcon("img/edit_icon.png"))
            edit_button.clicked.connect(
                lambda checked, rule=r:
                self.edit_rule(rule)
            )
            edit_button.setFixedSize(120, 30)
            edit_button.setIconSize(QSize(18, 18))
            rules_layout.addWidget(edit_button, i+1, 6)
            remove_button = QPushButton('Remove')
            remove_button.setIcon(QIcon("img/delete.png"))
            remove_button.clicked.connect(
                lambda checked, rule=r:
                self.remove_rule(rule)
            )
            remove_button.setFixedSize(120, 30)
            remove_button.setIconSize(QSize(18, 18))
            rules_layout.addWidget(remove_button, i+1, 7)
        #rules_layout.setColumnStretch(rules_layout.columnCount(), 1)
        
        add_rule_button = QPushButton("Rule")
        add_rule_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_rule_button.clicked.connect(self.add_rule)
        add_rule_button.setFixedSize(140, 40)
        add_rule_button.setIconSize(QSize(20, 20))
        #rules_layout.addWidget(add_rule_button, len(self.fw.rules)+2, 0)

        layout.addWidget(summary, 0, 0, 1, 2)
        layout.addWidget(interface, 1, 0, 1, 5)
        layout.addWidget(add_iface_button, 2, 0, 1, 1)
        layout.addWidget(hosts_collapse, 3, 0, 1, 3)
        layout.addWidget(add_host_button, 4, 0, 1, 1)
        layout.addWidget(rules, 5, 0, 1, 8)
        layout.addWidget(add_rule_button, 6, 0, 1, 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        layout.setRowStretch(layout.rowCount(), 1)
    
    def add_interface(self):
        self.add_iface_dialog = DialogAddInterface(self.main_window, self.fw)
        self.add_iface_dialog.exec()
        self.main_window.show_firewall()
    
    def edit_interface(self, interface):
        self.edit_iface_dialog = DialogEditInterface(self.main_window, self.fw, interface)
        self.edit_iface_dialog.exec()
        self.main_window.show_firewall()
    
    def remove_interface(self, interface):
        self.fw.remove_interface(interface)
        self.main_window.show_firewall()
    
    def add_host(self):
        self.add_host_dialog = DialogAddHost(self.main_window, self.fw)
        self.add_host_dialog.exec()
        self.main_window.show_firewall()
    
    def show_host(self, host):
        self.show_host_dialog = DialogShowHost(self.main_window, host)
        self.show_host_dialog.exec()
        self.main_window.show_firewall()
    
    def edit_host(self, host):
        self.edit_host_dialog = DialogEditHost(self.main_window, self.fw, host)
        self.edit_host_dialog.exec()
        self.main_window.show_firewall()
    
    def add_rule(self):
        self.add_rule_dialog = DialogAddRule(self.main_window, self.fw)
        self.add_rule_dialog.exec()
        self.main_window.show_firewall()
    
    def edit_rule(self, rule):
        self.edit_rule_dialog = DialogEditRule(self.main_window, self.fw, rule)
        self.edit_rule_dialog.exec()
        self.main_window.show_firewall()
    
    def remove_rule(self, rule):
        self.fw.remove_rule(rule)
        self.main_window.show_firewall()