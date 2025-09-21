'''
Default Window:
First window to show when starting the software
'''

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Firewall(QWidget):
    def __init__(self, fw):
        QWidget.__init__(self)
        self.fw = fw
        self.setWindowTitle(f"{fw.name} | {fw.company.name}")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 