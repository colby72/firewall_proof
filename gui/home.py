from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class HomeGUI(QWidget):
    def __init__(self, main_window, project):
        QWidget.__init__(self)
        self.main_window = main_window
        self.project = project
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        self.setLayout(layout)

        # project title
        title = QLabel(f"{self.project.name}")
        layout.addWidget(title)

        # project companies
        for c in self.project.companies:
            company = QGroupBox("")
            company_layout = QGridLayout()
            company_layout.setContentsMargins(10, 10, 10, 10)
            company_layout.setSpacing(10)
            company.setLayout(company_layout)
            company_layout.addWidget(QLabel("Company : "), 0, 0)
            company_layout.addWidget(QLabel(c.name), 0, 1)
            company_layout.addWidget(QLabel("Firewalls : "), 1, 0)
            company_layout.addWidget(QLabel(str(len(c.fw_inventory))), 1, 1)
            view_button = QPushButton("View")
            view_button.clicked.connect(
                lambda checked:
                self.view_company(c)
            )
            company_layout.addWidget(view_button, 2, 3)
            layout.addWidget(company)

        layout.addStretch()
    
    def view_company(self, company):
        self.main_window.company = company
        self.main_window.show_company()
        