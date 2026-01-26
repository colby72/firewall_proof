from ipaddress import IPv4Address, IPv4Network, ip_network, ip_address
import json

from cli.logger import *


with open('algorithms/ot_services.json', 'r', encoding="utf8") as f:
    ot_services = json.loads(f.read())


def hosts_by_zone(host_list):
    """
    INPUT: list of hosts objects
    OUTPUT: dict {"zone1": [h1, h3], "zone2": [h2, h4, h5]}
    """
    sorted_hosts = dict()
    for h in host_list:
        zone = h.zone
        if zone in sorted_hosts.keys():
            sorted_hosts[zone].append(h)
        else:
            sorted_hosts[zone] = [h]
    return sorted_hosts

def hosts_by_subnet(host_list):
    """
    INPUT: list of host objectshost
    OUTPUT: dict {"subnet1": [h1, h3], "subnet2": [h2, h4, h5]}
    """
    sorted_hosts = dict()
    for h in host_list:
        network = ip_network(h.address, False)
        if network in sorted_hosts.keys():
            sorted_hosts[network].append(h)
        else:
            sorted_hosts[network] = [h]
    return sorted_hosts

def subnet_zone_overlaps(firewall):
    '''
    INPUT: Firewall object
    OUTPUT: List of subnet-zone overlaps [(host_1, host_2, level), ...]
    OUTPUT: <level> can either be "info", "warning" or "critical"
    '''
    subnet_hosts = hosts_by_subnet(firewall.hosts)
    overlaps = []
    #print(f"Sorted by subnet: {sorted_hosts}")
    for subnet, hosts in subnet_hosts.items():
        if len(hosts)>1:
            i = 0
            while i < len(hosts)-1:
                for j in range(i+1, len(hosts)):
                    host_1 = hosts[i]
                    host_2 = hosts[j]
                    if host_1.zone.name != host_2.zone.name:
                        level = "info"
                        level_1 = float(host_1.zone.level) # Purdue level for host #1
                        level_2 = float(host_2.zone.level) # Purdue level for host #2
                        if (level_1 == level_2) or (level_1>=4 and level_2>=4) \
                        or (level_1<=2 and level_2<=2):
                            level = "info"
                        elif (level_1<=3 and level_2>=4) or (level_1>=4 and level_2<=3) \
                        or (abs(level_1-level_2) > 1):
                            level = "critical"
                        else:
                            level = "warning"
                        overlaps.append((host_1, host_2, level))
                i += 1
    return overlaps

def direct_it_ot_flows(firewall, vpn_required):
    '''host
    INPUT: Firewall object
    INPUT: vpn_required -> look into tunneled flows as well or not
    OUTPUT: List of breaches ['statement_1', 'statement_2']
    '''
    directs = []
    for rule in firewall.rules:
        if rule.vpn and (not vpn_required):
            continue
        # get source upper and lower levels
        src_upper = 0
        src_lower = 5
        for h in rule.src:
            if float(h.zone.level)>src_upper: src_upper = float(h.zone.level)
            if float(h.zone.level)<src_lower: src_lower = float(h.zone.level)
        # get destination uuper and lower levels
        dest_upper = 0
        dest_lower = 5
        for h in rule.dest:
            if float(h.zone.level)>dest_upper: dest_upper = float(h.zone.level)
            if float(h.zone.level)<dest_lower: dest_lower = float(h.zone.level)
        # look for issues
        tunnel = "a tunneled" if rule.vpn else "an untunneled"
        if src_upper<=3 and dest_lower>=4:
            directs.append(f"Rule <b>#{rule.number}</b> allows {tunnel} connection from OT domain (level {int(src_upper)}) to IT domain (level {int(dest_lower)})")
        elif src_lower>=4 and dest_upper<=3:
            directs.append(f"Rule <b>#{rule.number}</b> allows {tunnel} connection from IT domain (level {int(src_lower)}) to OT domain (level {int(dest_upper)})")
        else:
            pass
    return directs

def wrong_zone_attribution(firewall):
    '''
    INPUT: Firewall object
    OUTPUT: List of suspicious hosts [(host, [ot_svc_used], rule_id, level)]
    '''
    suspicious_hosts = []
    for rule in firewall.rules:
        applicable_svc = []
        for s in rule.services:
            # look for OT/ICS data flows
            if s in ot_services.keys(): applicable_svc.append(s)
        if applicable_svc:
            level = "info" if rule.status.compliant else "critical"
            for h in rule.src:
                if float(h.zone.level) >= 4:
                    suspicious_hosts.append((h, applicable_svc, rule.number, level))
            for h in rule.dest:
                if float(h.zone.level) >= 4:
                    suspicious_hosts.append((h, applicable_svc, rule.number, level))
    return suspicious_hosts

def vulnerable_services(firewall):
    """
    INPUT: Firewall object
    OUTPUT: list of tuples [(rule_number, vuln_service)]
    """
    vuln_services = []
    with open('algorithms/vulnerable_ports.json', 'r', encoding="utf8") as f:
        vulnerable_ports = json.loads(f.read())
    for rule in firewall.rules:
        for svc in rule.services:
            if svc in vulnerable_ports.keys():
                vuln_services.append((rule.number, svc, vulnerable_ports[svc]))
    return vuln_services