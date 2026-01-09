import json


# look for critical OT functions (L1-2) connected to DMZ
def insecure_dmz_ot_traffic(rule):
    src_level = float(rule.src_zone.level)
    dest_level = float(rule.dest_zone.level)
    return (src_level<=2 and dest_level==3.5) or (src_level==3.5 and dest_level<=2)

# look for direct IT-OT connections not stopping at OT DMZ
def policy_direct_it_ot_flows(rule):
    src_level = float(rule.src_zone.level)
    dest_level = float(rule.dest_zone.level)
    return (src_level<=3 and dest_level>=4) or (src_level>=4 and dest_level<=3)

# look for OT/ICS traffic beyond OT domain
def ot_traffic_overflow(rule):
    src_level = float(rule.src_zone.level)
    dest_level = float(rule.dest_zone.level)
    max_level = max(src_level, dest_level)
    with open('algorithms/ot_services.json', 'r', encoding="utf8") as f:
        ot_services = json.loads(f.read())
    applicable_svc = []
    for s in rule.services:
        if s in ot_services.keys(): applicable_svc.append(s)
    if (max_level == 3.5) and applicable_svc:
        return ("warning", applicable_svc)
    elif (max_level >= 4) and applicable_svc:
        return ("critical", applicable_svc)
    else:
        return None

# look for unencrypted and weak services
def weak_services(svc_list):
    suspect_svc = []
    with open('algorithms/vulnerable_ports.json', 'r', encoding="utf8") as f:
        vulnerable_ports = json.loads(f.read())
    for s in svc_list:
        if s in vulnerable_ports.keys():
            suspect_svc.append((s, vulnerable_ports[s]))
    return suspect_svc

def policy_anomalies(policy):
    # look for compliant default status
    default_compliant = policy.default.compliant
    # get suspicious rules
    rules_meter = []
    for rule in policy.rules:
        if not rule.status.compliant:
            continue
        rule_measure = (
            rule.id, # rules ID
            insecure_dmz_ot_traffic(rule), # boolean
            policy_direct_it_ot_flows(rule), # boolean
            ot_traffic_overflow(rule), # None or tuple (level, list of services concerned)
            weak_services(rule.services) # list of weak services
        )
        if rule_measure[1] or rule_measure[2] or rule_measure[3] or rule_measure[4]:
            rules_meter.append(rule_measure)
    # return result
    return (default_compliant, rules_meter)