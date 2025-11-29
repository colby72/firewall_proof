from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *
from core.policy import *

from cli.logger import *


class Project():
    def __init__(self, name):
        self.name = name
        self.companies = [] # list of refs to Company objects

    def set_name(self, name):
        self.name = name

    def add_company(self, company):
        for c in self.companies:
            if c.name == company.name:
                print_error(f"Company '{company.name}' already exists !")
                return None
        self.companies.append(company)
        return company
    
    def remove_company(self, company):
        self.companies.remove(company)