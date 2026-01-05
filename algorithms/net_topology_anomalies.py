from ipaddress import IPv4Address, IPv4Network, ip_network, ip_address

from cli.logger import *


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
    INPUT: list of host objects
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
