from core.firewall import *
from core.rule import *
from core.service import *
from core.policy import *
from core.host import *

from cli.logger import *
from utils import *


def get_hostname(global_raw):
    for l in global_raw:
        l = l.strip()
        pattern = "set hostname"
        if pattern in l:
            hostname = l.split(pattern)[1].strip().strip('\n')
            return hostname
    return None

def get_items(raw_block):
    item_list = []
    capture = False
    chunk = []
    for l in raw_block:
        # start capturing data
        if l.startswith("edit"):
            capture = True
            label = l.split("edit")[1].strip()
            continue
        # end capturing data
        if l.startswith("next"):
            item_list.append({
                'label': label,
                'data': chunk
            })
            capture = False
            chunk = []
        # capturing data
        if capture:
            chunk.append(l)
    return item_list

def parse_interfaces(ifce_raw):
    interfaces_list = []
    chunk_list = get_items(ifce_raw)
    for item in chunk_list:
        ifce = dict()
        ifce['label'] = item['label'].replace('"', '')
        for x in item['data']:
            # get interface's alias
            if "set alias" in x:
                alias = x.split(' ')[2].replace('"', '')
                ifce['name'] = f"{ifce['label']} ({alias})"
            # get interface's ip and mask
            if "set ip" in x:
                tmp = x.split(' ')
                ip, mask = tmp[2], tmp[3]
                ifce['ip'] = ip
                ifce['mask'] = mask
        interfaces_list.append(ifce)
    return interfaces_list

def parse_address(address_raw):
    address_list = []
    chunk_list = get_items(address_raw)
    for item in chunk_list:
        address = dict()
        address['label'] = item['label'].replace('"', '')
        address['type'] = "ip"
        for x in item['data']:
            if "set subnet" in x:
                tmp = x.split(' ')
                ip, mask = tmp[2], tmp[3]
                address['ip'] = ip
                address['mask'] = mask
            if "set type" in x:
                address['type'] = x.split(' ')[2]
            if "set interface" in x:
                address['interface'] = x.split(' ')[2].replace('"', '')
            if "set associated-interface" in x:
                address['associated_interface'] = x.split(' ')[2].replace('"', '')
            if "set fqdn" in x:
                address["fqdn"] = x.split(' ')[2].replace('"', '')
            if "set start-ip" in x:
                address['start_ip'] = x.split(' ')[2]
            if "set end-ip" in x:
                address['end_ip'] = x.split(' ')[2]
            if "set comment" in x:
                address['comment'] = x.split(' ')[2].replace('"', '')
        address_list.append(address)
    return address_list

def parse_service_custom(service_raw):
    svc_list = []
    chunk_list = get_items(service_raw)
    for item in chunk_list:
        svc = dict()
        svc['label'] = item['label'].replace('"', '')
        for x in item['data']:
            if "set category" in x:
                svc['category'] = x.split(' ')[2].replace('"', '')
            if "set tcp-portrange" in x:
                svc['tcp_range'] = x.split(' ')[2:]
            if "set udp-portrange" in x:
                svc['udp_range'] = x.split(' ')[2:]
            if "set protocol" in x:
                svc['protocol'] = x.split(' ')[2]
            if "set protocol-number" in x:
                svc['protocol_nb'] = x.split(' ')[2]
            if x.startswith("set icmptype"):
                svc['icmp_type'] = x.split(' ')[2]
            if "set comment" in x:
                svc['comment'] = x.split(' ')[2].replace('"', '')
        svc_list.append(svc)
    return svc_list

def parse_service_group(service_raw):
    grp_list = []
    chunk_list = get_items(service_raw)
    for item in chunk_list:
        grp = dict()
        grp['label'] = item['label'].replace('"', '')
        for x in item['data']:
            if "set member" in x:
                members = x.split(' ')[2:]
                grp['members'] = [e.replace('"', '') for e in members]
        grp_list.append(grp)
    return grp_list

def parse_policy(policy_raw):
    policy_list = []
    chunk_list = get_items(policy_raw)
    for item in chunk_list:
        rule = dict()
        rule['label'] = item['label'].replace('"', '')
        rule['disabled'] = False
        for x in item['data']:
            if "set status disable" in x:
                rule['disabled'] = True
            if "set name" in x:
                name = x.split(' ')[2].replace('"', '')
                rule['name'] = name
            if "set srcintf" in x:
                srcintf = x.split(' ')[2:]
                rule['srcintf'] = [e.replace('"', '') for e in srcintf]
            if "set dstintf" in x:
                dstintf = x.split(' ')[2:]
                rule['dstintf'] = [e.replace('"', '') for e in dstintf]
            if "set srcaddr" in x:
                srcaddr = x.split(' ')[2:]
                rule['srcaddr'] = [e.replace('"', '') for e in srcaddr]
            if "set dstaddr" in x:
                dstaddr = x.split(' ')[2:]
                rule['dstaddr'] = [e.replace('"', '') for e in dstaddr]
            if "set service" in x:
                service = x.split(' ')[2:]
                rule['service'] = [e.replace('"', '') for e in service]
            if "set action" in x:
                rule['action'] = x.split(' ')[2].replace('"', '')
            if "set comments" in x:
                rule['comment'] = x.split(' ')[2].replace('"', '')
        policy_list.append(rule)
    return policy_list

def get_fortigate_data(config_file):
    extracts = dict() # get raw extracts
    data = dict() # parsed data to return

    # parsing temp variables
    capture = False
    chunk = []
    label = None

    with open(config_file, 'r') as f:
        for line in f.readlines():
            # get hostname
            if "set hostname" in line:
                hostname = line.split("set hostname")[1].strip().strip('\n')
                data['hostname'] = hostname.replace('"', '')
            # get global config
            if line.startswith("config system global"):
                capture = True
                label = "global"
                continue
            # get interfaces
            elif line.startswith("config system interface"):
                capture = True
                label = "interfaces"
                continue
            # get address objects
            elif line.startswith("config firewall address"):
                capture = True
                label = "address"
                continue
            # get custom service objects
            elif line.startswith("config firewall service custom"):
                capture = True
                label = "svc_custom"
                continue
            # get service groups
            elif line.startswith("config firewall service group"):
                capture = True
                label = "svc_group"
                continue
            # get policy ruless
            elif line.startswith("config firewall policy"):
                capture = True
                label = "policy"
                continue
            elif line.startswith("end"):
                if label: extracts[label] = chunk
                # init variables
                capture = False
                chunk = []
                label = None
                continue
            else:
                if capture:
                    chunk.append(line.strip())
    
    if "interfaces" in extracts.keys():
        data['interfaces'] = parse_interfaces(extracts['interfaces'])

    if "policy" in extracts.keys():
        data['policy'] = parse_policy(extracts['policy'])
    
    if "address" in extracts.keys():
        data['address'] = parse_address(extracts['address'])
    
    if "svc_custom" in extracts.keys():
        data['svc_custom'] = parse_service_custom(extracts['svc_custom'])
    
    if "svc_group" in extracts.keys():
        data['svc_group'] = parse_service_group(extracts['svc_group'])
    
    return data

def parse_fortigate_config(config_file):
    """
    Generate a Firewall object from a parsed Fortigate config
    INPUT: Config data -> dict()
    OUTPUT: Firewall object
    """

    print_info(f"Parsing Fortigate config file {config_file} ...")

    # intatiate Firewall object
    config = get_fortigate_data(config_file)
    firewall = Firewall(None, config['hostname'], "Fortinet", None)

    # add Firewall Interfaces
    if "interfaces" in config.keys():
        for ifce in config['interfaces']:
            name = ifce['label']
            if set(['ip', 'mask']) <= set(ifce.keys()):
                prefix = mask_to_cidr(ifce['mask'])
                address = f"{ifce['ip']}/{prefix}"
                ifce = firewall.add_interface(name, address)
                print_info(f"Interface '{ifce.name}' added to Firewall ...")
    
    # add Hosts
    if "address" in config.keys():
        print_debug(f"Start parsing addresses ...")
        for addr in config['address']:
            print_debug(f"Start parsing address '{addr['label']}' ...")
            name = addr['label']
            if addr['type'] == "ip":
                print_debug(f"Address type for '{name}' is <ip>")
                if set(['ip', 'mask']) <= set(addr.keys()):
                    prefix = mask_to_cidr(addr['mask'])
                    address = f"{addr['ip']}/{prefix}"
                    host = Host(firewall, name, zone=None, address=address)
                    print_debug(f"Host '{host.name}' created")
                    if "associated_interface" in addr.keys():
                        ifce = get_fw_ifce_by_name(firewall, addr['associated_interface'])
                        if ifce:
                            host.set_interface(ifce)
                    host = firewall.add_host(host)
                    print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "fqdn":
                print_debug(f"Address type for '{name}' is <fqdn>")
                fqdn = addr['fqdn']
                host = Host(firewall, name, zone=None, address=None, fqdn=fqdn)
                print_debug(f"Host '{host.name}' created")
                if "associated_interface" in addr.keys():
                    ifce = get_fw_ifce_by_name(firewall, addr['associated_interface'])
                    if ifce:
                        host.set_interface(ifce)
                host = firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "interface-subnet":
                print_debug(f"Address type for '{name}' is <ifce subnet>")
                prefix = mask_to_cidr(addr['mask'])
                address = f"{addr['ip']}/{prefix}"
                host = Host(firewall, name, zone=None, address=address)
                print_debug(f"Host '{host.name}' created")
                if "interface" in addr.keys():
                    ifce = get_fw_ifce_by_name(firewall, addr['interface'])
                    if ifce:
                        host.set_interface(ifce)
                firewall.add_host(host)
                print_info(f"Host '{host.name}' added to Firewall ...")
            elif addr['type'] == "iprange":
                print_debug(f"Address type for '{name}' is <ip range>")
                pass
            else:
                print_debug(f"Address type for '{name}' is <unknown>")
                pass
    
    # add services
    if "svc_custom" in config.keys():
        for svc in config['svc_custom']:
            svc_list = []
            name = svc['label']
            if "tcp_range" in svc.keys():
                svc_list.extend(create_service_from_range(name, "TCP", svc['tcp_range']))
            if "udp_range" in svc.keys():
                svc_list.extend(create_service_from_range(name, "UDP", svc['udp_range']))
            if "icmp_type" in svc.keys():
                try:
                    port = int(svc['icmp_type'])
                    service = Service(name, "ICMP")
                    service.set_port(port)
                    svc_list.append(service)
                except:
                    pass
            if all(x not in svc.keys() for x in ["tcp_range", "udp_range", "icmp_type"]) and "protocol" in svc.keys():
                protocol = svc['protocol']
                service = Service(name, protocol)
                svc_list.append(service)
            if len(svc_list) > 1:
                for i, svc in enumerate(svc_list):
                    svc.set_name(f"{name}_{i+1}")
            for s in svc_list:
                firewall.add_service(s)
                print_info(f"Service '{s.name}' added to Firewall ...")

    # add service groups
    if "svc_group" in config.keys():
        print_debug(f"Start parsing service groups ...")
        for grp in config['svc_group']:
            svc_group = ServiceGroup(grp['label'])
            print_debug(f"Service group {svc_group.name} created")
            for svc_name in grp['members']:
                print_debug(f"Adding member {svc_name} ...")
                svc = get_service_by_name(firewall, svc_name)
                if svc:
                    svc_group.add_service(svc)
                    print_debug(f"Service '{svc.name}' added to group '{svc_group.name}'")
            firewall.add_svc_group(svc_group)
            print_info(f"Service group '{svc_group.name}' added to Firewall")

    # add rules
    if "policy" in config.keys():
        for r in config['policy']:
            if set(['label', 'srcaddr', 'dstaddr', 'service']) > set(r.keys()):
                continue
            nb = int(r['label'])
            # get source addresses
            src = []
            for a in r['srcaddr']:
                if a.lower() == "all":
                    src = None
                    break
                else:
                    host = get_host_by_name(firewall, a)
                    if host:
                        src.append(host)
            # get dest adresses
            dest = []
            for a in r['dstaddr']:
                if a.lower() == "all":
                    dest = None
                    break
                else:
                    host = get_host_by_name(firewall, a)
                    if host:
                        dest.append(host)
            # get services
            services = []
            for s in r['service']:
                if s.lower() == "all":
                    services = None
                    break
                else:
                    svc = get_service_by_name(firewall, s)
                    if svc:
                        services.append(svc)
                        continue
                    svc = get_svc_grp_by_name(firewall, s)
                    if svc:
                        services.append(svc)
            # initiate rule
            rule = Rule(nb, src, dest, services)
            # get source interfaces
            src_ifce = []
            if "srcintf" in r.keys():
                for i in r['srcintf']:
                    ifce = get_fw_ifce_by_name(firewall, i)
                    if ifce:
                        src_ifce.append(ifce)
                rule.set_src_ifce(src_ifce)
            # get dest interfaces
            dest_ifce = []
            if "destintf" in r.keys():
                for i in r['destintf']:
                    ifce = get_fw_ifce_by_name(firewall, i)
                    if ifce:
                        dest_ifce.append(ifce)
                rule.set_dest_ifce(dest_ifce)
            # check if rule is disabled
            if "disabled" in r.keys():
                if r['disabled']: rule.disable()
            firewall.add_rule(rule)
            print_info(f"Rule #{rule.number} added to Firewall")
    return firewall


'''config = get_fortigate_data("../../FG_sample_micro.conf")

if "hostname" in config.keys():
    print(f"hostname >> {config['hostname']}\n")

if "interfaces" in config.keys():
    for ifce in config['interfaces']:
        print(f"ifce >> {ifce}")
    print()

if "address" in config.keys():
    for addr in config['address']:
        print(f"address >> {addr}")
    print()

if "svc_custom" in config.keys():
    for svc in config['svc_custom']:
        print(f"service >> {svc}")
    print()

if "svc_group" in config.keys():
    for svc in config['svc_group']:
        print(f"svc group >> {svc}")
    print()

if "policy" in config.keys():
    for rule in config['policy']:
        print(f"rule >> {rule}")
    print()'''