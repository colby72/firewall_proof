from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *

from cli.logger import *
from cli.display import *

from algorithms.parse_policy import *
from algorithms.policy_check import *

from parsers.fwp_json import *


def main_banner():
    print("##################################")
    print("##                              ##")
    print("##   Firewall Proof v0.1-beta   ##")
    print("##                              ##")
    print("##################################")
    print("\n\n")


main_banner()
print_info("Starting Firewall Proof ...")

company = parse_fwp_json('test_data/space_y.json')
print_success(f"Company '{company.name}' succssfully created !")

policy = parse_policy('test_data/policy.json')
print_success(f"Firewall policy '{policy.name}' succssfully defined !")

for fw in company.fw_inventory:
    apply_policy(fw, policy)
    display_fw_rules(fw)

#display_company(company)
#for fw in company.fw_inventory:
#    display_firewall(fw)