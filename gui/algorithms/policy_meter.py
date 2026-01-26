from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import json

from algorithms.policy_meter import policy_anomalies


class DialogPolicyMeter(QDialog):
    def __init__(self, main_window, policy):
        QWidget.__init__(self)
        self.main_window = main_window
        self.policy = policy
        self.setWindowTitle(f"{self.policy.name} - Policy meter")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)

        anomalies = policy_anomalies(self.policy)
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
        if anomalies[0]:
            label = QLabel("WARNING")
            label.setStyleSheet(f"""
                color: {colors["warning"]};
                font-weight: bold;
            """)
            layout.addWidget(label, row, 0)
            msg = f"Defaulf status <b> <span style='color:{self.policy.default.color}'>{self.policy.default.label}</span></b> is a compliant status. It's a best practice to have the default status a non-compliant"
            layout.addWidget(QLabel(msg), row, 1)
            row += 1
        for rule in anomalies[1]:
            # look for critical OT functions (L1-2) connected to DMZ
            if rule[1]:
                label = QLabel("WARNING")
                label.setStyleSheet(f"""
                    color: {colors["warning"]};
                    font-weight: bold;
                """)
                layout.addWidget(label, row, 0)
                msg = f"Policy rule <b>#{rule[0]}</b> allows critical OT functions to connectto OT DMZ"
                layout.addWidget(QLabel(msg), row, 1)
                row += 1
            # look for direct IT-OT connections not stopping at OT DMZ
            if rule[2]:
                label = QLabel("WARNING")
                label.setStyleSheet(f"""
                    color: {colors["warning"]};
                    font-weight: bold;
                """)
                layout.addWidget(label, row, 0)
                msg = f"Policy rule <b>#{rule[0]}</b> allows connection between IT and OT domains. It is a best practice to make all IT-OT connections stop at an OT DMZ."
                layout.addWidget(QLabel(msg), row, 1)
                row += 1
            # look for OT/ICS traffic beyond OT domain
            if rule[3]:
                #print(f"debug> {rule[3]}")
                label = QLabel(rule[3][0].upper())
                label.setStyleSheet(f"""
                    color: {colors[rule[3][0]]};
                    font-weight: bold;
                """)
                layout.addWidget(label, row, 0)
                applicable_svc = ', '.join(rule[3][1])
                msg = f"Policy rule <b>#{rule[0]}</b> allows OT data flows ({applicable_svc}) into untrusted DMZ ot IT domain."
                layout.addWidget(QLabel(msg), row, 1)
                row += 1
            # look for unencrypted and weak services
            if rule[4]:
                for j, s in enumerate(rule[4]):
                    label = QLabel("WARNING")
                    label.setStyleSheet(f"""
                        color: {colors["warning"]};
                        font-weight: bold;
                    """)
                    layout.addWidget(label, row, 0)
                    msg = f"Policy rule <b>#{rule[0]}</b> allows weak service {self.common_ports[rule[4][j][0]]} ({rule[4][j][0]}). Please consider using {self.common_ports[rule[4][j][1]]} ({rule[4][j][1]}) instead."
                    layout.addWidget(QLabel(msg), row, 1)
                    row += 1

        layout.setColumnStretch(layout.columnCount(), 1)
        layout.setRowStretch(layout.rowCount(), 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttons.accepted.connect(self.when_ok)
        main_layout.addWidget(self.buttons)

    def when_ok(self):
        self.close()