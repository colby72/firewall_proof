from utils import *
from cli.logger import *
from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *
from core.policy import *
from core.service import *

import json


def parse_company_json_v1(conf_file):
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
        zone = Zone(z['name'], str(z['level']), z['description'], z['color'])
        e = company.add_zone(zone)
        if e: zone_count += 1
    print_info(f"{zone_count} Zones added to company '{company.name}'")

    # parse Firewall status list
    for s in data['status']:
        status = RuleStatus(s['label'], s['color'], s['compliant'])
        company.add_status(status)
    
    # parse firewall policies
    for p in data['policies']:
        default = get_status_by_label(company, p['default'])
        policy = FWPolicy(company, p['name'], default)
        print_info(f"Firewall policy '{policy.name}' initiated ...")
        for rule in p['rules']:
            src_zone = get_zone_by_name(company, rule['src_zone'])
            dest_zone = get_zone_by_name(company, rule['dest_zone'])
            status = get_status_by_label(company, rule['status'])
            pol_rule = PolicyRule(src_zone, dest_zone, rule['services'], rule['vpn'], status)
            policy.add_rule(pol_rule)
        company.add_policy(policy)

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
        # set policy
        policy = get_policy_by_name(company, fw['policy'])
        firewall.set_policy(policy)
    print_info(f"{fw_count} Firewalls added to company '{company.name}'")
    return company

def parse_company_json(conf_file):
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
        zone = Zone(z['name'], str(z['level']), z['description'], z['color'])
        e = company.add_zone(zone)
        if e: zone_count += 1
    print_info(f"{zone_count} Zones added to company '{company.name}'")

    # parse Firewall status list
    for s in data['status']:
        status = RuleStatus(s['label'], s['color'], s['compliant'])
        company.add_status(status)
    
    # parse firewall policies
    for p in data['policies']:
        default = get_status_by_label(company, p['default'])
        policy = FWPolicy(company, p['name'], default)
        print_info(f"Firewall policy '{policy.name}' initiated ...")
        for rule in p['rules']:
            src_zone = get_zone_by_name(company, rule['src_zone'])
            dest_zone = get_zone_by_name(company, rule['dest_zone'])
            status = get_status_by_label(company, rule['status'])
            services = [create_svc_from_label(svc) for svc in rule['services']]
            pol_rule = PolicyRule(src_zone, dest_zone, services, rule['vpn'], status)
            policy.add_rule(pol_rule)
        company.add_policy(policy)

    # parse Firewall inventory
    fw_count = 0
    for fw in data['fw_inventory']:
        firewall = Firewall(company, fw['name'], fw['vendor'], fw['address'])
        e = company.add_firewall(firewall)
        if e: fw_count += 1
        # parse Firewall interfacess
        for interface in fw['interfaces']:
            firewall.add_interface(interface['name'], interface['address'])
        # parse Firewall services
        for s in fw['services']:
            # get name
            if "name" in s.keys():
                name = s['name'].replace('/', '_')
            else:
                name = None
            # create Service instance
            svc = Service(name, s['protocol'])
            # get port or port range if any
            if "port_start" in s.keys() and "port_end" in s.keys():
                svc.set_port_range(s['port_start'], s['port_end'])
            elif "port" in s.keys():
                svc.set_port(s['port'])
            else:
                pass
            if not svc.name: svc.auto_set_name()
            firewall.add_service(svc)
        # parse Firewall service groups
        for g in fw['service_groups']:
            svc_group = ServiceGroup(g['name'].replace('/', '_'))
            for svc_name in g['services']:
                svc = get_service_by_name(firewall, svc_name)
                if svc:
                    svc_group.add_service(svc)
            firewall.add_svc_group(svc_group)
        # parse Firewall hosts
        for h in fw['hosts']:
            zone = get_zone_by_name(company, h['zone'])
            host = Host(fw, h['name'], zone, h['address'])
            firewall.add_host(host)
        # parse Firewall groups
        for g in fw['host_groups']:
            if "zone" in g.keys():
                group = ObjGroup(g['name'], g['zone'])
            else:
                group = ObjGroup(g['name'])
            firewall.add_group(group)
            for h in firewall.hosts:
                if h.name in g['hosts']:
                    group.add_host(h)
            group.auto_set_zone()
            firewall.add_group(group)
        # parse Firewall rules
        for r in fw['rules']:
            # fetch src host objects
            src = []
            for h in firewall.hosts:
                if h.name in r['src']:
                    src.append(h)
            for obj in firewall.groups:
                if obj.name in r['src']:
                    src.append(obj)
            # fetch dest host objects
            dest = []
            for h in firewall.hosts:
                if h.name in r['dest']:
                    dest.append(h)
            for obj in firewall.groups:
                if obj.name in r['dest']:
                    dest.append(obj)
            # fetch service objects
            services = []
            for s in r['services']:
                # try fetch single defined service
                svc = get_service_by_name(firewall, s)
                if svc:
                    services.append(svc)
                    continue
                # try fetch defined service group
                grp = get_svc_grp_by_name(firewall, s)
                if grp:
                    services.append(grp)
                    continue
                # try parse raw service labels
                new_service = create_svc_from_label(s)
                if new_service:
                    # add new service to FW
                    svc = firewall.add_service(new_service)
                    # append new service to rule's services
                    if svc:
                        services.append(svc)
            # initiate rule
            rule = Rule(r['number'], src, dest, services)
            firewall.add_rule(rule)
        # set policy
        policy = get_policy_by_name(company, fw['policy'])
        firewall.set_policy(policy)
    print_info(f"{fw_count} Firewalls added to company '{company.name}'")
    return company