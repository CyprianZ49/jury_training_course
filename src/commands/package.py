import os
import sys
import argparse
import commands.util as util
import shutil
from pathlib import Path
from ruamel.yaml import YAML


def create_package(tag, subtasks, verbose = 1):
    try:    
        os.makedirs(tag, exist_ok=False)
    except FileExistsError:
        raise Exception(f"Package '{tag}' already exists.")

    self_path = os.path.dirname(os.path.realpath(__file__))
    default_config_path = os.path.join(self_path, "default_config.yaml")
    default_checker_path = os.path.join(self_path, "default_checker.cpp")
    oih_path = os.path.join(self_path, "oi.h")

    yaml = YAML()
    yaml.preserve_quotes = True

    if os.path.exists(default_config_path):
        with open(default_config_path, 'r') as f:
            config = yaml.load(f) or {}

        config['tag'] = tag
        config['subtasks'] = subtasks
        config['model_solution'] = f"{tag}.cpp"

        with open(os.path.join(tag, "config.yaml"), 'w') as f:
            yaml.dump(config, f)
    else:
        raise Exception(f"default_config.yaml not found in '{default_config_path}'!")

    package_checker_path = os.path.join(tag, "default_checker.cpp")
    try:
        if not os.path.exists(default_checker_path):
            raise Exception("")
        
        shutil.copy(default_checker_path, package_checker_path)
    except Exception as e:
        raise Exception(f"Failed to copy default checker into the package.")
    
    package_oih_path = os.path.join(tag, "oi.h")
    try:
        if not os.path.exists(oih_path):
            raise Exception("")
        
        shutil.copy(oih_path, package_oih_path)
    except Exception as e:
        raise Exception(f"Failed to copy oi.h into the package.")

    testcases_path = os.path.join(tag, "testcases")

    for i in range(1, subtasks + 1):
        subtask_path = os.path.join(testcases_path, str(i))
    
        os.makedirs(os.path.join(subtask_path, "in"), exist_ok=True)
        os.makedirs(os.path.join(subtask_path, "out"), exist_ok=True)

    inver_tests_path = os.path.join(tag, "inver_tests")

    for i in range(1, subtasks + 1):
        subtask_path = os.path.join(inver_tests_path, str(i))
        os.makedirs(os.path.join(subtask_path, "in"), exist_ok=True)

    os.makedirs(os.path.join(tag, "tmp"))

    if verbose > 0:
        print(f"Created package: {tag}")


def command_create_package():
    util.ensure_workdir()
    path = Path(os.getcwd()).resolve()
    if path.name != "workdir":
        print("Only run create_package in workdir.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Creates a new package.")
    
    parser.add_argument("tag", type=str, help="Problem tag for the package being created.")
    
    parser.add_argument("-s", "--subtasks", type=int, default=1, 
                        help="number of subtasks (default = 1)")

    args = parser.parse_args()

    if args.subtasks < 1:
        print("Subtasks cannot be negative")
        sys.exit(1)

    try:
        create_package(args.tag, args.subtasks)
    except Exception as e:
        print(e)


def delete_package(tag, verbose = 1):
    if not os.path.isdir(tag):
        raise Exception(f"No directory '{tag}'")

    config_path = os.path.join(tag, "config.yaml")

    if not os.path.isfile(config_path):
        raise Exception(f"This doesn't look like a package. There is no config.yaml.")

    yaml = YAML()

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    if config.get("tag") != tag:
        raise Exception(f"Config tag doesn't match directory name. Something is wrong. Aborting.")

    try:
        shutil.rmtree(tag)
        if verbose > 0:
            print(f"Deleted package '{tag}'.")
    except Exception as e:
        raise Exception(f"Failed to delete package '{tag}': {e}")


def command_delete_package():
    util.ensure_workdir()
    path = Path(os.getcwd()).resolve()
    if path.name != "workdir":
        print("Only run delete_package in workdir.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Deletes a package.")

    parser.add_argument("tag", help="Problem tag for the package being deleted.")
    
    args = parser.parse_args()

    try:
        delete_package(args.tag)
    except Exception as e:
        print(e)
