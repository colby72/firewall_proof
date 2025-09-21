from PyQt6.QtWidgets import *


class Information(QWidget):
    def __init__(self):
        super().__init__()
        self.information()
        self.setWindowTitle("About Firewall Proof")
        self.resize(510, 310)
    
    def information(self):
        # init global layout and  and tab bar
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # software presentation
        presentation = QWidget()
        pres_layout = QVBoxLayout()
        pres_layout.addWidget(QLabel("This is a presentation"))
        presentation.setLayout(pres_layout)

        # used libraries
        libraries = QWidget()
        libraries_layout = QVBoxLayout()
        libraries_layout.addWidget(QLabel("This is a list of libraries"))
        libraries.setLayout(libraries_layout)
        
        # software detailed description
        description = QWidget()
        description_layout = QVBoxLayout()
        description_layout.addWidget(QLabel("Detailed description"))
        description.setLayout(description_layout)
        
        # add tabs to global layout
        tabs.addTab(presentation, "Firewall Proof")
        tabs.addTab(libraries, "Libraries")
        tabs.addTab(description, "Software details")