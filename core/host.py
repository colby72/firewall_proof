from core.company import *
from core.firewall import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *


class Host():
    def __init__(self, firewall, name, zone, address=["127.0.0.1/32"]):
        self.id = 0 # not used yet
        self.name = name
        self.firewall = firewall # ref to parent Firewall
        self.zone = zone # ref to zone
        self.address = address # list of host IP addresses (format: xxx.xxx.xxx.xxx/range)
        self.nat = None # not used yet
        self.group = None # list of refs to object's groups
        self.os = None # not used yet
    
    # host management
    def set_name(self, name):
        self.name = name

    def set_zone(self, zone):
        self.zone = zone
    
    def add_to_group(self, group):
        self.group = group
        group.add_host(self)

    def set_address(self, address):
        self.address = address

    # host information
    def get_ip(self):
        return self.address.split('/')[0]

    def get_mask(self):
        return int(self.address.split('/')[1])


class ObjGroup():
    def __init__(self, name, zone):
        self.id = 0
        self.name = name
        self.zone = zone
        self.hosts = []
    
    def set_name(self, name):
        self.name = name
    
    def set_zone(self, zone):
        self.zone = zone
    
    def add_host(self, host):
        if not host in self.hosts:
            self.hosts.append(host)
            host.add_to_group(self)
        