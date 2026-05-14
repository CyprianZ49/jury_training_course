import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor


def generate(gen_path, subtask, test_id):
    test_path = os.path.join("tmp", "gen")
    subtask_in_dir = os.path.join(test_path, str(subtask), "in")
    os.makedirs(subtask_in_dir, exist_ok=True)
    in_path = os.path.join(subtask_in_dir, f"{test_id}.in")
    
    try:
        with open(in_path, "w") as f:
            subprocess.run([gen_path, str(subtask)], stdout=f, check=True)
        return True
    except Exception as e:
        return False

def generate_tests(subtask, start, n, cpus, verbose = 1):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    gen = config.get("generator")
    gen_bin = config.get("generator_bin")

    if not gen_bin:
        gen_bin = os.path.splitext(os.path.basename(gen))[0]
    
    gen_path = os.path.join("tmp", "bin", gen_bin)

    if not os.path.exists(gen_path):
        raise Exception(f"Generator binary not found at {gen_path}. Run make first.")

    subtask_dir = os.path.join("tmp", "gen", str(subtask))
    os.makedirs(subtask_dir, exist_ok=True)

    tasks = [(gen_path, subtask, i) for i in range(start, start + n)]

    failed_generations = 0

    with ProcessPoolExecutor(max_workers=cpus) as executor:
        futures = [executor.submit(generate, *task) for task in tasks]
        
        for i, future in enumerate(futures, start):
            if not future.result():
                failed_generations += 1

                if verbose > 0:
                    print(f"Test {i} for subtask {subtask} failed to generate.")

    if verbose > 0:
        print(f"Tests for subtask {subtask} have been generated.")
        print(f"{n - failed_generations} / {n} successful.")

    return failed_generations == 0


def command_generate_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Generates tests with provided generator.")

    parser.add_argument("-n", type=int, required=True, 
                        help="Number of tests to generate.")
    
    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel generation.")

    parser.add_argument("-s", "--subtask", required=True,
                        help="Subtask number or 'all'.")
    
    parser.add_argument("--start", type=int, default=1, 
                        help="The index to start generating from (default = 1)")
    
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
        print("Cannot generate a subtask with number larger than subtask number in config. Aborting.")
        sys.exit(1)

    if subtasks[0] < 1:
        print("Cannot generate a subtask with number lower than 1. Aborting.")
        sys.exit(1)

    for s in subtasks:
        try:
            generate_tests(subtask=s, n=args.n, cpus=args.cpus, start=args.start)
        except Exception as e:
            print(e)


def delete_tests(subtask, verbose = 1):
    subtask_dir = os.path.join("tmp", "gen", str(subtask))
    
    if not os.path.isdir(subtask_dir):
        raise Exception(f"No generated testst for subtasl {subtask} detected.")

    try:
        shutil.rmtree(subtask_dir)
        if verbose > 0:
            print(f"Deleted generated tests for subtask {subtask}.")
    except Exception as e:
        raise Exception(f"Failed to delete tests for subtask {subtask}: {e}.")


def command_delete_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Deletes generated tests.")

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
        print("Cannot generate a subtask with number larger than subtask number in config. Aborting.")
        sys.exit(1)

    if subtasks[0] < 1:
        print("Cannot generate a subtask with number lower than 1. Aborting.")
        sys.exit(1)

    for s in subtasks:
        try:
            delete_tests(subtask=s)
        except Exception as e:
            print(e)
