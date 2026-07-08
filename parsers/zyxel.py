from core.firewall import *
from core.rule import *
from core.service import *
from core.policy import *
from core.host import *

from cli.logger import *
from utils import *


def parse_interface(interface_raw):
    interface = dict()
    for line in interface_raw:
        line = line.strip()
        if line.startswith("interface"):
            name = line.split("interface")[1].strip()
            interface['name'] = name
        elif line.startswith("ip address"):
            address = line.split("ip address")[1].strip()
            ip = address.split(' ')[0]
            mask = address.split(' ')[1]
            if is_ip(ip) and is_ip(mask):
                interface['address'] = f"{ip}/{mask_to_cidr(mask)}"
        else:
            pass
    return interface

def parse_address(address_raw):
    address = dict()
    x = address_raw.split(' ')
    address['name'] = x[1]
    if "fqdn" in address_raw:
        address['type'] = "fqdn"
        address['fqdn'] = x[x.index("fqdn")+1]
    elif "interface-subnet" in x:
        address['type'] = "interface-subnet"
        address['subnet'] = x[x.index("interface-subnet")+1]
    elif "interface-ip" in x:
        address['type'] = "interface-ip"
        address['subnet'] = x[x.index("interface-ip")+1]
    elif is_ip(x[2].split('/')[0]):
        ip = x[2]
        # add /32 CIDR to standalone addresses
        if not ('/' in ip): ip += "/32"
        # store data
        address['type'] = "ip"
        address['ip'] = ip
    else:
        print(f"Could not parse address-object '{address_raw}'") # warning
    return address

def parse_address_group(address_group_raw):
    group = {"name": "", "members": []}
    for line in address_group_raw:
        line = line.strip()
        if line.startswith("object-group address"):
            group['name'] = line.split("object-group address")[1].strip()
        elif line.startswith("address-object"):
            member = line.split("address-object")[1].strip()
            group['members'].append(member)
        else:
            pass
    return group

def parse_service(service_raw):
    service = dict()
    x = service_raw.split(' ')
    service['name'] = x[1]
    if "tcp eq" in service_raw:
        service['type'] = "port"
        port = int(x[x.index("eq")+1])
        service['protocol'] = "TCP"
        service['port'] = port
    elif "udp eq" in service_raw:
        service['type'] = "port"
        port = int(x[x.index("eq")+1])
        service['protocol'] = "UDP"
        service['port'] = port
    elif "tcp range" in service_raw:
        service['type'] = "range"
        port_start = int(x[x.index("range")+1])
        port_end = int(x[x.index("range")+2])
        service['protocol'] = "TCP"
        service['port_start'] = port_start
        service['port_end'] = port_end
    elif "udp range" in service_raw:
        service['type'] = "range"
        port_start = int(x[x.index("range")+1])
        port_end = int(x[x.index("range")+2])
        service['protocol'] = "UDP"
        service['port_start'] = port_start
        service['port_end'] = port_end
    elif "icmp " in service_raw:
        service['type'] = "icmp"
        service['port'] = x[x.index("icmp")+1]
    elif "icmpv6 " in service_raw:
        service['type'] = "icmp"
        service['port'] = x[x.index("icmpv6")+1]
    elif "protocol" in service_raw:
        service['type'] = "protocol"
        service['protocol_nb'] = int(x[x.index("protocol")+1])
    else:
        pass
    return service

def parse_service_group(svc_group_raw):
    group = {"name": "", "members": []}
    for line in svc_group_raw:
        line = line.strip()
        if line.startswith("object-group service"):
            group['name'] = line.split("object-group service")[1].strip()
        elif line.startswith("service-object"):
            member = line.split("service-object")[1].strip()
            group['members'].append(member)
        else:
            pass
    return group

def parse_zone(zone_raw):
    zone = {"name": "", "members": []}
    for line in zone_raw:
        line = line.strip()
        if line.startswith("zone "):
            zone['name'] = line.split("zone")[1].strip()
        elif line.startswith("interface "):
            member = line.split("interface")[1].strip()
            zone['members'].append(member)
        else:
            pass
    return zone

def parse_policy(policy_raw):
    rule = dict()
    for line in policy_raw:
        line = line.strip()
        if line.startswith("secure-policy "):
            number = line.split("secure-policy")[1].strip()
            rule['number'] = number
        elif line.startswith("from "):
            src_ifce = line.split("from")[1].strip()
            rule['src_ifce'] = src_ifce
        elif line.startswith("to "):
            dest_ifce = line.split("to")[1].strip()
            rule['dest_ifce'] = dest_ifce
        elif line.startswith("sourceip "):
            src_addr = line.split("sourceip")[1].strip()
            rule['src_addr'] = src_addr
        elif line.startswith("destinationip "):
            dest_addr = line.split("destinationip")[1].strip()
            rule['dest_addr'] = dest_addr
        elif line.startswith("service "):
            service = line.split("service")[1].strip()
            rule['service'] = service
        else:
            pass
    return rule

def get_zyxel_data(config_file):
    extracts = [] # get raw extracts
    # parsed data to return
    data = {
        "interface": [],
        "address": [],
        "address_group": [],
        "service": [],
        "svc_group": [],
        "zone": [],
        "policy": [],
    }

    # parsing temp variables
    capture = False
    chunk = []
    label = None

    with open(config_file, 'r') as f:
        for line in f.readlines():
            # get hostname
            if "hostname " in line:
                hostname = line.split("hostname")[1].strip().strip('\n')
                data['hostname'] = hostname.replace('"', '')
            # get interfaces
            elif line.startswith("interface "):
                capture = True
                label = "interface"
                #continue
            # get address objects
            elif line.startswith("address-object "):
                extracts.append(("address", line.strip()))
            # get object groups
            elif line.startswith("object-group address"):
                capture = True
                label = "address_group"
                #continue
            # get service objects
            elif line.startswith("service-object "):
                extracts.append(("service", line.strip()))
            # get service object groups
            elif line.startswith("object-group service "):
                capture = True
                label = "svc_group"
                #continue
            # get zones
            elif line.startswith("zone "):
                capture = True
                label = "zone"
                #continue
            # get policy rules
            elif line.startswith("secure-policy "):
                capture = True
                label = "policy"
                #continue
            # stop capture
            elif line.strip() == '!':
                #if label: extracts[label] = chunk
                if label: extracts.append((label, chunk))
                # init variables
                capture = False
                chunk = []
                label = None
            else:
                pass
            if capture:
                chunk.append(line.strip())
    
    for label, chunk in extracts:
        if label == "interface":
            #print(f"debug> label {label}")
            #print(f"debug> chunk {chunk}")
            data[label].append(parse_interface(chunk))
        elif label == "address":
            data[label].append(parse_address(chunk))
        elif label == "address_group":
            data[label].append(parse_address_group(chunk))
        elif label == "service":
            data[label].append(parse_service(chunk))
        elif label == "svc_group":
            data[label].append(parse_service_group(chunk))
        elif label == "zone":
            data[label].append(parse_zone(chunk))
        elif label == "policy":
            data[label].append(parse_policy(chunk))
        else:
            print(f"Skipping '{label}' unrecognized label while parsing Zyxel Firewall") # warning
    
    return data


def parse_zyxel_config(config_file):
    """
    Generate a Firewall object from a parsed Zyxel config
    INPUT: Config file -> str
    OUTPUT: Firewall object
    """

    print_info(f"Parsing Zyxel config file {config_file} ...")

    # intatiate Firewall object
    config = get_zyxel_data(config_file)
    firewall = Firewall(None, config['hostname'], "Zyxel", None)

    # add Firewall interfaces
    if "interface" in config.keys():
        for ifce in config['interface']:
            if "address" in ifce.keys():
                interface = firewall.add_interface(ifce['name'], ifce['address'])
                print_info(f"Interface '{interface.name}' added to Firewall ...")

    # add hosts
    if "address" in config.keys():
        for addr in config['address']:
            name = addr['name']
            if not ("type"in addr.keys()):
                print_warning(f"Address type for '{name}' is <unknown>")
                continue
            if addr['type'] == "ip":
                host = Host(firewall, name, zone=None, address=addr['ip'])
                host = firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "fqdn":
                host = Host(firewall, name, zone=None, address=None, fqdn=addr['fqdn'])
                host = firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "interface-ip":
                ifce = get_fw_ifce_by_name(firewall, addr['subnet'])
                if ifce:
                    host = Host(firewall, name, zone=None, address=ifce.address)
                else:
                    host = Host(firewall, name, zone=None, address=None)
                host = firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "interface-subnet":
                ifce = get_fw_ifce_by_name(firewall, addr['subnet'])
                if ifce:
                    host = Host(firewall, name, zone=None, address=ifce.address)
                else:
                    host = Host(firewall, name, zone=None, address=None)
                host = firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            else:
                print_warning(f"Address type for '{name}' is <unknown>")

    # add host groups
    if "address_group" in config.keys():
        for grp in config['address_group']:
            group = ObjGroup(grp['name'])
            for host_name in grp['members']:
                host = get_host_by_name(firewall, host_name)
                if host:
                    group.add_host(host)
            group = firewall.add_group(group)
            print_info(f"Host group '{group.name}' added to Firewall ...")

    # add services
    if "service" in config.keys():
        for svc in config['service']:
            name = svc['name']
            if svc['type'] == "port":
                service = Service(name, svc['protocol'])
                service.set_port(svc['port'])
                service = firewall.add_service(service)
                print_info(f"Service '{service.name}' added to Firewall ...")
            elif svc['type'] == "range":
                service = Service(name, svc['protocol'])
                service.set_port_range(svc['port_start'], svc['port_end'])
                service = firewall.add_service(service)
                print_info(f"Service '{service.name}' added to Firewall ...")
            elif svc['type'] == "icmp":
                service = Service(name, "ICMP")
                if isinstance(svc['port'], int):
                    service.set_port(svc['port'])
                if isinstance(svc['port'], str):
                    label = get_port_by_name(svc['port'])
                    if label:
                        port = label.split('/')[1]
                        service.set_port(port)
                service = firewall.add_service(service)
                print_info(f"Service '{service.name}' added to Firewall ...")
            elif svc['type'] == "protocol":
                pass # temp
            else:
                print_warning(f"Service type for '{name}' is <unknown>")
    
    # add service groups
    if "svc_group" in config.keys():
        for grp in config['svc_group']:
            svc_group = ServiceGroup(grp['name'])
            for svc_name in grp['members']:
                svc = get_service_by_name(firewall, svc_name)
                if svc:
                    svc_group.add_service(svc)
            firewall.add_svc_group(svc_group)
            print_info(f"Service group '{svc_group.name}' added to Firewall")

    # add rules
    if "policy" in config.keys():
        for r in config['policy']:
            # get rule's number
            try:
                nb = int(r['number'])
            except:
                continue
            # get rule's source object
            src = []
            if "src_addr" in r.keys():
                host = get_host_by_name(firewall, r['src_addr'])
                if host:
                    src.append(host)
            # get rule's dest object
            dest = []
            if "dest_addr" in r.keys():
                host = get_host_by_name(firewall, r['dest_addr'])
                if host:
                    dest.append(host)
            # get rule's source interface
            src_ifce = []
            if "src_ifce" in r.keys():
                ifce = get_fw_ifce_by_name(firewall, r['src_ifce'])
                if ifce:
                    src_ifce.append(ifce)
            # get rule's dest interface
            dest_ifce = []
            if "dest_ifce" in r.keys():
                ifce = get_fw_ifce_by_name(firewall, r['dest_ifce'])
                if ifce:
                    dest_ifce.append(ifce)
            # get rule's service
            services = []
            if "service" in r.keys():
                svc = get_service_by_name(firewall, r['service'])
                svc_grp = get_svc_grp_by_name(firewall, r['service'])
                if svc:
                    services.append(svc)
                if svc_grp:
                    services.append(svc_grp)
            # check if source is an interface
            if src_ifce and (not src):
                for i in src_ifce:
                    host = get_host_by_address(firewall, i.address)
                    if host:
                        src.append(host)
            # check if dest is an interface
            if dest_ifce and (not dest):
                for i in dest_ifce:
                    host = get_host_by_address(firewall, i.address)
                    if host:
                        dest.append(host)
            # initiate rule
            rule = Rule(nb, src, dest, services)
            rule.set_src_ifce(src_ifce)
            rule.set_dest_ifce(dest_ifce)
            # check if rule is disabled
            # TODO
            firewall.add_rule(rule)
            print_info(f"Rule #{rule.number} added to Firewall")
    
    return firewall


'''
config = get_zyxel_data("../../config-USG60_micro.conf")

print(f"debug keys > {config.keys()}\n")

if "hostname" in config.keys():
    print(f"hostname >> {config['hostname']}\n")

if "interface" in config.keys():
    for ifce in config['interface']:
        print(f"ifce >> {ifce}")
    print()

if "address" in config.keys():
    for addr in config['address']:
        print(f"address >> {addr}")
    print()

if "address_group" in config.keys():
    for grp in config['address_group']:
        print(f"address grp >> {grp}")
    print()

if "service" in config.keys():
    for svc in config['service']:
        print(f"service >> {svc}")
    print()

if "svc_group" in config.keys():
    for svc in config['svc_group']:
        print(f"svc group >> {svc}")
    print()

if "zone" in config.keys():
    for zone in config['zone']:
        print(f"zone >> {zone}")
    print()

if "policy" in config.keys():
    for rule in config['policy']:
        print(f"rule >> {rule}")
    print()
'''