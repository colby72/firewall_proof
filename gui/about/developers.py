from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from utils import *


class Developers(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.all_developers()
        self.setWindowTitle(f"Developers - Firewall Proof {self.main_window.version}")
        self.setWindowIcon(QIcon("img/developer_community_github_icon.png"))
        self.setStyleSheet(get_stylesheet("about.qss"))
        self.resize(410, 210)


    def all_developers(self):
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        developer_title = QLabel("Developers")
        developer_title.setObjectName('title')
        developer_1 = QLabel('Ramy CHEMAK')
        developer_1.setObjectName("normal")

        contributors_title = QLabel("Contributors & Donors")
        contributors_title.setObjectName('title')
        
        layout.addWidget(developer_title, 0, 0)
        layout.addWidget(developer_1, 1, 0)
        layout.addWidget(QLabel(), 2, 0)
        layout.addWidget(contributors_title, 3, 0)
        layout.setRowStretch(layout.rowCount(), 1)
        layout.setColumnStretch(layout.columnCount(), 1)