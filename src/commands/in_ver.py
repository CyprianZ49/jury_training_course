import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
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


def verify_tests(subtask, cpus, test_dir, verbose = 1, break_on_fail = False):
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
        raise Exception(f"Input verifier binary not found at {in_ver_path}. Run make first.")

    test_path = os.path.join(test_dir, str(subtask), "in")
    os.makedirs(test_path, exist_ok=True)

    tests = [t.name for t in Path(test_path).glob("*.in")]

    tasks = [(in_ver_path, subtask, test_path, t) for t in tests]

    failed_tests = []
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        # futures = [executor.submit(verify, *task) for task in tasks]
        
        future_to_task = {executor.submit(verify, *task): task for task in tasks}
        futures_iterator = as_completed(future_to_task) if break_on_fail else future_to_task.keys()

        for future in futures_iterator:
            task = future_to_task[future]
            test_name = task[3]

        # for i, future in enumerate(futures, 0):
            status, stdout, = future.result()

            if status != 0:
                failed_tests.append(test_name)

                if verbose > 1:
                    print(f"Test {test_name} failed with {status}. Subtask: {subtask} from {test_dir}.")
                    if stdout:
                        print(stdout)

                if break_on_fail:
                    if verbose > 1:
                        print("break_on_fail is enabled. Canceling pending tests and exiting.")
                
                    for f in future_to_task:
                        f.cancel()
                    break

            elif verbose > 2:
                print(f"Passed test: {test_name} from subtask {subtask} from {test_dir}.")

    failed_tests = sorted(failed_tests)

    if verbose > 0:
        if len(failed_tests) == 0:
            print(f"All {len(tests)} tests for subtask {subtask} from {test_dir} have been verified.")
        else:
            print(f"Tests for subtask {subtask} from {test_dir} didn't pass the input verifier.")
            print(f"Failed tests:")
            for test in failed_tests[:5]:
                print(test)
            if len(failed_tests) > 5:
                print("and more")

    return len(failed_tests) == 0, failed_tests


def command_verify_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Verifies handcrafted and generated testcases with provided input verifier.")
    
    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel verification.")

    parser.add_argument("-s", "--subtask", required=True,
                        help="Subtask number or 'all'.")
    
    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="How verbose should the output be. 1 (default) " \
                        "for each subtask results. 2+ for individual test results. " \
                        "0 for only the overall verdict.")
    
    parser.add_argument("-b", "--break_on_fail", action="store_true",
                help="Break execution immediately on the first failure.")

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

    if args.verbose < 0:
        print("Verbose shouldn't be negative be positive.")
        sys.exit(1)

    break_on_fail = args.break_on_fail

    all_passed = True
    for s in subtasks:
        try:
            passed, _ = verify_tests(subtask=s, cpus=args.cpus, test_dir="testcases", verbose=args.verbose, break_on_fail=break_on_fail)
            if not passed:
                all_passed = False
                if break_on_fail:
                    break
        except Exception as e:
            print(e)
            all_passed = False

        gen_test_path = os.path.join("tmp", "gen")
        try:
            passed, _ = verify_tests(subtask=s, cpus=args.cpus, test_dir=gen_test_path, verbose=args.verbose, break_on_fail=break_on_fail)
            if not passed:
                all_passed = False
                if break_on_fail:
                    break
        except Exception as e:
            print(e)
            all_passed = False

    if all_passed:
        print("All selected tests passed.")
    else:
        print("Some tests didn't pass.")
        if args.verbose == 0:
            print("For more info use higher verbosity.")

