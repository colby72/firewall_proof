from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from core.rule import *
from algorithms.shift_rules import *


class ShiftRules(QDialog):
    def __init__(self, main_window, fw):
        super().__init__()
        self.main_window = main_window
        self.fw = fw
        self.setWindowTitle("Shift Firewall rules")
        layout = QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)
        # get mrules' min and max
        rule_min = fw.rules[0].number
        rule_max = fw.rules[0].number
        for r in fw.rules:
            if r.number<rule_min: rule_min=r.number
            if r.number>rule_max: rule_max=r.number
        # widget design
        layout.addWidget(QLabel("From : "), 0, 0)
        self.start = QSpinBox()
        self.start.setRange(rule_min, rule_max)
        self.start.setValue(rule_min)
        layout.addWidget(self.start, 0, 1)
        layout.addWidget(QLabel("To : "), 1, 0)
        self.end = QSpinBox()
        self.end.setRange(rule_min, rule_max)
        self.end.setValue(rule_max)
        layout.addWidget(self.end, 1, 1)
        layout.addWidget(QLabel("Shift by : "), 2, 0)
        self.gap = QSpinBox()
        self.gap.setRange(1, 50)
        self.gap.setValue(1)
        layout.addWidget(self.gap, 2, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons, 3, 1)
    
    def when_ok(self):
        start = self.start.value()
        end = self.end.value()
        gap = self.gap.value()
        shift_rules(self.fw, gap, start, end)
        self.close()
    
    def when_cancel(self):
        self.close()