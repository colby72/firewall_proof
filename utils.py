from cli.logger import *


def get_zone_by_name(company, zone_name):
    for z in company.zones:
        if z.name == zone_name:
            return z
    print_error(f"Zone '{zone_name}' not found in Company '{company.name}'")
    return None

def get_status_by_label(company, label):
    for status in company.status_list:
        if status.label == label:
            return status
    print_error(f"Status '{label}' not found in Company '{company.name}'")
    return None

def get_status_list_labels(company):
    labels = [status.label for status in company.status_list]
    return labels

def text_to_tex(text):
    """
    Format text to be Latex-compatible
    Escape Latex special chars
    """
    text = text.replace('&', '\&')
    return text

def get_stylesheet(sheet_file):
    with open(f"gui/qss/{sheet_file}", 'r', encoding="utf8") as f:
        style = f.read()
        return style