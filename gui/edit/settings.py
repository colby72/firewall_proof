from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import os, shutil


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
        report_layout.setSpacing(10)
        report_tab.setLayout(report_layout)

        report_layout.addWidget(QLabel("Default report format : "), 0, 0)
        self.default_report_format = QComboBox()
        self.default_report_format.addItems(["Latex", "HTML", "Docx"])
        self.default_report_format.setCurrentText(self.main_window.report_format)
        report_layout.addWidget(self.default_report_format, 0, 1)

        # company default templates
        company_defaults = QGroupBox("Company reports")
        company_defaults_layout = QGridLayout()
        company_defaults_layout.setContentsMargins(10, 10, 10, 10)
        company_defaults_layout.setSpacing(10)
        company_defaults.setLayout(company_defaults_layout)
        
        company_defaults_layout.addWidget(QLabel("HTML template : "), 0, 0)
        self.company_html = QLabel(self.main_window.company_html_template)
        company_defaults_layout.addWidget(self.company_html, 0, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.company_html:
            self.edit_template(t, 'html')
        )
        company_defaults_layout.addWidget(edit_button, 0, 2)
        
        company_defaults_layout.addWidget(QLabel("Docx template : "), 1, 0)
        self.company_docx = QLabel(self.main_window.company_docx_template)
        company_defaults_layout.addWidget(self.company_docx, 1, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.company_docx:
            self.edit_template(t, 'docx')
        )
        company_defaults_layout.addWidget(edit_button, 1, 2)
        
        company_defaults_layout.addWidget(QLabel("Tex template : "), 2, 0)
        self.company_tex = QLabel(self.main_window.company_tex_template)
        company_defaults_layout.addWidget(self.company_tex, 2, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.company_tex:
            self.edit_template(t, 'tex')
        )
        company_defaults_layout.addWidget(edit_button, 2, 2)
        
        report_layout.addWidget(company_defaults, 1, 0, 1, 3)

        # firewall default templates
        fw_defaults = QGroupBox("Firewall reports")
        fw_defaults_layout = QGridLayout()
        fw_defaults_layout.setContentsMargins(10, 10, 10, 10)
        fw_defaults_layout.setSpacing(10)
        fw_defaults.setLayout(fw_defaults_layout)
        
        fw_defaults_layout.addWidget(QLabel("HTML template : "), 0, 0)
        self.fw_html = QLabel(self.main_window.firewall_html_template)
        fw_defaults_layout.addWidget(self.fw_html, 0, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.fw_html:
            self.edit_template(t, 'html')
        )
        fw_defaults_layout.addWidget(edit_button, 0, 2)

        fw_defaults_layout.addWidget(QLabel("Docx template : "), 1, 0)
        self.fw_docx = QLabel(self.main_window.firewall_docx_template)
        fw_defaults_layout.addWidget(self.fw_docx, 1, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.fw_docx:
            self.edit_template(t, 'docx')
        )
        fw_defaults_layout.addWidget(edit_button, 1, 2)

        fw_defaults_layout.addWidget(QLabel("Tex template : "), 2, 0)
        self.fw_tex = QLabel(self.main_window.firewall_tex_template)
        fw_defaults_layout.addWidget(self.fw_tex, 2, 1)
        edit_button = QPushButton("...")
        edit_button.setFixedSize(40, 25)
        edit_button.clicked.connect(
            lambda checked, t=self.fw_tex:
            self.edit_template(t, 'tex')
        )
        fw_defaults_layout.addWidget(edit_button, 2, 2)

        report_layout.addWidget(fw_defaults, 2, 0, 1, 3)

        report_layout.setRowStretch(report_layout.rowCount(), 1)

        # add tabs to global layout and buttons
        tabs.addTab(general_tab, "General")
        tabs.addTab(report_tab, "Reporting")

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.when_ok)
        self.buttons.rejected.connect(self.when_cancel)
        layout.addWidget(self.buttons)
    
    def edit_template(self, template, format):
        open_file_dialog = QFileDialog.getOpenFileName(self, "Open project ...", "", "FwProof files (*.j2);;All files (*)")
        selected_path = open_file_dialog[0]
        selected_file = os.path.split(selected_path)[1]
        shutil.copy(selected_path, 'reporting/templates/')
        template.setText(selected_file)

    
    def when_ok(self):
        # get generatl settings
        self.main_window.status_per_row = self.status_per_row.value()
        self.main_window.hosts_per_row = self.hosts_per_row.value()
        # get report settings
        self.main_window.report_format = self.default_report_format.currentText()
        self.main_window.company_html_template = self.company_html.text()
        self.main_window.company_docx_template = self.company_docx.text()
        self.main_window.company_tex_template = self.company_tex.text()
        self.main_window.firewall_html_template = self.fw_html.text()
        self.main_window.firewall_docx_template = self.fw_docx.text()
        self.main_window.firewall_tex_template = self.fw_tex.text()
        self.close()
    
    def when_cancel(self):
        self.close()