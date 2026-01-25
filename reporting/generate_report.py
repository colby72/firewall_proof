from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os, sys, shutil, datetime, docxtpl, docx2pdf, subprocess, glob
from docx.shared import Mm

from cli.logger import *
from utils import *


def generate_html_report(template, context, report_name):
    # get report template and render it
    env = Environment(loader = FileSystemLoader('reporting/templates'))
    template = env.get_template(template)
    html_content = template.render(context)

    # save rendered report
    html_file = f"{report_name}_{datetime.date.today()}.html".replace(' ', '_')
    pdf_file = f"{report_name}_{datetime.date.today()}.pdf".replace(' ', '_')
    try:
        with open(f"reporting/export/{html_file}", 'w') as f:
            f.write(html_content)
        print_success(f"HTML report '{report_name}' generated successfully")
    except:
        print_error(f"Error while generating HTML report '{report_name}'")
        return None
    try:
        with open(f"reporting/export/{pdf_file}", 'wb') as f:
            pisa_status = pisa.CreatePDF(html_content, dest=f)
        print_success(f"PDF report '{report_name}' generated successfully")
    except:
        print_error(f"Error while generating PDF report '{report_name}'")
        return None
    return pdf_file

def generate_latex_report(template, context, report_name):
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
    template = env.get_template(template)
    tex_content = template.render(context)

    # save rendered report
    tex_file = f"{report_name}_{datetime.date.today()}.tex".replace(' ', '_')
    pdf_file = f"{report_name}_{datetime.date.today()}.pdf".replace(' ', '_')
    try:
        with open(f"reporting/export/{tex_file}", 'w') as f:
            f.write(tex_content)
        print_success(f"Latex report '{report_name}' generated successfully")
    except:
        print_error(f"Error while generating Latex report '{report_name}'")
        return None
    
    # generate PDF file
    try:
        os.system(f"pdflatex -interaction=nonstopmode reporting/export/{tex_file}")
        to_remove = glob.glob("*.aux")
        to_remove.extend(glob.glob("*.log"))
        to_remove.extend(glob.glob("*.synctex*"))
        for f in to_remove:
            os.remove(f)
        shutil.move(pdf_file, f"reporting/export/{pdf_file}")
    except:
        print_error(f"Error while generating PDF report '{report_name}'")
        return None
    return pdf_file

def generate_docx_report(template, context, images, report_name):
    docx_file = f"{report_name}_{datetime.date.today()}.docx".replace(' ', '_')
    pdf_file = f"{report_name}_{datetime.date.today()}.pdf".replace(' ', '_')
    # get docx template and render it
    #try:
    tpl = docxtpl.DocxTemplate(f"reporting/templates/{template}")
    # create image docx objects
    for image in images.keys():
        if ("width" in image) or ("height" in image):
            continue
        pic_width = images[f"{image}_width"]
        pic_height = images[f"{image}_height"]
        pic = docxtpl.InlineImage(tpl, image_descriptor=images[image], width=Mm(pic_width), height=Mm(pic_height))
        context[image] = pic
    # render document
    tpl.render(context)
    tpl.save(docx_file)
    print_success(f"docx report '{docx_file}' generated successfully")
    '''except:
        print_error(f"Error while generating docx report '{docx_file}'")
        return None'''
    # save PDF report
    try:
        if sys.platform == "linux":
            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', docx_file])
            shutil.move(docx_file, f"reporting/export/{docx_file}")
            shutil.move(pdf_file, f"reporting/export/{pdf_file}")
            print_success(f"PDF report '{pdf_file}' generated successfully")
            return pdf_file
        if sys.platform == "win32":
            docx2pdf.convert(docx_file, pdf_file)
            shutil.move(docx_file, f"reporting/export/{docx_file}")
            shutil.move(pdf_file, f"reporting/export/{pdf_file}")
            print_error(f"Error while generating PDF report '{pdf_file}'")
            return pdf_file
    except:
        print_error(f"Error while generating PDF report '{report_name}'")
        return None