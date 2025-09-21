from PyQt6.QtWidgets import *


class Information(QWidget):
    def __init__(self):
        super().__init__()
        self.information()
        self.setWindowTitle("About Firewall Proof")
        self.resize(410, 210)
    
    def information(self):
        # init global layout and  and tab bar
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # software presentation
        presentation = QWidget()
        pres_layout = QVBoxLayout()
        pres_layout.setContentsMargins(15, 15, 15, 15)
        pres_layout.addWidget(QLabel("This is a presentation"))
        pres_layout.addStretch()
        presentation.setLayout(pres_layout)

        # used libraries
        libraries = QWidget()
        libraries_layout = QVBoxLayout()
        libraries_layout.setContentsMargins(15, 15, 15, 15)
        libraries_layout.addWidget(QLabel("This is a list of libraries"))
        libraries_layout.addStretch()
        libraries.setLayout(libraries_layout)
        
        # software detailed description
        description = QWidget()
        description_layout = QVBoxLayout()
        description_layout.setContentsMargins(15, 15, 15, 15)
        description_layout.addWidget(QLabel("Detailed description"))
        description_layout.addStretch()
        description.setLayout(description_layout)
        
        # add tabs to global layout
        tabs.addTab(presentation, "Firewall Proof")
        tabs.addTab(libraries, "Libraries")
        tabs.addTab(description, "Software details")