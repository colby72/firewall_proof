import json
from cli.logger import *


class Service():
    def __init__(self, name, protocol, is_range=False):
        self.name = name # service name such as "ssh" or "http" or "ping-echo"
        self.protocol = protocol
        self.is_range = is_range
        self.port = None
        self.port_start = None
        self.port_end = None
        self.label = None # could be "TCP/22" or "UDP/301-305" or "GRE"

        if not self.name:
            self.auto_set_name()
        if not self.label:
            self.auto_set_label()
    
    def auto_set_name(self):
        with open('algorithms/common_ports.json', 'r', encoding="utf8") as f:
            common_ports = json.loads(f.read())
        self.auto_set_label()
        for p, s in common_ports.items():
            if self.label == p:
                self.name = s
                print_success(f"Service '{s}' detected and auto-assigned")
                return self.name
        print_warning("Auto service name could not be set")
        return None
    
    def auto_set_label(self):
        if not self.protocol:
            return None
        self.label = self.protocol
        if all([self.is_range, self.port_start, self.port_end]):
            self.label += f"/{self.port_start}-{self.port_end}"
        else:
            if self.port:
                self.label += f"/{self.port}"
        return self.label
    
    def set_name(self, name):
        self.name = name
    
    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_port(self, port):
        if not isinstance(port, int):
            try:
                port = int(port)
            except:
                return None
        if self.is_range:
            print_warning(f"Changing service '{self.name}' from range to single port")
        self.is_range = False
        self.port = port
        self.port_start = None
        self.port_end = None
        self.auto_set_label()
    
    def set_port_range(self, port_start, port_end):
        try:
            port_start = int(port_start)
            port_end = int(port_end)
        except:
            return None
        if port_start == port_end:
            self.set_port(port_start)
        if not self.is_range:
            print_warning(f"Changing service '{self.name}' from single port to range")
        self.is_range = True
        self.port = None
        self.port_start = port_start
        self.port_end = port_end
        self.auto_set_label()


class ServiceGroup():
    def __init__(self, name, services=[]):
        self.name = name
        self.services = services # list of ref to services
    
    def add_service(self, service):
        # verify if service already exists
        for s in self.services:
            if s.name == service.name:
                print_warning(f"Service '{s.name}' already exists in service group '{self.name}'")
                return None
        # add service
        self.services.append(service)
        return service