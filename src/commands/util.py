import os
import sys
from pathlib import Path
from ruamel.yaml import YAML
import traceback

def check_workdir():
    path = os.path.abspath(os.getcwd())

    if "workdir" in path.split(os.sep):
        return True
    else:
        return False


def ensure_workdir():
    if not check_workdir():
        print("This command should only be run in workdir.")
        sys.exit(1)


def ensure_package():
    cwd = os.getcwd()
    config_path = os.path.join(cwd, "config.yaml")

    if not os.path.exists(config_path):
        print("This command should only be run in a package directory.")
        sys.exit(1)


def get_jail_path():

    path = Path(os.getcwd()).resolve()
    while (path.name != "workdir" and path.name != "judge") and path.parent != path:
        path = path.parent

    if path.parent == path:
        print("Get_jail_path is run outside workdir and judge. Cannot resolve - exiting.")
        sys.exit(1)

    root_path = path.parent

    jail_path = os.path.join(root_path, "bin", "sio2jail")

    return jail_path


def print_green(text):
    print(f"\033[92m{text}\033[00m")
    

def print_red(text):
    print(f"\033[91m{text}\033[00m")


def print_yellow(text):
    print(f"\033[93m{text}\033[00m")