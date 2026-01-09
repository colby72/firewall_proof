from core.company import *


def add_traffic_lights_status(company):
    status_list = [
        {"label": "OK", "color": "#1ba91c", "compliant": True},
        {"label": "WARNING", "color": "#f4bf14", "compliant": False},
        {"label": "NOK", "color": "#e83232", "compliant": False}
    ]
    error = False
    for s in status_list:
        status = RuleStatus(s['label'], s['color'], s['compliant'])
        added = company.add_status(status)
        if not added: error = True
    return error