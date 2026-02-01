from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import datetime
from utils import *


class Information(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.information()
        self.setWindowTitle(f"About Firewall Proof {self.main_window.version}")
        self.setWindowIcon(QIcon("img/network_learn_info_information_media_icon.png"))
        self.setStyleSheet(get_stylesheet("about.qss"))
        #self.resize(410, 210)
        self.setFixedSize(600, 420)
    
    def information(self):
        # init global layout and  and tab bar
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # software presentation
        presentation = QWidget()
        pres_layout = QGridLayout()
        pres_layout.setContentsMargins(15, 15, 15, 15)
        pres_layout.setSpacing(10)
        presentation.setLayout(pres_layout)
        
        logo = QLabel()
        logo.resize(150, 150)
        logo_pixmap = QPixmap('img/logo05.png')
        logo_scaled = logo_pixmap.scaled(logo.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        logo.setPixmap(logo_scaled)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        software_banner = QLabel(f"Firewall Proof {self.main_window.version}")
        software_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        software_banner.setObjectName("banner")
        brief_pres = QLabel("Firewall compliance audit tool")
        brief_pres.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brief_pres.setObjectName("normal")
        pres_layout.addWidget(logo, 0, 0)
        pres_layout.addWidget(software_banner, 1, 0)
        pres_layout.addWidget(brief_pres, 2, 0)
        pres_layout.setRowStretch(pres_layout.rowCount(), 1)

        # used libraries
        libraries = QWidget()
        lib_scroll_area = QScrollArea()
        lib_scroll_area.setWidgetResizable(True)
        lib_scroll_area.setWidget(libraries)
        libraries_layout = QGridLayout()
        libraries_layout.setContentsMargins(15, 15, 15, 15)
        libraries_layout.setSpacing(10)
        libraries.setLayout(libraries_layout)

        package_title = QLabel("Python packages")
        package_title.setObjectName('title')
        packages = [
            "PyQt6 - GNU GPL v3",
            "superqt - BSD-3-Clause",
            "jsonpickle - BSD-3-Clause",
            "colorama - BSD-3-Clause",
            "jinja2 - BSD-3-Clause",
            "matplotlib",
            "docxtpl - LGPL v2.1",
            "docx - MIT license",
            "spire-doc free - e-iceblue",
            "xhtml2pdf - Apache 2.0" 
        ]
        libraries_layout.addWidget(package_title, 0, 0)
        for i, p in enumerate(packages):
            package_label = QLabel(p)
            package_label.setObjectName("normal")
            libraries_layout.addWidget(package_label, i+1, 0)
        software_title = QLabel("Third-party software")
        software_title.setObjectName("title")
        softwares = [
            "pdflatex (Linux)",
            "MikTeX or any other LaTeX editor (Windows)",
        ]
        libraries_layout.addWidget(software_title, 0, 1)
        for i, s in enumerate(softwares):
            software_label = QLabel(s)
            software_label.setObjectName("normal")
            libraries_layout.addWidget(software_label, i+1, 1)
        libraries_layout.setRowStretch(libraries_layout.rowCount(), 1)
        libraries_layout.setColumnStretch(libraries_layout.columnCount(), 1)
        
        # software detailed description
        description = QWidget()
        desc_scroll_area = QScrollArea()
        desc_scroll_area.setWidgetResizable(True)
        desc_scroll_area.setWidget(description)
        description_layout = QGridLayout()
        description_layout.setContentsMargins(15, 15, 15, 15)
        description_layout.setSpacing(10)
        description.setLayout(description_layout)
        
        desc_header = QLabel("Description")
        desc_header.setObjectName("paragraph_title")
        description_layout.addWidget(desc_header, 0, 0)
        paragraph_1 = "Firewall compliance audit tool, designed to allow " \
            "organizations to audit their Firewalls flow matrix against a set of rules, " \
            "namely a security policy. It can uncover potential misconfigurations or " \
            "security flaws."
        paragraph_2 = "To put it straight, a Firewall whose only rule <b>'allows'</b>" \
            " flows from <b>'all'</b> source objects to <b>'all'</b> destinations " \
            "on <b>'any'</b> service, well ... it's fairly useless actually."
        paragraph_3 = "For an efficient secure network filtering, a Firewall " \
            "shall at least be configured with a set of rules that ensure network " \
            "segregation between different object groups and network zones, " \
            "following a block-all allow-required basis. These rules can further " \
            "enhanced by restricting network subnets or tunneling sensitive " \
            "communications (using IPSec for example)."
        
        paragraphs = [paragraph_1, paragraph_2, paragraph_3]
        for i, p in enumerate(paragraphs):
            par = QLabel(p)
            par.setWordWrap(True)
            par.setObjectName("paragraph")
            par.setAlignment(Qt.AlignmentFlag.AlignJustify)
            description_layout.addWidget(par, i+1, 0)
        description_layout.setRowStretch(description_layout.rowCount(), 1)
        #description_layout.setColumnStretch(description_layout.columnCount(), 1)

        # license
        license_tab = QWidget()
        lic_scroll_area = QScrollArea()
        lic_scroll_area.setWidgetResizable(True)
        lic_scroll_area.setWidget(license_tab)
        license_layout = QGridLayout()
        license_layout.setContentsMargins(15, 15, 15, 15)
        license_layout.setSpacing(10)
        license_tab.setLayout(license_layout)
        
        license_1 = f"Firewall Proof {self.main_window.version} - Firewall compliance audit tool"\
            f"\nCopyright (C) {datetime.date.today().year}  Ramy Chemak"
        license_2 = "This work is licensed under the <a href='https://www.gnu.org/licenses/gpl-3.0.html'>"\
            "GNU General Public License, version 3 or (at your option) any later version</a>."
        license_3 = "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;"\
            " without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. "\
            "See the GNU General Public License for more details."
        license_4 = "For any commercial or professional use, please first send an email to "\
            "<b>ramy.software@protonmail.com</b>. Commercial use would be allowed in certain situations."
        
        licenses = [license_1, license_2, license_3, license_4]
        for i, p in enumerate(licenses):
            par = QLabel(p)
            par.setWordWrap(True)
            par.setObjectName("paragraph")
            par.setAlignment(Qt.AlignmentFlag.AlignJustify)
            par.setOpenExternalLinks(True)
            license_layout.addWidget(par, i, 0)
        license_layout.setRowStretch(license_layout.rowCount(), 1)

        # add tabs to global layout
        tabs.addTab(presentation, "Firewall Proof")
        tabs.addTab(lib_scroll_area, "Libraries")
        tabs.addTab(desc_scroll_area, "Software details")
        tabs.addTab(lic_scroll_area, "License")