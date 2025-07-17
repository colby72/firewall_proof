from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel


class Developers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.all_developers()
        self.setWindowTitle("About developers")
        self.resize(410, 210)


    def all_developers(self):
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
        #self.setWindowTitle("About developers")
        #self.resize(410, 210)