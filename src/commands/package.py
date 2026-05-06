import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML


def create_package(tag, type, subtasks):
    try:    
        os.makedirs(tag, exist_ok=False)
    except FileExistsError:
        print(f"Package '{tag}' already exists.")
        sys.exit(1)

    self_path = os.path.dirname(os.path.realpath(__file__))
    default_config_path = os.path.join(self_path, "default_config.yaml")

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    if os.path.exists(default_config_path):
        with open(default_config_path, 'r') as f:
            config = yaml.load(f) or {}

        config['tag'] = tag
        config['type'] = type
        config['subtasks'] = subtasks

        with open(os.path.join(tag, "config.yaml"), 'w') as f:
            yaml.dump(config, f)
    else:
        print(f"default_config.yaml not found in '{default_config_path}'!")

    testcases_path = os.path.join(tag, "testcases")

    for i in range(1, subtasks + 1):
        subtask_path = os.path.join(testcases_path, str(i))
        
        os.makedirs(os.path.join(subtask_path, "in"), exist_ok=True)

        if type == "output":
            os.makedirs(os.path.join(subtask_path, "out"), exist_ok=True)

    os.makedirs(os.path.join(tag, "bin"))

    print(f"Created package: {tag}")


def command_create_package():
    util.ensure_workdir()

    parser = argparse.ArgumentParser(description="Creates a new package.")
    
    parser.add_argument("tag", type=str, help="Problem tag for the package being created.")
    
    parser.add_argument("--type", choices=["output", "checker"], default="output", 
                        help="output for tasks with a single output (defualt) "
                             "checker for tasks that require a cheker program")
    
    parser.add_argument("--subtasks", type=int, default=1, 
                        help="number of subtasks (default = 1)")

    args = parser.parse_args()

    if args.subtasks < 1:
        print("Subtasks cannot be negative")
        sys.exit(1)

    create_package(args.tag, args.type, args.subtasks)


def delete_package(tag):
    if not os.path.isdir(tag):
        print(f"No directory '{tag}'")
        sys.exit(1)

    config_path = os.path.join(tag, "config.yaml")

    if not os.path.isfile(config_path):
        print(f"This doesn't look like a package. There is no config.yaml.")
        sys.exit(1)

    yaml = YAML()

    try:
        with open(config_path, 'r') as f:
            config = yaml.load(f) or {}
        if config.get("tag") != tag:
            print(f"Config tag doesn't match directory name. Something is wrong. Aborting.")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to read config.yaml")
        sys.exit(1)

    try:
        shutil.rmtree(tag)
        print(f"Deleted package '{tag}'.")
    except Exception as e:
        print(f"Failed to delete package '{tag}': {e}")
        sys.exit(1)


def command_delete_package():
    util.ensure_workdir()

    parser = argparse.ArgumentParser(description="Deletes a package.")

    parser.add_argument("tag", help="Problem tag for the package being deleted.")
    
    args = parser.parse_args()

    delete_package(args.tag)