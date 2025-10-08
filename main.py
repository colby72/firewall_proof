from project import *

from core.company import *
from core.firewall import *
from core.host import *
from core.rule import *
from core.zone import *

from file.save_file import *
from file.open_file import *

from cli.logger import *
from cli.display import *

from algorithms.parse_policy import *
from algorithms.policy_check import *

from parsers.fwp_json import *


def main_banner():
    print("############################################")
    print("##                                        ##")
    print("##      Firewall Proof v1.0.0-alpha1      ##")
    print("##                                        ##")
    print("############################################")
    print("\n\n")


main_banner()
print_info("Starting Firewall Proof ...")

def create_data():
    company = parse_fwp_json('test_data/space_y.json')
    print_success(f"Company '{company.name}' succssfully created !")

    policy = parse_policy(company, 'test_data/policy.json')
    print_success(f"Firewall policy '{policy.name}' succssfully defined !")

    for fw in company.fw_inventory:
        apply_policy(fw, policy)
        display_fw_rules(fw)

    project = Project("Test project")
    project.add_company(company)
    print_success(f"Project '{project.name}' created successfully")

    file_saved = save_file(project)

def open_data():
    file_saved = "test_project.fwp"
    project = open_file(file_saved)

    company = project.companies[0]
    print_info(f"Project has {len(project.companies)} companies defined")
    print_info(f"Company to display is: '{company.name}'")

    for fw in company.fw_inventory:
        display_fw_rules(fw)

#create_data()
open_data()