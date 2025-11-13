from jinja2 import Environment, FileSystemLoader
#from xhtml2pdf import pisa
import os

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
        "rules_count": len(firewall.rules)
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

def generate_firewall_report_tex(firewall):
    # get context data
    context = get_firewall_data(firewall)
    # get report template and render it
    env = Environment(
        loader = FileSystemLoader('reporting/templates'),
        trim_blocks=True,
        block_start_string='@@',
        block_end_string='@@',
        variable_start_string='@=',
        variable_end_string='=@',
        autoescape=False,
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
    )
    template = env.get_template('firewall_report.tex.j2')
    tex_content = template.render(context)

    # save rendered report
    tex_file = f"{firewall.name}_report.tex".replace(' ', '_')
    pdf_file = f"{firewall.name}_report.pdf".replace(' ', '_')
    try:
        with open(f"reporting/export/{tex_file}", 'w') as f:
            f.write(tex_content)
        print_success(f"Firewall TEX report for {firewall.name} generated successfully")
    except:
        print_error(f"Error while generating TEX repot for firewall {firewall.name}")
        return None
    
    # generate PDF file
    os.system(f"pdflatex -interaction=nonstopmode reporting/export/{tex_file}")
    os.system("rm *.aux *.log *.synctex*")
    os.system(f"mv {pdf_file} reporting/export/")