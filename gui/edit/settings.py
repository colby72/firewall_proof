from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class Settings(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle(f"Settings - Firewall Proof {self.main_window.version}")
        self.setWindowIcon(QIcon("img/screwdriver_wrench_icon.png"))
        self.resize(400, 410)

        # widget design
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # general settings tab
        general_tab = QWidget()
        general_layout = QGridLayout()
        general_layout.setContentsMargins(15, 15, 15, 15)
        general_tab.setLayout(general_layout)

        general_layout.addWidget(QLabel("# Status per row : "), 0, 0)
        self.status_per_row = QSpinBox()
        self.status_per_row.setRange(3, 6)
        self.status_per_row.setValue(self.main_window.status_per_row)
        general_layout.addWidget(self.status_per_row, 0, 1)
        general_layout.addWidget(QLabel("# Hosts per row : "), 1, 0)
        self.hosts_per_row = QSpinBox()
        self.hosts_per_row.setRange(3, 7)
        self.hosts_per_row.setValue(self.main_window.hosts_per_row)
        general_layout.addWidget(self.hosts_per_row, 1, 1)
        general_layout.setRowStretch(general_layout.rowCount(), 1)

        # report settings tab
        report_tab = QWidget()
        report_layout = QGridLayout()
        report_layout.setContentsMargins(15, 15, 15, 15)
        report_tab.setLayout(report_layout)

        report_layout.addWidget(QLabel("Default report format : "), 0, 0)
        self.default_report_format = QComboBox()
        self.default_report_format.addItems(["Latex", "HTML", "Docx"])
        self.default_report_format.setCurrentText(self.main_window.report_format)
        report_layout.addWidget(self.default_report_format, 0, 1)
        report_layout.setRowStretch(report_layout.rowCount(), 1)

        # add tabs to global layout and buttons
        tabs.addTab(general_tab, "General")
        tabs.addTab(report_tab, "Reporting")

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons)
    
    def when_ok(self):
        # get generatl settings
        status_per_row = self.status_per_row.value()
        hosts_per_row = self.hosts_per_row.value()
        # get report settings
        default_report_format = self.default_report_format.currentText()
        # apply settings
        self.main_window.status_per_row = status_per_row
        self.main_window.hosts_per_row = hosts_per_row
        self.main_window.report_format = default_report_format
        self.close()
    
    def when_cancel(self):
        self.close()