import os
import sys
from pathlib import Path
from ruamel.yaml import YAML


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
    ensure_workdir()

    path = Path(os.getcwd()).resolve()
    while path.name != "workdir" and path.parent != path:
        path = path.parent

    root_path = path.parent

    jail_path = os.path.join(root_path, "bin", "sio2jail")

    return jail_path