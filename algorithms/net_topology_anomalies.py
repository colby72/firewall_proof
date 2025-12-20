from ipaddress import IPv4Address, IPv4Network, ip_network, ip_address


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

def find_net_overlaps(firewall):
    zone_hosts = hosts_by_zone(firewall.hosts)
    #print(f"Sorted by zone: {sorted_hosts}")
    for zone, hosts in zone_hosts.items():
        print(f"Zone : {zone.name}")
        for h in hosts:
            print(f"{h.name}", end="\t")
        print()
    subnet_hosts = hosts_by_subnet(firewall.hosts)
    #print(f"Sorted by subnet: {sorted_hosts}")
    for subnet, hosts in subnet_hosts.items():
        print(f"Subnet : {subnet}")
        for h in hosts:
            print(f"{h.name}", end="\t")
        print()
    
