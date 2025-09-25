import jsonpickle
import os

from cli.logger import *


def open_file(file_name, file_path=os.getcwd()):
    target_file = os.path.join(file_path, file_name)
    # read file data
    try:
        with open(target_file, 'r') as tfile:
            project_json = tfile.readlines()[0]
        tfile.close()
    except:
        print_error(f"Reading '{target_file}' failed !")
        return None
    # decode file data
    try:
        project = jsonpickle.decode(project_json)
        print_success(f"File '{target_file}' decoded successfully")
        return project
    except:
        print_error(f"Decoding '{target_file}' failed !")