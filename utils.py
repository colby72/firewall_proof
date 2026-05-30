from core.service import *
from cli.logger import *


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