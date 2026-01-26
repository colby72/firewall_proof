from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import json

from algorithms.net_topology_anomalies import subnet_zone_overlaps, direct_it_ot_flows, wrong_zone_attribution, vulnerable_services


class DialogNetTopologyAnomalies(QDialog):
    def __init__(self, main_window, fw):
        QWidget.__init__(self)
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle(f"Firewall {self.fw.name} - Network topology anomalies")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)

        colors = {"info": "#0000e0", "warning": "#f4bf14", "critical": "#ff0000"}
        # load common ports dictionary
        with open("algorithms/common_ports.json", 'r', encoding="utf8") as f:
            self.common_ports = json.loads(f.read())
        
        # widget design
        main_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10   )
        main_layout.setSpacing(10)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        main_widget.setLayout(layout)
        row = 0

        # zone subnet overlaps
        overlaps = subnet_zone_overlaps(self.fw)
        if overlaps:
            overlaps_box = QGroupBox("Zone subnet overlaps")
            overlaps_layout = QGridLayout()
            overlaps_layout.setContentsMargins(10, 10, 10, 10)
            overlaps_layout.setSpacing(10)
            overlaps_box.setLayout(overlaps_layout)
            for i in range(len(overlaps)):
                h1, h2, level = overlaps[i]
                label = QLabel(level.upper())
                label.setStyleSheet(f"""
                    color: {colors[level]};
                    font-weight: bold;
                """)
                overlaps_layout.addWidget(label, i, 0)
                msg = f"{h1.name} ({h1.zone.name}) and {h2.name} ({h2.zone.name}) share the same subnet while belonging to different zones"
                overlaps_layout.addWidget(QLabel(msg), i, 1)
            overlaps_layout.setColumnStretch(overlaps_layout.columnCount(), 1)
            overlaps_layout.setRowStretch(overlaps_layout.rowCount(), 1)
            layout.addWidget(overlaps_box, row, 0)
            row += 1

        # direct IT OT flows
        breaches = direct_it_ot_flows(self.fw, True)
        if breaches:
            direct_box = QGroupBox("Direct IT-OT flows")
            direct_layout = QGridLayout()
            direct_layout.setContentsMargins(10, 10, 10, 10)
            direct_layout.setSpacing(10)
            direct_box.setLayout(direct_layout)
            for i, breach in enumerate(breaches):
                label = QLabel("WARNING")
                label.setStyleSheet(f"""
                    color: {colors["warning"]};
                    font-weight: bold;
                """)
                direct_layout.addWidget(label, i, 0)
                direct_layout.addWidget(QLabel(breach), i, 1)
            direct_layout.setColumnStretch(direct_layout.columnCount(), 1)
            direct_layout.setRowStretch(direct_layout.rowCount(), 1)
            layout.addWidget(direct_box, row, 0)
            row += 1
        
        # wrong zone attribution
        wrong_hosts = wrong_zone_attribution(self.fw)
        if wrong_hosts:
            wrong_box = QGroupBox("Suspected host zonings")
            wrong_layout = QGridLayout()
            wrong_layout.setContentsMargins(10, 10, 10, 10)
            wrong_layout.setSpacing(10)
            wrong_box.setLayout(wrong_layout)
            for i in range(len(wrong_hosts)):
                h, svc_list, rule_id, level = wrong_hosts[i]
                label = QLabel(level.upper())
                label.setStyleSheet(f"""
                    color: {colors[level]};
                    font-weight: bold;
                """)
                wrong_layout.addWidget(label, i, 0)
                for j in range(len(svc_list)): svc_list[j] = self.common_ports[svc_list[j]]
                applicable_svc = ', '.join(svc_list)
                msg = f"Host <b>{h.name}</b> classified as an IT asset but uses OT protocols ({applicable_svc}) in rule #{rule_id} suggesting it may be an OT asset instead."
                wrong_layout.addWidget(QLabel(msg), i, 1)
            wrong_layout.setColumnStretch(wrong_layout.columnCount(), 1)
            wrong_layout.setRowStretch(wrong_layout.rowCount(), 1)
            layout.addWidget(wrong_box, row, 0)
            row += 1
        
        # vulnerables services
        vuln_services = vulnerable_services(self.fw)
        if vuln_services:
            vuln_services_box = QGroupBox("Weak services")
            vuln_services_layout = QGridLayout()
            vuln_services_layout.setContentsMargins(10, 10, 10, 10)
            vuln_services_layout.setSpacing(10)
            vuln_services_box.setLayout(vuln_services_layout)
            for i, vuln in enumerate(vuln_services):
                label = QLabel("WARNING")
                label.setStyleSheet(f"""
                    color: {colors["warning"]};
                    font-weight: bold;
                """)
                vuln_services_layout.addWidget(label, i, 0)
                msg = f"Rule <b>#{vuln[0]}</b> allows weak service <b>{self.common_ports[vuln[1]]} ({vuln[1]})</b>. Please consider using <b>{self.common_ports[vuln[2]]} ({vuln[2]})</b> instead."
                vuln_services_layout.addWidget(QLabel(msg), i, 1)
            vuln_services_layout.setColumnStretch(vuln_services_layout.columnCount(), 1)
            vuln_services_layout.setRowStretch(vuln_services_layout.rowCount(), 1)
            layout.addWidget(vuln_services_box, row, 0)


        layout.setColumnStretch(layout.columnCount(), 1)
        layout.setRowStretch(layout.rowCount(), 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttons.accepted.connect(self.when_ok)
        main_layout.addWidget(self.buttons)
    
    def when_ok(self):
        self.close()
