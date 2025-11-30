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

def generate_company_report_tex(company):
    # get context data
    context = get_company_data(company)
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
    template = env.get_template('company_report.tex.j2')
    tex_content = template.render(context)

    # save rendered report
    tex_file = f"{company.name}_report.tex".replace(' ', '_')
    pdf_file = f"{company.name}_report.pdf".replace(' ', '_')
    try:
        with open(f"reporting/export/{tex_file}", 'w') as f:
            f.write(tex_content)
        print_success(f"Company TEX report for {company.name} generated successfully")
    except:
        print_error(f"Error while generating TEX repot for company {company.name}")
        return None
    
    # generate PDF file
    os.system(f"pdflatex -interaction=nonstopmode reporting/export/{tex_file}")
    os.system("rm *.aux *.log *.synctex*")
    os.system(f"mv {pdf_file} reporting/export/")

def generate_company_report_html(company):
    # get context data
    context = {
        "company_name": company.name,
        "zone_count": len(company.zones),
        "fw_count": len(company.fw_inventory)
    }

    # get report template and render it
    env = Environment(loader = FileSystemLoader('reporting/templates'))
    template = env.get_template('company_report.j2')
    html_content = template.render(context)
    
    # save rendered report
    html_report = f"{company.name}_report.html"
    pdf_report = f"{company.name}_report.pdf"
    try:
        with open(f"reporting/export/{html_report}", 'w') as f:
            f.write(html_content)
        f.close()
        print_success(f"Company HTML report for {company.name} generated successfully")
    except:
        print_error(f"Error while generating HTML repot for company {company.name}")
        return None
    try:
        with open(f"reporting/export/{pdf_report}", 'wb') as f:
            pisa_status = pisa.CreatePDF(html_content, dest=f)
        f.close()
        print_success(f"Company PDF report for {company.name} generated successfully")
    except:
        print_error(f"Error while generating PDF repot for company {company.name}")
        return None
    return pdf_report

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