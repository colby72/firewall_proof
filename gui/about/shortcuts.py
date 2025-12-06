from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from utils import *


class Shortcuts(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.shortcuts()
        self.setWindowTitle(f"Shortcuts - Firewall Proof {self.main_window.version}")
        self.setWindowIcon(QIcon("img/share_social_media_network_connection_icon.png"))
        self.setStyleSheet(get_stylesheet("about.qss"))
        self.resize(410, 210)
    
    def shortcuts(self):
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        shortcut_list = {
            "New project": "Ctrl+N",
            "Open project": "Ctrl+O",
            "Save project": "Ctrl+S",
            "Close project": "Ctrl+W",
            "Quit": "Ctrl+Q",
            "Project home": "Ctrl+H",
            "Settings": "Ctrl+P",
            "About software": "F1",
            "Developers list": "F2",
            "Shortcuts list": "F3"
        }
        for i, (a, s) in enumerate(shortcut_list.items()):
            action = QLabel(a)
            shortcut = QLabel(s)
            shortcut.setObjectName("normal")
            layout.addWidget(action, i, 0)
            layout.addWidget(shortcut, i, 1)

        layout.setRowStretch(layout.rowCount(), 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)