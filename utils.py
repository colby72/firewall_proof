from core.service import *
from cli.logger import *

import ipaddress


def get_zone_by_name(company, zone_name):
    for z in company.zones:
        if z.name == zone_name:
            return z
    print_error(f"Zone '{zone_name}' not found in Company '{company.name}'")
    return None

def get_status_by_label(company, label):
    for status in company.status_list:
        if status.label == label:
            return status
    print_error(f"Status '{label}' not found in Company '{company.name}'")
    return None

def get_status_list_labels(company):
    labels = [status.label for status in company.status_list]
    return labels

def get_policy_by_name(company, policy_name):
    for p in company.policies:
        if p.name == policy_name:
            return p
    print_error(f"Policy '{policy_name}' not found in Company '{company.name}'")
    return None

def get_fw_ifce_by_name(firewall, ifce_name):
    for ifce in firewall.interfaces:
        if ifce.name == ifce_name:
            return ifce
    print_error(f"Interface '{ifce_name}' not found in Firewall '{firewall.name}'")
    return None

def get_service_by_name(firewall, svc_name):
    for svc in firewall.services:
        if svc.name == svc_name:
            return svc
    print_error(f"Service '{svc_name}' not found in Firewall '{firewall.name}'")
    return None

def get_svc_grp_by_name(firewall, grp_name):
    for grp in firewall.svc_groups:
        if grp.name == grp_name:
            return grp
    print_error(f"Service group '{grp_name}' not found in Firewall '{firewall.name}'")
    return None

def get_host_by_name(firewall, host_name):
    for host in firewall.hosts:
        if host.name == host_name:
            return host
    print_error(f"Host '{host_name}' not found in Firewall '{firewall.name}'")
    return None

def get_host_by_address(firewall, addr):
    for host in firewall.hosts:
        if host.address == addr:
            return host
    print_error(f"No host with address '{addr}' found in Firewall '{firewall.name}'")
    return None

def get_host_grp_by_name(firewall, grp_name):
    for grp in firewall.groups:
        if grp.name == grp_name:
            return grp
    print_error(f"Host group '{grp_name}' not found in Firewall '{firewall.name}'")
    return None

def create_svc_from_label(label):
    """
    Instantiate Service object from label such as 'GRE', 'UDP/123', 'TCP/800-805'
    """
    if isinstance(label, str) and ('/' in label):
        # parse raw service and create new Service instance
        tmp = label.split('/')
        new_service = Service(None, tmp[0])
        if '-' in tmp[1]:
            tmp2 = tmp[1].split('-')
            try:
                port_start = int(tmp2[0])
                port_end = int(tmp2[1])
                new_service.set_port_range(port_start, port_end)
            except:
                print_error(f"Service '{label}' seems to be a port range, but format error found")
                return None
        else:
            try:
                port = int(tmp[1])
                new_service.set_port(port)
            except:
                print_error(f"Format error found in service '{label}'")
                return None
        new_service.auto_set_name()
        new_service.auto_set_label()
        return new_service

def create_service_from_range(name, protocol, port_range):
    """
    INPUT: array (eg. ['21'], ['451', '1451'], ['80', '150-155'])
    OUTPUT: List of Service objects
    """
    svc_list = []
    for p in port_range:
        if '-' in p:
            tmp = p.split('-')
            try:
                port_start, port_end = int(tmp[0]), int(tmp[1])
            except:
                print_error(f"Couldn't parse port range '{port_range}'")
                continue
            svc = Service(None, None, is_range=True)
            svc.set_port_range(port_start, port_end)
            svc_list.append(svc)
        else:
            try:
                port = int(p)
            except:
                print_error(f"Couldn't parse port range '{port_range}'")
                continue
            svc = Service(name, protocol, is_range=False)
            svc.set_port(port)
            svc_list.append(svc)
    return svc_list

def mask_to_cidr(mask):
    net = ipaddress.IPv4Network(f"0.0.0.0/{mask}")
    if mask != str(net.netmask):
        print_error(f"'{mask}' is a host mask, not a subnet mask")
        return None
    return net.prefixlen

def cidr_to_mask(prefix):
    return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)

def is_ip(ip):
    try:
        x = ipaddress.ip_address(ip)
    except:
        print_warning(f"'{ip}' is not recognized as a valid IP address")
        return False
    return True

def get_port_by_name(svc_name):
    """
    INPUT: Service name: 'RFB/VNC Server', 'Kaspersky AV', 'timestamp'
    OUTPUT: Port label: UDP/5900, TCP/8086, ICMP/13
    """
    with open('algorithms/common_ports.json', 'r', encoding="utf8") as f:
        common_ports = json.loads(f.read())
        for p, s in common_ports.items():
            if s == svc_name:
                return p
    return None

def text_to_tex(text):
    """
    Format text to be Latex-compatible
    Escape Latex special chars
    """
    text = text.replace('&', '\&')
    return text

def get_stylesheet(sheet_file):
    with open(f"gui/qss/{sheet_file}", 'r', encoding="utf8") as f:
        style = f.read()
        return style