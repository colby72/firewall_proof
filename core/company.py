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
        self.policies = [] # list of refs to company's policies
        self.status_list = [] # list of refs to RuleStatus
    
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
    
    def remove_zone(self, zone):
        self.zones.remove(zone)
    
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
    
    def remove_firewall(self, firewall):
        self.fw_inventory.remove(firewall)
    
    def add_policy(self, policy):
        # verify if policy already exists
        for pol in self.policies:
            if pol.name == policy.name:
                print_warning(f"Policy '{pol.name}' already exists for company '{self.name}'")
                return None
        # add policy
        self.policies.append(policy)
        print_info(f"Policy '{policy.name}' added to company '{self.name}'")
        return policy
    
    def remove_policy(self, policy):
        self.policies.remove(policy)
    
    def add_status(self, status):
        # verify if status already exists
        for st in self.status_list:
            if st.label == status.label:
                print_warning(f"Status '{st.label}' already exists for company '{self.name}'")
                return None
        # add status
        self.status_list.append(status)
        print_info(f"Status '{status.label}' added to company '{self.name}'")
        return status
    
    def remove_status(self, status):
        self.status_list.remove(status)


class RuleStatus():
    def __init__(self, label, color="#00FF00"):
        self.label = label
        self.color = color
    
    def set_label(self, label):
        self.label = label
    
    def set_color(self, color):
        self.color = color