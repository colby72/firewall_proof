from cli.logger import *


def get_zone_by_name(company, zone_name):
    for z in company.zones:
        if z.name == zone_name:
            return z
    print_error(f"Zone '{zone_name}' not found in Company '{company.name}'")
    return None