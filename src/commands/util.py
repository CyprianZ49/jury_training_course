import os
import sys
from ruamel.yaml import YAML

def ensure_workdir():
    path = os.path.abspath(os.getcwd())

    if "workdir" not in path.split(os.sep):
        print("This command should only be run in workdir.")
        sys.exit(1)

def ensure_package():
    cwd = os.getcwd()
    config_path = os.path.join(cwd, "config.yaml")

    if not os.path.exists(config_path):
        print("This command should only be run in a package directory.")
        sys.exit(1)