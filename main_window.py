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
from gui.core.policy import *
from gui.core.firewall import *
from gui.core.host import *
from gui.edit.settings import *
from gui.dialogs.add_zone import *
from gui.dialogs.add_policy import *
from gui.dialogs.add_firewall import *
from gui.dialogs.add_interface import *
from gui.dialogs.add_host import *
from gui.dialogs.add_rule import *
from gui.dialogs.add_policy_rule import *
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

# import reporting functions
from reporting.company_report import *
from reporting.firewall_report import *


class FWProofGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('img/firewall3.png'))
        self.version = "v1.0.0-beta1"
        self.left = 60
        self.top = 60
        self.width = 1500
        self.height = 900
        self.toolbar_icon_size = 30
        self.init_ui()
        self.init_data()

        # Related sub windows
        self.windows = QStackedWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.windows)
        self.setCentralWidget(self.scroll_area)
        self.default = DefaultGUI(self)
        self.windows.addWidget(self.default)

    # related FW Proof data
    def init_data(self):
        self.file_path = None
        self.file_name = None
        self.project = None
        self.company = None
        self.firewall = None
        self.zone = None
        self.host = None
        self.policy = None

    def init_ui(self, parent=None):
        # General layout
        #self.setWindowTitle(f"Firewall Proof {self.version}")
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)

        # Create a menu bar
        menu = self.menuBar()

        # Create a root menu
        file_menu = menu.addMenu('File')
        edit_menu = menu.addMenu('Edit')
        project_menu = menu.addMenu('Project')
        dumb_ai_menu = menu.addMenu('Dumb AI')
        report_menu = menu.addMenu('Report')
        about_menu = menu.addMenu('About')

        """ 1. Create actions for File menu """
        self.new_action = QAction(QtGui.QIcon("img/file_new_blue_icon.png"), "New project", self)
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('New project')
        self.new_action.triggered.connect(self.new_project)

        self.open_action = QAction(QtGui.QIcon("img/file_open_icon.png"), "Open project", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open project")
        self.open_action.triggered.connect(self.open_project)

        self.save_as_action = QAction(QtGui.QIcon("img/floppy_disc_save_storage_disk_icon.png"), "Save project as", self)
        #self.save_as_action.setShortcut("Ctrl+S")
        self.save_as_action.setStatusTip("Save project as")
        self.save_as_action.triggered.connect(self.save_project_as)
        self.save_as_action.setDisabled(True)

        self.save_action = QAction(QtGui.QIcon("img/floppy_disc_save_storage_disk_icon.png"), "Save project", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setStatusTip("Save project")
        self.save_action.triggered.connect(self.save_project)
        self.save_action.setDisabled(True)

        self.close_action = QAction(QtGui.QIcon("img/close_remove_icon.png"), "Close project", self)
        self.close_action.setShortcut("Ctrl+W")
        self.close_action.setStatusTip("Close project")
        self.close_action.triggered.connect(self.close_project)
        self.close_action.setDisabled(True)

        quit_action = QAction(QtGui.QIcon("img/shutdown_red.png"), "Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit")
        quit_action.triggered.connect(self.quit)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addAction(self.close_action)
        file_menu.addAction(quit_action)

        """ 2. Create actions for Edit menu """
        self.settings_action = QAction(QtGui.QIcon("img/screwdriver_wrench_icon.png"), "Settings", self)
        self.settings_action.setShortcut("Ctrl+P")
        self.settings_action.setStatusTip("Edit preferences")
        self.settings_action.triggered.connect(self.show_settings)
        self.settings_action.setStatusTip("Settings")

        self.undo_action = QAction(QtGui.QIcon("img/undo_icon.png"), "Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo last action")
        self.undo_action.setDisabled(True)

        self.redo_action = QAction(QtGui.QIcon("img/redo_icon.png"), "Redo", self)
        self.redo_action.setShortcut("Ctrl+A")
        self.redo_action.setStatusTip("Redo last action")
        self.redo_action.setDisabled(True)

        edit_menu.addAction(self.settings_action)
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        """ 3. Create actions for Project menu """
        self.home_action = QAction(QtGui.QIcon("img/house_icon.png"), "Project home", self)
        self.home_action.setShortcut('Ctrl+H')
        self.home_action.setStatusTip('Project home')
        self.home_action.triggered.connect(self.show_home)
        self.home_action.setDisabled(True)

        self.add_company_action = QAction(QtGui.QIcon("img/office-building.png"), "Add new Company", self)
        #self.add_company_action.setShortcut('Ctrl+H')
        self.add_company_action.setStatusTip('New Company')
        self.add_company_action.triggered.connect(self.add_company)
        self.add_company_action.setDisabled(True)

        """ 3.1 Create actions for Company sub-menu """
        self.show_company_action = QAction(QtGui.QIcon("img/office-building.png"), "Show Company", self)
        #self.show_company_action.setShortcut('Ctrl+H')
        self.show_company_action.setStatusTip('Show Company')
        self.show_company_action.triggered.connect(self.show_company)
        self.show_company_action.setDisabled(True)

        self.add_firewall_action = QAction(QtGui.QIcon("img/firewall_add_icon.png"), "Add new Firewall", self)
        #self.add_firewall_action.setShortcut('Ctrl+H')
        self.add_firewall_action.setStatusTip('New Firewall')
        self.add_firewall_action.triggered.connect(self.add_firewall)
        self.add_firewall_action.setDisabled(True)

        self.add_zone_action = QAction(QtGui.QIcon("img/bx_category_icon.png"), "Add new Zone", self)
        #self.add_zone_action.setShortcut('Ctrl+H')
        self.add_zone_action.setStatusTip('New Zone')
        self.add_zone_action.triggered.connect(self.add_zone)
        self.add_zone_action.setDisabled(True)

        self.add_policy_action = QAction(QtGui.QIcon("img/agreement_conditions_contract_policy_terms_icon.png"), "Add new Policy", self)
        #self.add_policy_action.setShortcut('Ctrl+H')
        self.add_policy_action.setStatusTip('New Policy')
        self.add_policy_action.triggered.connect(self.add_policy)
        self.add_policy_action.setDisabled(True)

        """ 3.2 Create actions for Firewall sub-menu """
        self.show_firewall_action = QAction(QtGui.QIcon("img/firewall4.png"), "Show Firewall", self)
        #self.show_firewall_action.setShortcut('Ctrl+H')
        self.show_firewall_action.setStatusTip('Show Firewall')
        self.show_firewall_action.triggered.connect(self.show_firewall)
        self.show_firewall_action.setDisabled(True)

        self.add_interface_action = QAction(QtGui.QIcon("img/connection_server_center_connected_data_icon.png"), "Add new Interface", self)
        #self.add_interface_action.setShortcut('Ctrl+H')
        self.add_interface_action.setStatusTip('New Interface')
        self.add_interface_action.triggered.connect(self.add_interface)
        self.add_interface_action.setDisabled(True)

        self.add_host_action = QAction(QtGui.QIcon("img/computer_icon.png"), "Add new Host", self)
        #self.add_host_action.setShortcut('Ctrl+H')
        self.add_host_action.setStatusTip('New Host')
        self.add_host_action.triggered.connect(self.add_host)
        self.add_host_action.setDisabled(True)

        self.add_rule_action = QAction(QtGui.QIcon("img/antivirus_internet_lock_locked_protect_icon.png"), "Add new Rule", self)
        #self.add_rule_action.setShortcut('Ctrl+H')
        self.add_rule_action.setStatusTip('New Rule')
        self.add_rule_action.triggered.connect(self.add_rule)
        self.add_rule_action.setDisabled(True)

        """ 3.3 Create actions for Policy sub-menu """
        self.show_policy_action = QAction(QtGui.QIcon("img/agreement_conditions_contract_policy_terms_icon.png"), "Show Policy", self)
        #self.show_policy_action.setShortcut('Ctrl+H')
        self.show_policy_action.setStatusTip('View Policy')
        self.show_policy_action.triggered.connect(self.show_policy)
        self.show_policy_action.setDisabled(True)

        self.add_policy_rule_action = QAction(QtGui.QIcon("img/agreement_conditions_contract_policy_terms_icon.png"), "Add new Policy rule", self)
        #self.add_policy_rule_action.setShortcut('Ctrl+H')
        self.add_policy_rule_action.setStatusTip('Add Policy Rule')
        self.add_policy_rule_action.triggered.connect(self.add_policy_rule)
        self.add_policy_rule_action.setDisabled(True)

        project_menu.addAction(self.home_action)
        project_menu.addAction(self.add_company_action)
        self.company_submenu = project_menu.addMenu("Company")
        self.company_submenu.addAction(self.show_company_action)
        self.company_submenu.addAction(self.add_firewall_action)
        self.company_submenu.addAction(self.add_zone_action)
        self.company_submenu.addAction(self.add_policy_action)
        self.firewall_submenu = project_menu.addMenu("Firewall")
        self.firewall_submenu.addAction(self.show_firewall_action)
        self.firewall_submenu.addAction(self.add_interface_action)
        self.firewall_submenu.addAction(self.add_host_action)
        self.firewall_submenu.addAction(self.add_rule_action)
        self.policy_submenu = project_menu.addMenu("Policy")
        self.policy_submenu.addAction(self.show_policy_action)
        self.policy_submenu.addAction(self.add_policy_rule_action)

        """ 4. Create actions for DumbAI menu """

        """ 5. Create actions for Report menu """
        self.company_report_action = QAction(QtGui.QIcon("img/report_seo_analysis_pie_chart_icon.png"), "Company report", self)
        #self.company_report_action.setShortcut("Ctrl+A")
        self.company_report_action.setStatusTip("Generate company report")
        self.company_report_action.triggered.connect(self.generate_company_report)
        self.company_report_action.setDisabled(True)

        self.firewall_report_action = QAction(QtGui.QIcon("img/report_seo_analysis_pie_chart_icon.png"), "Firewall report", self)
        #self.firewall_report_action.setShortcut("Ctrl+A")
        self.firewall_report_action.setStatusTip("Generate firewall report")
        self.firewall_report_action.triggered.connect(self.generate_firewall_report)
        self.firewall_report_action.setDisabled(True)

        report_menu.addAction(self.company_report_action)
        report_menu.addAction(self.firewall_report_action)
        
        """ 6. Create actions for About menu """
        info_action = QAction(QtGui.QIcon("img/network_learn_info_information_media_icon.png"), "About software", self)
        info_action.setShortcut("F1")
        info_action.setStatusTip("About software")
        info_action.triggered.connect(self.show_software_info)

        developers_action = QAction(QtGui.QIcon("img/developer_community_github_icon.png"), "Developers", self)
        developers_action.setShortcut("F2")
        developers_action.setStatusTip("Show developers")
        developers_action.triggered.connect(self.show_developers)

        shortcuts_action = QAction(QtGui.QIcon("img/share_social_media_network_connection_icon.png"), "Shortcuts", self)
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
        self.toolbar.addAction(self.new_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.open_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.home_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.show_company_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.show_firewall_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.show_policy_action)
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
    def enable_actions(self, action_list):
        for a in action_list:
            if isinstance(a, QAction):
                a.setDisabled(False)
            elif isinstance(a, QMenu):
                for sub_a in a.actions():
                    sub_a.setDisabled(False)
    
    def disable_actions(self, action_list):
        for a in action_list:
            if isinstance(a, QAction):
                a.setDisabled(True)
            elif isinstance(a, QMenu):
                for sub_a in a.actions():
                    sub_a.setDisabled(True)

    ''' 1- Call functions for Menu: File '''
    def new_project(self):
        project_title, ok_pressed = QInputDialog.getText(self, "New project", "Project name")
        if ok_pressed and project_title:
            # create new project
            self.project = Project(project_title)
            # update menu actions
            enabled_actions = [self.save_action, self.close_action]
            self.enable_actions(enabled_actions)
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
        self.save_action.setDisabled(True)
        confirm_close = QMessageBox.question(self, "Close project", "Are you sure you want to close current project ?\nChanges unsaved will be lost.", buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        defaultButton=QMessageBox.StandardButton.No)
        if confirm_close == QMessageBox.StandardButton.Yes:
            self.init_data()
            # update menu actions
            disbaled_actions = [
                self.save_action,
                self.save_as_action,
                self.close_action,
                self.home_action,
                self.add_company_action,
                self.company_submenu,
                self.firewall_submenu,
                self.policy_submenu,
                self.company_report_action,
                self.firewall_report_action
            ]
            self.disable_actions(disbaled_actions)
            # show default widget
            self.setWindowTitle(f"Firewall Proof {self.version}")
            self.windows.setCurrentWidget(self.default)
    
    def quit(self):
        if QMessageBox.question(self,"Exit Firewall Proof", "Do you want to exit?",
                                QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes) == QMessageBox.StandardButton.Yes:
            self.close()
    
    ''' 2- Call functions for Menu: Edit '''
    def show_settings(self):
        self.settings_dialog = Settings(self)
        self.settings_dialog.show()
    
    ''' 3- Call functions for Menu: Project '''
    def show_home(self):
        if self.project:
            home = HomeGUI(self, self.project)
            self.windows.addWidget(home)
            self.windows.setCurrentWidget(home)
    
    def add_company(self):
        if self.project:
            company_name, ok_pressed = QInputDialog.getText(self, "Add Company", "Company name")
            if ok_pressed and company_name:
                company = Company(company_name)
                self.project.add_company(company)
                self.show_home()

    def show_company(self):
        if self.company:
            company_gui = CompanyGUI(self)
            self.windows.addWidget(company_gui)
            self.windows.setCurrentWidget(company_gui)
    
    def add_firewall(self):
        if self.company:
            self.add_fw_dialog = DialogAddFirewall(self, self.company)
            self.add_fw_dialog.exec()
            self.show_company()
    
    def add_zone(self):
        if self.company:
            self.add_zone_dialog = DialogAddZone(self, self.company)
            self.add_zone_dialog.exec()
            self.show_company()
    
    def add_policy(self):
        if self.company:
            self.add_policy_dialog = DialogAddPolicy(self, self.company)
            self.add_policy_dialog.exec()
            self.show_company()
    
    def show_firewall(self):
        if self.firewall:
            self.policy = self.firewall.policy
            firewall_gui = FirewallGUI(self, self.firewall)
            self.windows.addWidget(firewall_gui)
            self.windows.setCurrentWidget(firewall_gui)
    
    def add_interface(self):
        if self.firewall:
            self.add_iface_dialog = DialogAddInterface(self, self.firewall)
            self.add_iface_dialog.exec()
            self.show_firewall()
    
    def add_host(self):
        if self.firewall:
            self.add_host_dialog = DialogAddHost(self, self.firewall)
            self.add_host_dialog.exec()
            self.show_firewall()
    
    def add_rule(self):
        if self.firewall:
            self.add_rule_dialog = DialogAddRule(self, self.firewall)
            self.add_rule_dialog.exec()
            self.show_firewall()

    def show_host(self):
        if self.host:
            host_gui = HostGUI(self, host)
            self.windows.addWidget(host_gui)
            self.windows.setCurrentWidget(host_gui)
    
    def show_policy(self):
        if self.policy:
            policy_gui = PolicyGUI(self, self.policy)
            self.windows.addWidget(policy_gui)
            self.windows.setCurrentWidget(policy_gui)
    
    def add_policy_rule(self):
        if self.policy:
            self.add_policy_rule_dialog = DialogAddPolicyRule(self, self.policy)
            self.add_policy_rule_dialog.exec()
            self.show_policy()

    ''' 4- Call functions for Menu: DumbAI '''

    ''' 5- Call functions for Menu: Report '''
    def generate_company_report(self):
        if self.company:
            generate_company_report_tex(self.company)
    
    def generate_firewall_report(self):
        if self.firewall:
            generate_firewall_report_tex(self.firewall)
    
    ''' 6- Call functions for Menu: About '''
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
        policy = parse_policy(company, 'test_data/policy.json')
        company.add_policy(policy)
        for fw in company.fw_inventory:
            apply_policy(fw, policy)
        self.project = Project("Test project")
        self.project.add_company(company)
        # update menu actions
        self.save_action.setDisabled(False)
        self.close_action.setDisabled(False)
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

main_window = FWProofGUI()
sys.exit(app.exec())