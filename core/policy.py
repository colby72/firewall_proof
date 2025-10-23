from core.company import *
from core.firewall import *
from core.host import *
from core.zone import *
from core.rule import *


class FWPolicy():
    def __init__(self, company, name, default="NOK"):
        self.id = 0 # not used yet
        self.company = company # ref to parent company
        self.name = name # policy's name for referencing purpose
        self.default = default # deault status if no policy matches
        self.rules = []
    
    def set_name(self, name):
        self.name = name
    
    def set_default(self, default):
        self.default = default


class PolicyRule():
    def __init__(self, src_zone, dest_zone, services, vpn, status):
        self.src_zone = src_zone
        self.dest_zone = dest_zone
        self.services = services
        self.vpn = vpn
        self.status = status
    
    def set_src_zone(self, src_zone):
        self.src_zone = src_zone
    
    def set_dest_zone(self, dest_zone):
        self.dest_zone = dest_zone
    
    def set_services(self, services):
        self.services = services
    
    def set_vpn(self, vpn):
        self.vpn = vpn
    
    def set_status(self, status):
        self.status = status