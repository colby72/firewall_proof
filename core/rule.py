from core.company import *
from core.firewall import *
from core.host import *
from core.zone import *
from core.policy import *

from cli.logger import *

import time


class Rule():
    def __init__(self, number, src, dest, services):
        # filled in by user
        self.id = 0 # not used yet
        self.number = number # rule's number
        self.src = src # list of refs to source hosts
        self.dest = dest # list of refs to destination hosts
        self.services = services # list of authorized ports and services for this flow
        self.vpn = None # not used yet
        self.disabled = False # set to True only if rule is DISABLED

        # filled in by software
        self.status = None # rule's status (eg. OK, WARNING ...)
        self.date = time.strftime("%B %d. %Y") # last modification date

    def set_src(self, src):
        self.src = src
        self.date = time.strftime("%B %d. %Y")

    def set_dest(self, dest):
        self.dest = dest
        self.date = time.strftime("%B %d. %Y")

    def set_services(self, services):
        self.services = services
        self.date = time.strftime("%B %d. %Y")

    def set_status(self, status):
        self.status = status
        self.date = time.strftime("%B %d. %Y")
    
    def disable(self):
        self.disable = True
        self.date = time.strftime("%B %d. %Y")