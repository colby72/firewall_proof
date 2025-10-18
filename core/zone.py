from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.policy import *

from cli.logger import *


class Zone():
    def __init__(self, name, level, description=None, color="#174EFF"):
        self.id = 0 # not used yet
        self.name = name # eg. "DMZ", "IIS-SL2", ...
        self.level = level # Purdue level
        self.description = description # brief description

        self.color = color
    
    # zone settings
    def set_name(self, name):
        self.name = name
    
    def set_level(self, level):
        self.level = level