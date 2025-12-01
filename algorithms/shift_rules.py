def shift_rules(firewall, gap, start=1, end=None):
    for rule in firewall.rules:
        if end:
            if (start<=rule.number) and (rule.number<=end):
                rule.number += gap
        else:
            if start <= rule.number: rule.number += gap