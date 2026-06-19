from core.company import *
from core.firewall import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *


class Host():
    def __init__(self, firewall, name, zone, address="127.0.0.1/32", fqdn=None, ifce=None):
        self.id = 0 # not used yet
        self.name = name
        self.firewall = firewall # ref to parent Firewall
        self.zone = zone # ref to zone
        self.address = address # host IP address (format: a.b.c.d/range)
        self.fqdn = fqdn # fqdn name
        self.interface = ifce
        self.nat = [] # not used yet
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
    
    def set_fqdn(self, fqdn):
        self.fqdn = fqdn
    
    def set_interface(self, ifce):
        self.interface = ifce
    
    def set_category(self, category):
        self.category = category
    
    def set_os(self, os):
        self.os = os
    
    # host information
    def get_ip(self):
        return self.address.split('/')[0]

    def get_mask(self):
        return int(self.address.split('/')[1])
    
    # GUI properties
    def get_tooltip(self):
        tooltip = ""
        if self.zone:
            tooltip += f"Zone: {self.zone.name}"
        if self.address:
            tooltip += f"\nIP: {self.address}"
        if self.fqdn:
            tooltip += f"\nFQDN: {self.fqdn}"
        return tooltip.strip('\n')


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
            return None
        zone = self.hosts[0].zone
        for h in self.hosts:
            if (not h.zone) or (zone.name != h.zone.name):
                self.zone = None
        self.zone = zone
    
    # GUI properties
    def get_tooltip(self):
        #tooltip = "\n".join([f"[+] {x.name}: {x.address}" for x in host.hosts])
        tooltip = ""
        if self.zone:
            tooltip += f"Zone: {self.zone.name}"
        for h in self.hosts:
            if h.address:
                tooltip += f"\n[+] {h.name}: {h.address}"
            elif h.fqdn:
                tooltip += f"\n[+] {h.name}: {h.fqdn}"
            else:
                tooltip += f"\n[+] {h.name}"
        return tooltip.strip('\n')