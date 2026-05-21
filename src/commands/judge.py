import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import hashlib

import commands.generate as gen
import commands.in_ver as inver
import commands.run as run
import commands.verify as verfify


def get_project_path():
    current_dir = Path(__file__).resolve().parent
    project_dir = current_dir.parent
    return project_dir


def get_judge_path():
    judge_path = os.path.join(get_judge_path, "judge")
    return judge_path


def restore_master():
    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    master_path = config.get("master_path")

    for item in judge_dir.iterdir():
        if item == config_path:
            continue
            
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            raise Exception(f"Failed to restore master package state. "
                            f"Problem with deleting old files: {e}.")
        
    try:
        shutil.copytree(master_path, judge_dir, symlinks=False)
    except Exception as e:
            raise Exception(f"Failed to restore master package state. "
                            f"Problem with copying master package: {e}.")


def judge_init(problem_tag, user_package_tag):

    problems_path = os.path.join(get_project_path(), "problems")
    master_path = None

    for item in problems_path.iterdir():
        if item.is_dir() and item.name == problem_tag:
            master_path = item.resolve()

    if not master_path:
        raise Exception(f"No problem with tag {problem_tag}.")

    workdir_path = os.path.join(get_project_path(), "workdir")
    user_path = None

    for item in workdir_path.iterdir():
        if item.is_dir() and item.name == user_package_tag:
            user_path = item.resolve()

    if not user_path:
        raise Exception(f"No package {user_package_tag} in workdir.")

    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    config_data = {
        "master_path": master_path,
        "user_path": user_path
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)

    try:
        restore_master()
    except Exception as e:
        raise Exception(f"Problem with init: {e}")
    

def judge_init_command():
    parser = argparse.ArgumentParser(description="Prepares user package to be judged.")
    
    parser.add_argument("problem_tag", help="Tag of the problem.")

    parser.add_argument("user_package_tag", help="Tag of the user package for the problem.")

    args = parser.parse_args()

    try:
        judge_init(args.problem_tag, args.user_package_tag)
    except Exception as e:
        print(f"Judge init failed: {e}")