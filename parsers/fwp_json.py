from utils import *
from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *

import json


def parse_fwp_json(conf_file):
    print_info(f"Parsing JSON conf file '{conf_file}' ...")
    # read JSON data from file
    f = open(conf_file, 'r', encoding="utf8")
    data = json.loads(f.read())
    f.close()

    # initiate company
    company = Company(data['name'])
    print_info(f"Company '{company.name}' initiated ...")

    # parse zones
    zone_count = 0
    print_info(f"Parsing zones for company '{company.name}' ...")
    for z in data['zones']:
        zone = Zone(z['name'], z['level'], z['description'], z['color'])
        e = company.add_zone(zone)
        if e: zone_count += 1
    print_info(f"{zone_count} Zones added to company '{company.name}'")

    # parse Firewall status list
    for s in data['status']:
        status = RuleStatus(s['label'], s['color'], s['compliant'])
        company.add_status(status)

    # parse Firewall inventory
    fw_count = 0
    for fw in data['fw_inventory']:
        firewall = Firewall(company, fw['name'], fw['vendor'], fw['address'])
        e = company.add_firewall(firewall)
        if e: fw_count += 1
        # parse Firewall interfacess
        for interface in fw['interfaces']:
            firewall.add_interface(interface['name'], interface['address'])
        # parse Firewall hosts
        for h in fw['hosts']:
            zone = get_zone_by_name(company, h['zone'])
            host = Host(fw, h['name'], zone, h['address'])
            firewall.add_host(host)
        # parse Firewall groups
        for g in fw['groups']:
            group = ObjGroup(g['name'], g['zone'])
            firewall.add_group(group)
            for h in firewall.hosts:
                if h.name in g['hosts']:
                    group.add_host(h)
        # parse Firewall rules
        for r in fw['rules']:
            # fetch src host objects
            src = []
            for h in firewall.hosts:
                if h.name in r['src']:
                    src.append(h)
            # fetch dest host objects
            dest = []
            for h in firewall.hosts:
                if h.name in r['dest']:
                    dest.append(h)
            # initiate rule
            rule = Rule(r['number'], src, dest, r['services'])
            firewall.add_rule(rule)
    print_info(f"{fw_count} Firewalls added to company '{company.name}'")
    return company