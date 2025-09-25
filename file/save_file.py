import jsonpickle
import os

from cli.logger import *


def save_file(project, file_name=None, file_path=os.getcwd()):
    # set default file name
    if not file_name:
        file_name = project.name.replace(' ', '_').lower()
    # set file extension
    if not file_name.endswith(".fwp"):
        file_name += '.fwp'
    target_file = os.path.join(file_path, file_name)

    # convert project data into JSON
    try:
        project_json = jsonpickle.encode(project)
    except:
        print_error(f"Converting project '{project.name}' into JSON failed !")
        return None

    # save JSON data to target file
    try:
        with open(target_file, 'w') as tfile:
            tfile.write(project_json)
        tfile.close()
        print_success(f"{len(project_json)} chars successfully written to {target_file}")
        return target_file
    except:
        print_error(f"Project '{project.name}' save failed !")
        return None