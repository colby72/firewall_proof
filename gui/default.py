'''
Default Window:
First window to show when starting the software
'''

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from algorithms.parse_policy import *
from algorithms.policy_check import *
from parsers.fwp_json import *

from gui.core.company import *


class DefaultGUI(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        layout.addWidget(QLabel(), 0, 0, 1, 1)
        layout.addWidget(QLabel(), 0, 2, 1, 1)

        self.new_button = QPushButton("Create new project")
        self.new_button.clicked.connect(self.new_project)
        layout.addWidget(self.new_button, 1, 1, 1, 1)

        self.open_button = QPushButton("Open project")
        self.open_button.clicked.connect(self.open_project)
        layout.addWidget(self.open_button, 2, 1, 1, 1)

        self.company_button = QPushButton("Test Company")
        self.company_button.clicked.connect(self.test_company)
        layout.addWidget(self.company_button, 3, 1, 1, 1)

        self.firewall_button = QPushButton("Test Firewall")
        self.firewall_button.clicked.connect(self.test_firewall)
        layout.addWidget(self.firewall_button, 4, 1, 1, 1)

        self.host_button = QPushButton("Test Host")
        self.host_button.clicked.connect(self.test_host)
        layout.addWidget(self.host_button, 5, 1, 1, 1)

        self.project_button = QPushButton("Test Project")
        self.project_button.clicked.connect(self.test_project)
        layout.addWidget(self.project_button, 6, 1, 1, 1)

        layout.setRowStretch(layout.rowCount(), 1)
        self.setLayout(layout)

    def new_project(self):
        self.main_window.new_project()
    
    def open_project(self):
        self.main_window.open_project()
    
    def test_company(self):
        #company = parse_fwp_json('test_data/space_y.json')
        #self.main_window.comapny = company
        self.main_window.display_company()
    
    def test_firewall(self):
        self.main_window.display_firewall()
    
    def test_host(self):
        self.main_window.display_host()
    
    def test_project(self):
        self.main_window.display_home()