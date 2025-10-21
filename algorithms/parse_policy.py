from utils import *
from cli.logger import *
from core.policy import *

import json


def parse_policy(company, policy_file):
    print_info(f"Parsing JSON policy file '{policy_file}' ...")
    # read JSON data from file
    f = open(policy_file, 'r', encoding="utf8")
    data = json.loads(f.read())
    f.close()

    # parse data
    default = get_status_by_label(company, data['default'])
    policy = FWPolicy(company, data['name'], default)
    print_info(f"Firewall policy '{policy.name}' initiated ...")
    for rule in data['rules']:
        src_zone = get_zone_by_name(company, rule['src_zone'])
        dest_zone = get_zone_by_name(company, rule['dest_zone'])
        status = get_status_by_label(company, rule['status'])
        pol_rule = {
            "src_zone": src_zone,
            "dest_zone": dest_zone,
            "services": rule['services'],
            "vpn": rule['vpn'],
            "status": status
        }
        policy.rules.append(pol_rule)
    return policy