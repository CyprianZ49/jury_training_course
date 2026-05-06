import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor

def generate_input(gen_path, subtask, test_id):
    in_path = os.path.join("generated", subtask, "in" f"{test_id}.in")
    
    try:
        with open(in_path, "w") as f:
            subprocess.run([gen_path, str(subtask)], stdout=f, check=True)
        return True
    except Exception as e:
        return False

def generate_output(solution_path, subtask, test_id):
    in_path = os.path.join("generated", subtask, "in" f"{test_id}.in")
    out_path = os.path.join("generated", subtask, "out" f"{test_id}.out")

    try:
        with open(in_path, "r") as input:
            with open(out_path, "w") as output:
                subprocess.run([solution_path], stdin=input, stdout=output, check=True)
        return True
    except Exception as e:
        return False

def generate_tests(subtask, n, cpus):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}
        
    util.ensure_type()
    task_type = config.get("type")

    gen = config.get("generator")
    gen_bin = config.get("generator_bin")

    if not gen_bin:
        gen_bin = os.path.splitext(os.path.basename(gen))[0]
    
    gen_path = os.path.join("bin", gen_bin)



def command_generate_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Generates tests with provided generator.")

    parser.add_argument("subtasks", help="")
    
    args = parser.parse_args()

    generate_tests(args.tag)