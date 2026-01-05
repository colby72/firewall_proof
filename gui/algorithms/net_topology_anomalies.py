from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from algorithms.net_topology_anomalies import subnet_zone_overlaps


class DialogNetTopologyAnomalies(QDialog):
    def __init__(self, main_window, fw):
        QWidget.__init__(self)
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle(f"{self.fw.name} - Network topology anomalies")

        overlaps = subnet_zone_overlaps(self.fw)
        colors = {"info": "#0000e0", "warning": "#f4bf14", "critical": "#ff0000"}
        
        # widget design
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        for i in range(len(overlaps)):
            h1, h2, level = overlaps[i]
            label = QLabel(level.upper())
            label.setStyleSheet(f"""
                color: {colors[level]};
                font-weight: bold;
            """)
            layout.addWidget(label, i, 0)
            msg = f"{h1.name} ({h1.zone.name}) and {h2.name} ({h2.zone.name}) share the same subnet while belonging to different zones"
            layout.addWidget(QLabel(msg), i, 1)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttons.accepted.connect(self.when_ok)
        layout.addWidget(self.buttons, len(overlaps)+1, 1)
    
    def when_ok(self):
        self.close()
