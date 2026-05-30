from core.service import *
from cli.logger import *


def apply_policy_v1(firewall, policy):
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

def compare_service(rule_svc, policy_svc):
    rule_label = rule_svc.auto_set_label()
    policy_label = policy_svc.auto_set_label()
    if rule_svc.protocol != policy_svc.protocol:
        return False
    # both services are flagged as range
    if rule_svc.is_range and policy_svc.is_range:
        return (rule_svc.port_start>=policy_svc.port_start and rule_svc.port_end<=policy_svc.port_end) \
            or ((not rule_svc.port_start) and (not policy_svc.port_start))
    # both services are single port
    if (not rule_svc.is_range) and (not policy_svc.is_range):
        return (rule_svc.port == policy_svc.port) or ((not rule_svc.port) and (not policy_svc.port))
    # by default return False
    return False

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
        #dest_zones = [h.zone.name for h in fw_rule.dest]
        dest_zones = []
        for h in fw_rule.dest:
            dest_zones.append(h.zone.name)
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
            for sr in fw_rule.services:
                if isinstance(sr, Service):
                    comparaisons = [compare_service(sr, sp) for sp in pol_rule.services]
                if isinstance(sr, ServiceGroup):
                    comparaisons = []
                    for x in sr.services:
                        comparaisons.extend([compare_service(x, sp) for sp in pol_rule.services])
                if any(comparaisons):
                    continue
                else:
                    service_compliant = False
                    break

            # apply rule
            if vpn_compliant and service_compliant:
                fw_rule.set_status(pol_rule.status)
                print_info(f"Rule #{fw_rule.number} set to: {fw_rule.status.label}")