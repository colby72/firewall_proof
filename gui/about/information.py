from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTabBar, QWidget


class Information(QMainWindow):
    def __init__(self):
        super().__init__()
        self.information()
        self.setWindowTitle("Information")
        self.resize(410, 210)
    
    def information(self):
        # init global layout and  and tab bar
        layout = QVBoxLayout()
        tabs = QTabBar()
        # software presentation
        presentation = QWidget()
        p_layout = QVBoxLayout()
        presentation.setLayout(p_layout)
        # used libraries
        libraries = QWidget()
        # software detailed description
        description = QWidget()
        # add tabs to global layout
        tabs.addTab("Firewall Proof")
        tabs.addTab("Libraries")
        tabs.addTab("Software details")
        layout.addWidget(tabs)
        self.setLayout(layout)


    def developers(self):
        vbox = QVBoxLayout()
        developer_1 = QLabel('-- CHEMAK Ramy', self)
        developer_1.move(30, 20)
        developer_1.setFixedWidth(260)
        developer_2 = QLabel('Arabelle Solutions', self)
        developer_2.move(30, 50)
        developer_2.setFixedWidth(260)

        vbox.addWidget(developer_1)
        vbox.addWidget(developer_2)

        self.setLayout(vbox)
        self.setWindowTitle("About developers")
        self.resize(410, 210)