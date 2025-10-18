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
    policy = FWPolicy(company, data['name'], data['default'])
    print_info(f"Firewall policy '{policy.name}' initiated ...")
    #policy.rules = data['rules'][:]
    for rule in data['rules']:
        src_zone = get_zone_by_name(company, rule['src_zone'])
        dest_zone = get_zone_by_name(company, rule['dest_zone'])
        pol_rule = {
            "src_zone": src_zone,
            "dest_zone": dest_zone,
            "services": rule['services'],
            "vpn": rule['vpn'],
            "status": rule['status']
        }
        policy.rules.append(pol_rule)
    return policy