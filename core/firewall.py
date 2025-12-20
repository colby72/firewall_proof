from core.company import *
from core.host import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *
from algorithms.policy_check import apply_policy


class Firewall():
    def __init__(self, company, name, vendor, address, policy=None):
        self.id = 0
        self.name = name
        self.company = company
        self.vendor = vendor
        self.address = address
        self.policy = policy # ref to FW policy object

        # firewall's components & elements
        self.interfaces = [] # list of refs to FW's interfaces
        self.hosts = [] # list of refs to FW's hosts
        self.groups = [] # list of refs to FW's object groups
        self.rules = [] # list of refs to FW's rules

    # Firewall management
    def set_name(self, name):
        self.name = name
    
    def set_vendor(self, vendor):
        self.vendor = vendor
    
    def set_address(self, address):
        self.address = address
    
    def set_policy(self, policy):
        self.policy = policy
        self.check_policy()
    
    # Firewall operations
    def add_interface(self, name, address):
        interface = FwInterface(name, address)
        self.interfaces.append(interface)
    
    def remove_interface(self, interface):
        self.interfaces.remove(interface)
    
    def add_host(self, host):
        # verify if host already exists
        for h in self.hosts:
            if h.name == host.name:
                print_warning(f"Host '{h.name}' already exists in Firewall '{self.name}'")
                return None
        # add host
        self.hosts.append(host)
        return host
    
    def remove_host(self, host):
        self.hosts.remove(host)
    
    def add_rule(self, rule):
        # verify if rule already exists
        for r in self.rules:
            if r.number == rule.number:
                r.set_src(rule.src)
                r.set_dest(rule.dest)
                r.set_services(rule.services)
                return r
        # add rule if new
        self.rules.append(rule)
    
    def remove_rule(self, rule):
        self.rules.remove(rule)
    
    def add_group(self, group):
        # verify if group already exists
        for g in self.groups:
            if g.name == group.name:
                print_warning(f"Group '{g.name}' already exists in Firewall '{self.name}'")
                return None
        # add group
        self.groups.append(group)
        return group
    
    def check_policy(self):
        apply_policy(self, self.policy)
    
    # stats & reporting functions
    def compliance_rate(self):
        if not self.policy:
            return 0
        compliant = 0
        for r in self.rules:
            if r.status.compliant: compliant += 1
        try:
            rate = round((compliant/len(self.rules))*100, 2)
        except:
            rate = 0
        return rate
    
    def status_stats(self):
        stats = {}
        #stats['total'] = len(self.rules)
        for r in self.rules:
            if r.status.label in stats.keys():
                stats[r.status.label] += 1
            else:
                stats[r.status.label] = 1
        return stats
    
    def sort_rules_by_number(self):
        self.rules.sort(key=lambda r: r.number)
    
    def sort_hosts_by_zone(self):
        self.hosts.sort(key=lambda h: (h.zone.level, h.name))
    
    def sort_objects(self):
        self.sort_rules_by_number()
        self.sort_hosts_by_zone()



class FwInterface():
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def set_name(self,name):
        self.name = name
    
    def set_address(self, address):
        self.address = address