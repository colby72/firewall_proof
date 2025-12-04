import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from utils import *


def status_pie_chart(title, company, stats):
    # prepare data
    labels = stats.keys()
    sizes = stats.values()
    colors = []
    for label in stats.keys():
        status = get_status_by_label(company, label)
        colors.append(status.color)
    file_name = title.lower().replace(' ', '_') + '.png'
    if not os.path.isdir("reporting/export/charts/"):
        os.mkdir("reporting/export/charts")
    file_path = os.path.join("reporting/export/charts/", file_name)
    # draw pie chart
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90, colors=colors)
    plt.title(title)
    plt.savefig(file_path, dpi=300, format='png', bbox_inches='tight', transparent=True)
    return file_name, file_path