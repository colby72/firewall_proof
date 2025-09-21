from PyQt6.QtWidgets import *


class Shortcuts(QWidget):
    def __init__(self):
        super().__init__()
        self.shortcuts()
        self.setWindowTitle("Shortcuts list")
        self.resize(410, 210)
    
    def shortcuts(self):
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        shortcut_list = {
            "Save": "Ctrl+S",
            "About software": "F1",
            "Developers list": "F2",
            "Shortcuts list": "F3"
        }
        for i, (a, s) in enumerate(shortcut_list.items()):
            action = QLabel(a)
            shortcut = QLabel(s)
            layout.addWidget(action, i, 0)
            layout.addWidget(shortcut, i, 1)

        layout.setRowStretch(layout.rowCount(), 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)