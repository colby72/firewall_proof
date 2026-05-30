from core.company import *
from core.firewall import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *


class Host():
    def __init__(self, firewall, name, zone, address=["127.0.0.1/32"], fqdn=[], ifce=None):
        self.id = 0 # not used yet
        self.name = name
        self.firewall = firewall # ref to parent Firewall
        self.zone = zone # ref to zone
        self.address = address # list of host IP addresses (format: a.b.c.d/range)
        self.fqdn = fqdn # list of fqdn names
        self.interface = ifce
        self.nat = None # not used yet
        self.group = None # list of refs to object's groups
        self.category = "desktop" # can be "desktop", "net_device", "server", "hypervisor"
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
    def __init__(self, name, zone=None):
        self.name = name
        self.zone = zone # ref to zone
        self.hosts = [] # list of refs to hosts
    
    def set_name(self, name):
        self.name = name
    
    def set_zone(self, zone):
        self.zone = zone
    
    def add_host(self, host):
        if not host in self.hosts:
            self.hosts.append(host)
            host.add_to_group(self)
    
    def auto_set_zone(self):
        if not self.hosts:
            self.zone = None
        zone = self.hosts[0].zone
        for h in self.hosts:
            if zone.name != h.zone.name:
                self.zone = None
        self.zone = zone