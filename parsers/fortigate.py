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
        ifce['label'] = item['label']
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
        address['label'] = item['label']
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
        svc['label'] = item['label']
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
            if "set comment" in x:
                svc['comment'] = x.split(' ')[2].replace('"', '')
        svc_list.append(svc)
    return svc_list

def parse_service_group(service_raw):
    grp_list = []
    chunk_list = get_items(service_raw)
    for item in chunk_list:
        grp = dict()
        grp['label'] = item['label']
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
        rule['label'] = item['label']
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

def parse_fortigate_config(config_file):
    extracts = dict()
    capture = False
    chunk = []
    label = None

    with open(config_file, 'r') as f:
        for line in f.readlines():
            if line.startswith("config system global"):
                capture = True
                label = "global"
                continue
            elif line.startswith("config system interface"):
                capture = True
                label = "interfaces"
                continue
            elif line.startswith("config firewall address"):
                capture = True
                label = "address"
                continue
            elif line.startswith("config firewall service custom"):
                capture = True
                label = "svc_custom"
                continue
            elif line.startswith("config firewall service group"):
                capture = True
                label = "svc_group"
                continue
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
        interfaces_raw = extracts['interfaces']
        interfaces = parse_interfaces(interfaces_raw)
        for ifce in interfaces:
            print(f"ifce >> {ifce}")

    if "policy" in extracts.keys():
        policy_raw = extracts['policy']
        policy = parse_policy(policy_raw)
        #for rule in policy:
            #print(f"rule >> {rule}")
    
    if "address" in extracts.keys():
        address_raw = extracts['address']
        address = parse_address(address_raw)
        #for addr in address:
            #print(f"address >> {addr}")
    
    if "svc_custom" in extracts.keys():
        svc_raw = extracts['svc_custom']
        svc = parse_service_custom(svc_raw)
        for s in svc:
            print(f"service >> {s}")
    
    if "svc_group" in extracts.keys():
        svc_raw = extracts['svc_group']
        svc = parse_service_group(svc_raw)
        for s in svc:
            print(f"svc group >> {s}")


parse_fortigate_config("../../FG_sample_micro.conf")