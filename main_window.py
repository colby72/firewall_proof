# import software's GUI resources
import sys, os
from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from project import *

# import GUI components
from gui.home import *
from gui.default import *
from gui.core.company import *
from gui.core.firewall import *
from gui.core.host import *

from gui.about.information import *
from gui.about.developers import *
from gui.about.shortcuts import *

# import software's core resources
from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *

# import file processing functions
from file.save_file import *
from file.open_file import *

# import data algorithms
from algorithms.parse_policy import *
from algorithms.policy_check import *


class FWProofGUI(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('img/firewall_lock_red_icon.png'))
        self.title = title
        self.left = 60
        self.top = 60
        self.width = 1500
        self.height = 900
        self.toolbar_icon_size = 30
        self.init_ui()
        self.init_data()

        # Related sub windows
        self.windows = QStackedWidget()
        self.setCentralWidget(self.windows)
        self.default = DefaultGUI(self)
        self.windows.addWidget(self.default)
        #self.home = Home(self, fw_proof)

    # related FW Proof data
    def init_data(self):
        self.file_path = None
        self.file_name = None
        self.project = None
        self.company = None

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

        self.close_action = QAction(QtGui.QIcon("img/close_remove_icon.png"), "Close project", self)
        self.close_action.setShortcut("Ctrl+X")
        self.close_action.setStatusTip("Close project")
        self.close_action.triggered.connect(self.close_project)

        quit_action = QAction(QtGui.QIcon("img/shutdown_red.png"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit")
        quit_action.triggered.connect(self.quit)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(self.close_action)
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
        project_title, ok_pressed = QInputDialog.getText(self, "New project", "Project name")
        if ok_pressed and project_title:
            # create new project
            self.project = Project(project_title)
            # show project's home
            home = HomeGUI(self, self.project)
            self.windows.addWidget(home)
            self.windows.setCurrentWidget(home)
        elif ok_pressed and (project_title==""):
            alert = QMessageBox.critical(self, "New project", "Project name cannot be empty !", buttons=QMessageBox.StandardButton.Ok)
        else:
            alert = QMessageBox.critical(self, "New project", "Project name entered invalid !", buttons=QMessageBox.StandardButton.Ok)
    
    def open_project(self):
        self.open_file_dialog = QFileDialog.getOpenFileName(self, "Open project ...", "", "FwProof files (*.fwp);;All files (*)")
        selected_file = self.open_file_dialog[0]
        if selected_file:
            # read opened file
            file_path, file_name = os.path.split(selected_file)
            project = open_file(file_name, file_path)
            # set main window's data variables 
            self.file_path = file_path
            self.file_name = file_name
            self.project = project
            # show project's home
            home = HomeGUI(self, self.project)
            self.windows.addWidget(home)
            self.windows.setCurrentWidget(home)
    
    def save_project(self):
        if not (self.file_name and self.file_path):
            self.save_project_as()
        else:
            save_file(self.project, self.file_name, self.file_path)
    
    def save_project_as(self):
        if not self.project:
            pass # alert box
            return None
        self.save_file_dialog = QFileDialog.getSaveFileName(self, "Save project ...", self.project.name.replace(' ', '_').lower(), "FwProof files (*.fwp);;All files (*)")
        target_file = self.save_file_dialog[0]
        if target_file:
            file_path, file_name = os.path.split(target_file)
            save_file(self.project, file_name, file_path)
            self.file_path = file_path
            self.file_name = file_name
    
    def close_project(self):
        confirm_close = QMessageBox.question(self, "Close project", "Are you sure you want to close current project ?\nChanges unsaved will be lost.", buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.No)
        if confirm_close == QMessageBox.StandardButton.Yes:
            self.init_data()
            self.windows.setCurrentWidget(self.default)
    
    def quit(self):
        if QMessageBox.question(self,"Exit Firewall Proof", "Do you want to exit?",
                                QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes) == QMessageBox.StandardButton.Yes:
            self.close()
    
    ''' 5- Call functions for Menu: About '''
    def show_software_info(self):
        self.widget_software_info = Information()
        self.widget_software_info.show()
    
    def show_developers(self):
        self.widget_developers = Developers()
        self.widget_developers.show()
    
    def show_shortcuts(self):
        self.widget_shortcuts = Shortcuts()
        self.widget_shortcuts.show()
    
    ''' X- Call functions for Test Widgets '''
    def display_home(self):
        company = parse_fwp_json('test_data/space_y.json')
        policy = parse_policy('test_data/policy.json')
        for fw in company.fw_inventory:
            apply_policy(fw, policy)
        self.project = Project("Test project")
        self.project.add_company(company)
        self.company = company
        # display the project
        home = HomeGUI(self, self.project)
        self.windows.addWidget(home)
        self.windows.setCurrentWidget(home)

    def display_company(self):
        company = parse_fwp_json('test_data/space_y.json')
        policy = parse_policy('test_data/policy.json')
        for fw in company.fw_inventory:
            apply_policy(fw, policy)
        self.company = company
        #print(f"display company '{self.company.name}'")
        company_gui = CompanyGUI(self)
        self.windows.addWidget(company_gui)
        self.windows.setCurrentWidget(company_gui)
    
    def display_firewall(self):
        company = parse_fwp_json('test_data/space_y.json')
        policy = parse_policy('test_data/policy.json')
        for fw in company.fw_inventory:
            apply_policy(fw, policy)
        self.company = company
        # choose a random firewall to display
        fw = self.company.fw_inventory[0]
        firewall_gui = FirewallGUI(self, fw)
        self.windows.addWidget(firewall_gui)
        self.windows.setCurrentWidget(firewall_gui)
    
    def display_host(self):
        company = parse_fwp_json('test_data/space_y.json')
        policy = parse_policy('test_data/policy.json')
        for fw in company.fw_inventory:
            apply_policy(fw, policy)
        self.company = company
        # choose a random host to display
        print(f"len = {len(self.company.fw_inventory[0].hosts)}")
        print(f"type = {type(self.company.fw_inventory[0].hosts[0])}")
        host = self.company.fw_inventory[0].hosts[4]
        host_gui = HostGUI(self, host)
        self.windows.addWidget(host_gui)
        self.windows.setCurrentWidget(host_gui)


app = QApplication(sys.argv)
title = "Firewall Proof v0.1-beta"

main_window = FWProofGUI(title)
sys.exit(app.exec())