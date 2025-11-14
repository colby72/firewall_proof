from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class Developers(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.all_developers()
        self.setWindowTitle(f"Developers - Firewall Proof {self.main_window.version}")
        self.setWindowIcon(QIcon("img/developer_community_github_icon.png"))
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