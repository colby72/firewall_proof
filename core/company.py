from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *


class Company():
    def __init__(self, name):
        self.id = 0 # not used
        self.name = name # comapny's name
        self.fw_inventory = [] # list of refs to company's Firewalls
        self.zones = [] # list of refs to company's zones
    
    # company management
    def set_name(self, name):
        self.name = name
    
    # company operations
    def add_zone(self, zone):
        # verify if zone already exists
        for z in self.zones:
            if zone.name==z.name:
                print_warning(f"Zone '{z.name}' already exists for company '{self.name}")
                return None
        # add Zone
        self.zones.append(zone)
        print_info(f"Zone '{zone.name}' added to company '{self.name}")
        return zone
    
    def add_firewall(self, firewall):
        # verify if Firewall already exists in FW inventory
        for fw in self.fw_inventory:
            if fw.name == firewall.name:
                print_warning(f"Firewall '{fw.name}' already exists for company '{self.name}'")
                return None
        # add Firewall
        firewall.company = self
        self.fw_inventory.append(firewall)
        print_info(f"Firewall '{firewall.name}' added to company '{self.name}'")
        return firewall