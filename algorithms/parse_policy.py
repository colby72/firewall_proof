from cli.logger import *
from core.policy import *

import json


def parse_policy(policy_file):
    print_info(f"Parsing JSON policy file '{policy_file}' ...")
    # read JSON data from file
    f = open(policy_file, 'r', encoding="utf8")
    data = json.loads(f.read())
    f.close()

    # parse data
    policy = FWPolicy(data['name'], data['default'])
    print_info(f"Firewall policy '{policy.name}' initiated ...")
    policy.rules = data['rules'][:]
    return policy