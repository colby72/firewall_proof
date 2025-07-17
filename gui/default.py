'''
Default Window:
First window to show when starting the software
'''

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Default(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        self.new_button = QPushButton("Create new project")
        self.new_button.clicked.connect(self.new_project)
        layout.addWidget(self.new_button, 2, 1)

        self.open_button = QPushButton("Open existing project")
        self.open_button.clicked.connect(self.open_project)
        layout.addWidget(self.open_button, 3, 1)

    def new_project(self):
        pass
    
    def open_project(self):
        pass