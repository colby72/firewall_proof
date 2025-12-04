from jinja2 import Environment, FileSystemLoader
import os, datetime

from reporting.generate_report import *
from reporting.generate_graphs import *
from cli.logger import *
from utils import *


def get_firewall_data(firewall):
    colored_row = "e4e4e4"
    context = {
        "fw_name": text_to_tex(firewall.name),
        "fw_vendor": text_to_tex(firewall.vendor),
        "fw_address": text_to_tex(firewall.address),
        "fw_policy": text_to_tex(firewall.policy.name),
        "iface_count": len(firewall.interfaces),
        "host_count": len(firewall.hosts),
        "group_count": len(firewall.groups),
        "rules_count": len(firewall.rules),
        "compliance_rate": firewall.compliance_rate(),
        "date": datetime.date.today()
    }
    
    # get interfaces
    context['interfaces'] = []
    for i, interface in enumerate(firewall.interfaces):
        iface = {
            "name": text_to_tex(interface.name),
            "address": text_to_tex(interface.address),
            "hosts": "n/a",
            "row_color": "ffffff"
        }
        if i%2==0: iface['row_color'] = colored_row
        context['interfaces'].append(iface)
    
    # get rules
    context['rules'] = []
    for i, r in enumerate(firewall.rules):
        rule = {
            "id": r.number,
            "src": [{"name": h.name, "color": h.zone.color.replace('#', '')} for h in r.src],
            "dest": [{"name": h.name, "color": h.zone.color.replace('#', '')} for h in r.dest],
            "services": '\\\\'.join(r.services) if r.services else "all",
            "vpn": str(r.vpn),
            "status": text_to_tex(r.status.label),
            "status_color": r.status.color.replace('#', ''),
            "row_color": "ffffff"
        }
        if i%2==0: rule['row_color'] = colored_row
        context['rules'].append(rule)
    return context

def get_firewall_data_docx(firewall):
    colored_row = "e4e4e4"
    context = {
        "fw_name": text_to_tex(firewall.name),
        "fw_vendor": text_to_tex(firewall.vendor),
        "fw_address": text_to_tex(firewall.address),
        "fw_policy": text_to_tex(firewall.policy.name),
        "iface_count": len(firewall.interfaces),
        "host_count": len(firewall.hosts),
        "group_count": len(firewall.groups),
        "rules_count": len(firewall.rules),
        "compliance_rate": firewall.compliance_rate(),
        "date": datetime.date.today()
    }
    
    # get interfaces
    context['interfaces'] = []
    for i, interface in enumerate(firewall.interfaces):
        iface = {
            "name": text_to_tex(interface.name),
            "address": text_to_tex(interface.address),
            "hosts": "n/a",
            "row_color": "ffffff"
        }
        if i%2==0: iface['row_color'] = colored_row
        context['interfaces'].append(iface)
    
    # get rules
    context['rules'] = []
    for i, r in enumerate(firewall.rules):
        rule = {
            "id": r.number,
            "src": '\n'.join([h.name for h in r.src]),
            "dest": '\n'.join([h.name for h in r.dest]),
            "services": '\n'.join(r.services) if r.services else "all",
            "vpn": str(r.vpn),
            "status": text_to_tex(r.status.label),
            "status_color": r.status.color.replace('#', ''),
            "row_color": "ffffff"
        }
        if i%2==0: rule['row_color'] = colored_row
        context['rules'].append(rule)
    return context

def generate_firewall_report_latex(firewall):
    # get context data
    context = get_firewall_data(firewall)
    chart_file, chart_path = status_pie_chart("", firewall.company, firewall.status_stats())
    context['firewall_chart'] = chart_path
    # get report template and render it
    report = generate_latex_report("firewall_report.tex.j2", context, firewall.name)
    return report

def generate_firewall_report_docx(firewall):
    # get context data
    context = get_firewall_data_docx(firewall)
    chart_file, chart_path = status_pie_chart("", firewall.company, firewall.status_stats())
    images = {
        "firewall_chart": chart_path,
        "firewall_chart_width": 75,
        "firewall_chart_height": 75
    }
    # generate report
    report = generate_docx_report("firewall_report.docx.j2", context, images, firewall.name)
    return report

def generate_firewall_report_html(firewall):
    # get context data
    context = get_firewall_data_docx(firewall)
    # generate report
    report = generate_html_report("firewall_report.html.j2", context, firewall.name)
    return report