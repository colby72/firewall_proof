# import software's GUI resources
import sys
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# import GUI components
from gui.home import *
from gui.default import *

from gui.about.information import *
from gui.about.developers import *

# import software's core resources
from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *


class FWProofGUI(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('img/firewall_lock_red_icon.png'))
        self.title = title
        self.left = 60
        self.top = 60
        self.width = 1100
        self.height = 600
        self.toolbar_icon_size = 30
        self.init_ui()

        # Related sub windows
        self.windows = QStackedWidget()
        self.setCentralWidget(self.windows)
        self.default = Default()
        self.windows.addWidget(self.default)
        #self.home = Home(self, fw_proof)

    def init_ui(self, parent=None):
        # General layout
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)

        # Create a menu bar
        menu = self.menuBar()

        # Create a root menu
        file_menu = menu.addMenu('File')
        edit_menu = menu.addMenu('Edit')
        fw_menu = menu.addMenu('Firewall')
        dumb_ai_menu = menu.addMenu('Dumb AI')
        report_menu = menu.addMenu('Report')
        about_menu = menu.addMenu('About')

        """ Create actions for file menu """
        new_action = QAction(QtGui.QIcon("img/file_new_blue_icon.png"), "New project", self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New project')
        new_action.triggered.connect(self.new_project)

        open_action = QAction(QtGui.QIcon("img/file_open_icon.png"), "Open project", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open project")
        open_action.triggered.connect(self.open_project)

        save_action = QAction(QtGui.QIcon("img/save_file_icon.png"), "Save project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save project")
        save_action.triggered.connect(self.save_project)

        quit_action = QAction(QtGui.QIcon("img/shutdown_red.png"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit")
        quit_action.triggered.connect(self.quit)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(quit_action)

        """ Create actions for edit menu """
        settings_action = QAction(QtGui.QIcon("img/settings_software_icon.png"), "Settings", self)
        #settings_action.setShortcut("Ctrl+Q")
        settings_action.setStatusTip("Settings")

        undo_action = QAction(QtGui.QIcon("img/undo.jpg"), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Undo last action")

        redo_action = QAction(QtGui.QIcon("img/redo.jpg"), "Redo", self)
        redo_action.setShortcut("Ctrl+A")
        redo_action.setStatusTip("Redo last action")

        edit_menu.addAction(settings_action)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        """ Create actions for about menu """
        info_action = QAction(QtGui.QIcon("img/info_grey_icon.png"), "About software", self)
        info_action.setShortcut("F1")
        info_action.setStatusTip("About software")
        info_action.triggered.connect(self.show_software_info)

        developers_action = QAction(QtGui.QIcon("img/coding_developer_icon.png"), "Developers", self)
        developers_action.setShortcut("F2")
        developers_action.setStatusTip("Show developers")
        developers_action.triggered.connect(self.show_developers)

        shortcuts_action = QAction(QtGui.QIcon("img/info_icon.png"), "Shortcuts", self)
        shortcuts_action.setShortcut("F3")
        shortcuts_action.setStatusTip("Show shortcuts")
        shortcuts_action.triggered.connect(self.show_shortcuts)

        about_menu.addAction(info_action)
        about_menu.addAction(developers_action)
        about_menu.addAction(shortcuts_action)
        

        #Create a statusbar
        self.statusBar().showMessage("Status Bar")

        # Create Tool Bar
        self.toolbar = self.addToolBar("ToolBar")

        # Add The Actions To Tool Bar
        self.toolbar.addAction(new_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(info_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(developers_action)
        self.toolbar.addSeparator()

        self.toolbar.setStyleSheet("background-color: rgb(250, 250, 250)")
        self.toolbar.setIconSize(QSize(self.toolbar_icon_size, self.toolbar_icon_size))

        # Create Vertical Layout for MenuBar
        self.mb_vboxlayout = QVBoxLayout(self)
        self.mb_hboxlayout = QHBoxLayout()

        # Add Menu Bar to Vertical Layout
        self.mb_hboxlayout.addWidget(menu)
        self.mb_vboxlayout.addLayout(self.mb_hboxlayout)

        #self.showMaximized()
        self.show()

    ''' ### Menu call functions ### '''
    ''' 1- Call functions for Menu: File '''
    def new_project(self):
        pass
    
    def open_project(self):
        pass
    
    def save_project(self):
        pass
    
    def quit(self):
        if QMessageBox.question(self, "FW Checker", "Do you want to exit?", QMessageBox.No | QMessageBox.Yes) == QMessageBox.Yes:
            self.close()
    def quit(self):
        self.close()
    
    ''' 5- Call functions for Menu: About '''
    def show_software_info(self):
        self.widget_software_info = Information()
        self.widget_software_info.show()
    
    def show_developers(self):
        self.widget_developers = Developers()
        self.widget_developers.show()
    
    def show_shortcuts(self):
        pass
    

app = QApplication(sys.argv)
title = "Firewall Proof v0.1-beta"

main_window = FWProofGUI(title)
sys.exit(app.exec())