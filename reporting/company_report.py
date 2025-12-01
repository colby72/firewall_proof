from jinja2 import Environment, FileSystemLoader
#from xhtml2pdf import pisa
import os

from reporting.generate_report import *
from cli.logger import *
from utils import *


def get_company_data(company):
    colored_row = "e4e4e4"
    context = {
        "company_name": text_to_tex(company.name),
        "zone_count": len(company.zones),
        "fw_count": len(company.fw_inventory)
    }
    
    # get zones
    context['zones'] = []
    for i, z in enumerate(company.zones):
        zone = {
            "name": text_to_tex(z.name),
            "level": z.level,
            "description": text_to_tex(z.description),
            "color": z.color.replace('#', ''),
            "row_color": "ffffff"
        }
        if i%2==0: zone['row_color'] = colored_row
        context['zones'].append(zone)
    
    # get policies
    context['policies'] = []
    for i, p in enumerate(company.policies):
        policy = {
            "name": text_to_tex(p.name),
            "default": text_to_tex(p.default.label),
            "nb_rules": len(p.rules),
            "row_color": "ffffff"
        }
        if i%2==0: policy['row_color'] = colored_row
        context['policies'].append(policy)
    
    # get firewalls
    context['firewalls'] =[]
    for i, fw in enumerate(company.fw_inventory):
        firewall = {
            "name": text_to_tex(fw.name),
            "vendor": text_to_tex(fw.vendor),
            "address": text_to_tex(fw.address),
            "policy": text_to_tex(fw.policy.name),
            "row_color": "ffffff"
        }
        if i%2==0: firewall['row_color'] = colored_row
        context['firewalls'].append(firewall)
    return context

def generate_company_report_html(company):
    # get context data
    context = {
        "company_name": company.name,
        "zone_count": len(company.zones),
        "fw_count": len(company.fw_inventory)
    }
    # generate report
    report = generate_html_report("company_report.html.j2", context, company.name)
    return report

def generate_company_report_latex(company):
    # get context data
    context = get_company_data(company)
    # generate report
    report = generate_latex_report("company_report.tex.j2", context, company.name)
    return report

def generate_company_report_docx(company):
    # get context data
    context = {
        "company_name": company.name,
        "zone_count": len(company.zones),
        "fw_count": len(company.fw_inventory)
    }
    # generate report
    report = generate_docx_report("company_report.docx.j2", context, company.name)
    return report