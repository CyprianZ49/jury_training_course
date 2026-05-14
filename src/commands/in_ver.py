import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def verify(in_ver_path, subtask, test_path, test_name):
    os.makedirs(test_path, exist_ok=True)
    test = os.path.join(test_path, test_name)
    if not os.path.exists(test):
        return -1, f"{test} not found."

    try:
        with open(test, "r") as t:
            result = subprocess.run(
                [in_ver_path, str(subtask)],
                stdin=t, check=False,
                capture_output=True, text=True)
        return result.returncode, result.stdout.strip()
    except Exception as e:
        return -1, f"Exception {e}."


def verify_tests(subtask, cpus, test_dir):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    in_ver = config.get("input_verifier")
    in_ver_bin = config.get("input_verifier_bin")

    if not in_ver_bin:
        in_ver_bin = os.path.splitext(os.path.basename(in_ver))[0]
    
    in_ver_path = os.path.join("tmp", "bin", in_ver_bin)

    if not os.path.exists(in_ver_path):
        print(f"Input verifier binary not found at {in_ver_path}. Run make first.")
        sys.exit(1)

    test_path = os.path.join(test_dir, str(subtask), "in")
    os.makedirs(test_path, exist_ok=True)

    tests = [t.name for t in Path(test_path).glob("*.in")]

    tasks = [(in_ver_path, subtask, test_path, t) for t in tests]

    failed_tests = 0
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        futures = [executor.submit(verify, *task) for task in tasks]
        
        for i, future in enumerate(futures, 0):
            status, stdout, = future.result()

            if status != 0:
                failed_tests += 1
                print(f"Test {tasks[i][3]} failed with {status}. Subtask: {subtask} from {test_dir}.")
                if stdout:
                    print(stdout)

            else:
                print(f"Passed test: {tasks[i][3]} from subtask {subtask} from {test_dir}.")

    if failed_tests == 0:
        print(f"Tests for subtask {subtask} from {test_dir} have been verified.")
    else:
        print(f"Tests for subtask {subtask} from {test_dir} do not pass the input verifier.")


def command_verify_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Verifies handcrafted and generated testcases with provided input verifier.")
    
    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel verification.")

    parser.add_argument("-s", "--subtask", required=True,
                        help="Subtask number or 'all'.")
    
    args = parser.parse_args()

    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    subtask_number = config.get("subtasks")

    if not subtask_number:
        print("No subtask number in config. Aborting.")
        sys.exit(1)

    if args.subtask.lower() == "all":
        subtasks = range(1, subtask_number + 1)
    else:
        try:
            subtasks = [int(args.subtask)]
        except ValueError:
            print(f"Error: Subtask must be a number or 'all'. Received: {args.subtask}")
            sys.exit(1)

    if subtasks[-1] > subtask_number:
        print("Cannot verify a subtask with number larger than subtask number in config. Aborting.")
        sys.exit(1)

    for s in subtasks:
        verify_tests(subtask=s, cpus=args.cpus, test_dir="testcases")
        gen_test_path = os.path.join("tmp", "gen")
        verify_tests(subtask=s, cpus=args.cpus, test_dir=gen_test_path)
