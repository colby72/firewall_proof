from PyQt6.QtWidgets import *


class Developers(QWidget):
    def __init__(self):
        super().__init__()
        self.all_developers()
        self.setWindowTitle("About developers")
        self.resize(410, 210)


    def all_developers(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(15, 15, 15, 15)
        vbox.setSpacing(10)
        developer_1 = QLabel('-- CHEMAK Ramy')
        developer_2 = QLabel('Arabelle Solutions')

        vbox.addWidget(developer_1)
        vbox.addWidget(developer_2)
        vbox.addStretch()
        self.setLayout(vbox)