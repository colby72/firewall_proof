from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.company import *
from utils import *


class HomeGUI(QWidget):
    def __init__(self, main_window, project):
        QWidget.__init__(self)
        self.main_window = main_window
        self.project = project
        self.main_window.setWindowTitle(f"{self.project.name} - Firewall Proof {self.main_window.version}")
        # update menu actions
        enabled_actions = [
            self.main_window.save_action,
            self.main_window.save_as_action,
            self.main_window.close_action,
            self.main_window.home_action,
            self.main_window.add_company_action
        ]
        self.main_window.enable_actions(enabled_actions)
        disabled_actions = [
            self.main_window.company_submenu,
            self.main_window.firewall_submenu,
            self.main_window.policy_submenu,
            self.main_window.company_report_action
        ]
        self.main_window.disable_actions(disabled_actions)
        
        # widget design
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 100, 15)
        layout.setSpacing(10)
        self.setLayout(layout)

        # project title
        title = QLabel(f"{self.project.name}")
        layout.addWidget(title, 0, 0)

        # project companies
        for c in self.project.companies:
            company = QGroupBox("")
            company_layout = QGridLayout()
            company_layout.setContentsMargins(10, 10, 10, 10)
            company_layout.setSpacing(20)
            company.setLayout(company_layout)
            company_layout.addWidget(QLabel("Company : "), 0, 0)
            company_layout.addWidget(QLabel(c.name), 0, 1)
            company_layout.addWidget(QLabel("Firewalls : "), 1, 0)
            company_layout.addWidget(QLabel(str(len(c.fw_inventory))), 1, 1)
            view_button = QPushButton(" View")
            view_button.setIcon(QIcon("img/business_eye_focus_internet_security_icon.png"))
            view_button.clicked.connect(
                lambda checked, comp=c:
                self.view_company(comp)
            )
            view_button.setFixedSize(120, 30)
            view_button.setIconSize(QSize(18, 18))
            company_layout.addWidget(view_button, 2, 4)
            company_layout.setColumnStretch(company_layout.columnCount(), 1)
            layout.addWidget(company, 1, 0)
        
        # add company
        add_button = QPushButton(" Company")
        add_button.setIcon(QIcon("img/add_sign_icon.png"))
        add_button.clicked.connect(self.add_company)
        add_button.setObjectName("add_button")
        add_button.setFixedSize(140, 40)
        add_button.setIconSize(QSize(20, 20))
        layout.addWidget(add_button, 2, 0)

        layout.setColumnStretch(layout.columnCount(), 1)
        layout.setRowStretch(layout.rowCount(), 1)
        #layout.addStretch()
    
    def view_company(self, company):
        self.main_window.company = company
        self.main_window.show_company()
    
    def add_company(self, name):
        company_name, ok_pressed = QInputDialog.getText(self, "Add Company", "Company name")
        if ok_pressed and company_name:
            company = Company(company_name)
            self.project.add_company(company)
            self.main_window.show_home()