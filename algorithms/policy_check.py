from cli.logger import *


def apply_policy(firewall, policy):
    """
    INPUT: Object Firewall -> firewall
    INPUT: Object FWPolicy -> policy
    Step 1: Set all Firewall rules to Policy's default
    Step 2: Go through Firewall rules and set status for applicable ones
    """
    print_info(f"Applying policy '{policy.name}' to the Firewall '{firewall.name}' ...")
    print_info(f"All rules will be set set to policy default value: {policy.default.label}")
    firewall.policy = policy
    for fw_rule in firewall.rules:
        # skip rule is status is set manually
        if fw_rule.manual:
            continue
        # set status to default value
        fw_rule.set_status(policy.default)
        
        # get rule's data to be analyzed
        src_zones = [h.zone.name for h in fw_rule.src]
        dest_zones = [h.zone.name for h in fw_rule.dest]
        services = fw_rule.services

        # enumerate and look for applicable rules
        for pol_rule in policy.rules:
            # is src applicable ?
            src_applicable = False
            if (pol_rule.src_zone==None) or (pol_rule.src_zone.name in src_zones):
                src_applicable = True
            else:
                continue
            
            # is dest applicable ?
            dest_applicable = False
            if (pol_rule.dest_zone==None) or (pol_rule.dest_zone.name in dest_zones):
                dest_applicable = True
            else:
                continue

            # is VPN setting coompliant ?
            if (not pol_rule.vpn) or (pol_rule.vpn and fw_rule.vpn):
                vpn_compliant = True
            else:
                vpn_compliant = False
            
            # are services compliant ?
            service_compliant = True
            if pol_rule.services: # verify policy 'services' is not set to 'all' 
                for s in fw_rule.services:
                    if not (s in pol_rule.services):
                        service_compliant = False
                        break

            # apply rule
            if vpn_compliant and service_compliant:
                fw_rule.set_status(pol_rule.status)
                print_info(f"Rule #{fw_rule.number} set to: {fw_rule.status.label}")