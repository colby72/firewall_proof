from core.firewall import *
from core.rule import *
from core.service import *
from core.policy import *
from core.host import *

from cli.logger import *
from utils import *

import json


def parse_firewall_json(conf_file, company=None):
    print_info(f"Parsing Firewall JSON config file '{conf_file}' ...")
    # read JSON data from file
    f = open(conf_file, 'r', encoding="utf8")
    data = json.loads(f.read())
    f.close()

    # initiate Firewall
    name = data['name'] if "name" in data.keys() else "Unknown"
    vendor = data['vendor'] if "vendor" in data.keys() else None
    address = data['address'] if "address" in data.keys() else None
    firewall = Firewall(company, name, vendor, address)

    # parse Firewall interfaces
    if "interfaces" in data.keys():
        for interface in data['interfaces']:
            name = interface['name'] if "name" in interface.keys() else "Unknown"
            address = interface['address'] if "address" in interface.keys() else None
            firewall.add_interface(name, address)
    
    # parse Firewall services
    if "services" in data.keys():
        for s in data['services']:
            # get name
            name = s['name'].replace('/', '_') if "name" in s.keys() else None
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
    if "service_groups" in data.keys():
        for g in data['service_groups']:
            svc_group = ServiceGroup(g['name'].replace('/', '_'))
            for svc_name in g['services']:
                svc = get_service_by_name(firewall, svc_name)
                if svc:
                    svc_group.add_service(svc)
            firewall.add_svc_group(svc_group)
    
    # parse Firewall hosts
    if "hosts" in data.keys():
        for h in data['hosts']:
            if company and "zone" in h.keys():
                zone = get_zone_by_name(company, h['zone'])
            else:
                zone = None
            host = Host(firewall, h['name'], zone, h['address'])
            firewall.add_host(host)
    
    # parse Firewall host groups
    if "host_groups" in data.keys():
        for g in data['host_groups']:
            if "zone" in g.keys():
                group = ObjGroup(g['name'], g['zone'])
            else:
                group = ObjGroup(g['name'])
            for h in firewall.hosts:
                if h.name in g['hosts']:
                    group.add_host(h)
            group.auto_set_zone()
            firewall.add_group(group)
    
    # parse Firewall rules
    if "rules" in data.keys():
        for r in data['rules']:
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

    return firewall