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