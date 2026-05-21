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
    os.chdir(get_judge_path())


def judge_init(problem_name, user_package_name):
