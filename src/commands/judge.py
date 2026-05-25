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
    project_dir = current_dir.parent.parent
    return project_dir


def get_judge_path():
    judge_path = os.path.join(get_project_path(), "judge")
    os.makedirs(judge_path, exist_ok=True)
    return judge_path


def restore_master():

    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    master_path = config.get("master_path")

    for item in Path(judge_dir).iterdir():
        if str(item) == config_path:
            continue
            
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            raise Exception(f"Failed to restore master package state. "
                            f"Problem with deleting old files: {e}.")

    problem_name = Path(master_path).name
    target = os.path.join(judge_dir, problem_name)
    try:
        shutil.copytree(master_path, target, symlinks=False)
    except Exception as e:
            raise Exception(f"Failed to restore master package state. "
                            f"Problem with copying master package: {e}.")


def judge_init(problem_tag, user_package_tag):

    problems_path = os.path.join(get_project_path(), "problems")
    master_path = None

    for item in Path(problems_path).iterdir():
        if item.is_dir() and item.name == problem_tag:
            master_path = item.resolve()
    
    if not master_path:
        raise Exception(f"No problem with tag {problem_tag} in problems (no such master package).")

    try:
        subprocess.run(
            ["make"], 
            cwd=master_path, 
            check=True
        )
    except Exception as e:
        raise Exception(f"Makefile in master package failed with {e}.")

    workdir_path = os.path.join(get_project_path(), "workdir")
    user_path = None

    for item in Path(workdir_path).iterdir():
        if item.is_dir() and item.name == user_package_tag:
            user_path = item.resolve()

    if not user_path:
        raise Exception(f"No package {user_package_tag} in workdir.")

    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    config_data = {
        "problem_tag": problem_tag, 
        "master_path": str(master_path),
        "user_path": str(user_path)
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
        print("Init successful.")
    except Exception as e:
        print(f"Judge init failed: {e}")

def judge_solution(cpus, raport = False, verbose = 0):
    restore_master()

    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    with open(config_path, 'r') as f:
        judge_config = yaml.load(f) or {}

    problem_tag = judge_config.get("problem_tag")

    user_path = judge_config.get("user_path")

    if not user_path:
        raise Exception("Judge_config missing user package path. Judge is likely not initiated.")

    config_path = os.path.join(user_path, "config.yaml")
    
    with open(config_path, 'r') as f:
        user_config = yaml.load(f) or {}

    user_model = user_config.get("model_solution")

    if not user_model:
        raise Exception("User package config has no model solution.")
    
    user_model_bin = user_config.get("model_solution_bin")

    if not user_model_bin:
        user_model_bin = os.path.splitext(os.path.basename(user_model))[0]

    user_model_path = os.path.join(user_path, "tmp", "bin", user_model_bin)

    judge_bin_dir = os.path.join(judge_dir, problem_tag, "tmp", "bin")

    os.makedirs(judge_bin_dir, exist_ok=True)

    model_name = "user_" + user_model_bin

    judge_copy_of_user_model = os.path.join(judge_bin_dir, model_name)

    shutil.copy2(user_model_path, judge_copy_of_user_model)

    judge_package_config_path = os.path.join(judge_dir, problem_tag, "config.yaml")

    with open(judge_package_config_path, 'r') as f:
        judge_package_config = yaml.load(f) or {}

    subtasks = judge_package_config.get("subtasks")
    subtask_list = list(range(1, subtasks + 1))

    model_entry = {
        "name": "user_model_solution",
        "program": model_name + ".cpp",
        "program_bin": model_name,
        "pass_subtasks": subtask_list,
    }

    if "other_solutions" not in judge_package_config or judge_package_config["other_solutions"] is None:
        judge_package_config["other_solutions"] = []

    judge_package_config["other_solutions"].append(model_entry)

    with open(judge_package_config_path, "w") as f:
        yaml.dump(judge_package_config, f)

    # setup done - now running the model_solution as one of other_solutions

    save_dir = os.getcwd()

    os.chdir(os.path.join(judge_dir, problem_tag))

    all_results = []
    all_success = True

    if verbose > 0:
        print("Running user model solution on master tests.")

    for s in subtask_list:

        try:
            success, _, results = run.run_tests(s, cpus, "testcases", model_name + ".cpp", 0, False, True)
            all_results.append(("user_model_solution", s, "testcases", results))
        except Exception as e:
            if verbose > 0:
                print(f"Judging model solution on subtask {s} testcases raised an exception:")
                print(e)
                print("This is considered a failure.")
            all_success = False
        
        if not success:
            if verbose > 0:
                print(f"Model solution failed on subtask {s} testcases.")
            all_success = False
        else:
            if verbose > 1:
                print(f"Model solution passes subtask {s} testcases.")
        
        gen_test_path = os.path.join("tmp", "gen")

        try:
            success, _, results = run.run_tests(s, cpus, gen_test_path, model_name + ".cpp", 0, False, True)
            all_results.append(("user_model_solution", s, gen_test_path, results))
        except Exception as e:
            if verbose > 0:
                print(f"Judging model solution on subtask {s} {gen_test_path} raised an exception:")
                print(e)
                print("This is considered a failure.")
            all_success = False

        if not success:
            if verbose > 0:
                print(f"Model solution failed on subtask {s} {gen_test_path}.")
            all_success = False
        else:
            if verbose > 1:
                print(f"Model solution passes subtask {s} {gen_test_path}.")

    if raport:
        run.generate_html_report(all_results, "model_solution_judge_report", verbose)

    os.chdir(save_dir)

    return all_success


def judge_solution_command():
    parser = argparse.ArgumentParser(description="Judges the model solution of user package.")

    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel running.")
    
    parser.add_argument("-r", "--raport", action="store_true",
                help="Prepare judging raport.")

    parser.add_argument("-v", "--verbose", type=int, default=0,
                        help="How verbose should the output be. 1 " \
                        "for information on what failed." \
                        "0 (default) for only the overall verdict. " \
                        "2 for more details.")

    args = parser.parse_args()

    try:
        success = judge_solution(args.cpus, args.raport, args.verbose)
        if success:
            print("Your model solution passes the master package tests.")
        else:
            print("Your model solution fails the master package tests.")

    except Exception as e:
        print(f"Judge_solution failed: {e}")


def judge_package(cpus, raport = False, verbose = 0):
    restore_master()

    judge_dir = get_judge_path()

    yaml = YAML()
    config_path = os.path.join(judge_dir, "judge_config.yaml")

    with open(config_path, 'r') as f:
        judge_config = yaml.load(f) or {}

    problem_tag = judge_config.get("problem_tag")

    user_path = judge_config.get("user_path")

    if not user_path:
        raise Exception("Judge_config missing user package path. Judge is likely not initiated.")

    config_path = os.path.join(user_path, "config.yaml")
    
    with open(config_path, 'r') as f:
        user_config = yaml.load(f) or {}

    master_path = judge_config.get("master_path")

    if not master_path:
        raise Exception("Judge_config missing user master path. Judge is likely not initiated.")

    config_path = os.path.join(master_path, "config.yaml")

    with open(config_path, 'r') as f:
        master_config = yaml.load(f) or {}

    subtasks = range(1, master_config.get("subtasks") + 1)

    save_dir = os.getcwd()

    os.chdir(os.path.join(judge_dir, problem_tag))

    # setup done moving on to judging

    master_memory = master_config.get("memory_limit")
    user_memory = user_config.get("memory_limit")

    if user_memory != master_memory:
        if verbose > 0:
            print("User memory limit is different from the one in the task.")
        return False

    user_trusted_brute = user_config.get("trusted_brute_force_solution")

    if user_trusted_brute is None:
        if verbose > 0:
            print("A quality package should have a trusted brute force solution.")
        return False
    
    # checker and inver

    bin_dir = os.path.join("tmp", "bin")

    if verbose > 0:
        print("Judging checker and input verifier.")

    user_checker = user_config.get("checker")
    user_inver = user_config.get("input_verifier")

    if not user_checker:
        if verbose > 0:
            print("User package config has no checker.")
        return False
    if not user_inver:
        if verbose > 0:
            print("User package config has no input_verifier.")
        return False

    user_checker_bin = user_config.get("checker_bin")
    user_inver_bin = user_config.get("input_verifier_bin")

    if not user_checker_bin:
        user_checker_bin = os.path.splitext(os.path.basename(user_checker))[0]
    if not user_inver_bin:
        user_inver_bin = os.path.splitext(os.path.basename(user_inver))[0]

    user_checker_path = os.path.join(user_path, "tmp", "bin", user_checker_bin)
    user_inver_path = os.path.join(user_path, "tmp", "bin", user_inver_bin)

    os.makedirs(bin_dir, exist_ok=True)

    checker_name = "user_" + user_checker_bin
    inver_name = "user_" + user_inver_bin

    judge_copy_of_user_checker = os.path.join(bin_dir, checker_name)
    judge_copy_of_user_inver = os.path.join(bin_dir, inver_name)

    shutil.copy2(user_checker_path, judge_copy_of_user_checker)
    shutil.copy2(user_inver_path, judge_copy_of_user_inver)

    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        internal_config = yaml.load(f) or {}

    internal_config["checker"] =  checker_name + ".cpp"
    internal_config["checker_bin"] = checker_name
    internal_config["input_verifier"] =  inver_name + ".cpp"
    internal_config["input_verifier_bin"] = inver_name

    with open(config_path, "w") as f:
        yaml.dump(internal_config, f)

    ver_status = verfify.internal_verify_package(cpus, verbose - 1, False, raport)
    
    if not ver_status:
        if verbose > 0:
            print("Checker or input doesn't work for the master package.")
        return False
    
    for s in subtasks:
        try:
            _, failed = inver.verify_tests(subtask=s, cpus=cpus, test_dir="inver_tests", verbose=verbose - 1, break_on_fail=False)
        except Exception as e:
            if verbose > 0:
                print(f"Input verifier tests raised an exception: {e}")
            return False
        
        inver_tests_path = os.path.join("inver_tests", str(s), "in")
        test_count = sum(1 for x in Path(inver_tests_path).iterdir() if x.is_file())
        if len(failed) != test_count:
            if verbose > 0:
                print(f"Your input verifier passes a test for subtask {s} which isn't a valid test incorrect.")
            return False

    if verbose > 0:
        print("Checker and input verifier are high quality.")

    # testcases + generator

    os.chdir(save_dir)
    
    restore_master()

    os.chdir(os.path.join(judge_dir, problem_tag))

    if verbose > 0:
        print("Judging testcases and generator.")
    
    # replacing generator

    user_generator = user_config.get("generator")

    if not user_generator:
        if verbose > 0:
            print("User package config has no generator.")
        return False

    user_generator_bin = user_config.get("generator_bin")

    if not user_generator_bin:
        user_generator_bin = os.path.splitext(os.path.basename(user_generator))[0]

    user_generator_path = os.path.join(user_path, "tmp", "bin", user_generator_bin)

    generator_name = "user_" + user_generator_bin

    judge_copy_of_user_generator = os.path.join(bin_dir, generator_name)

    shutil.copy2(user_generator_path, judge_copy_of_user_generator)

    # replacing testcases

    internal_testcases = os.path.join(judge_dir, problem_tag, "testcases")
    user_testcases = os.path.join(user_path, "testcases")

    if Path(internal_testcases).exists():
        shutil.rmtree(internal_testcases)

    if Path(user_testcases).exists():
        shutil.copytree(user_testcases, internal_testcases)
    else:
        raise Exception("User testcases directory not found.")

    # altering config

    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        internal_config = yaml.load(f) or {}

    internal_config["number_of_generated_testcases_per_subtask"] = user_config.get("number_of_generated_testcases_per_subtask")
    internal_config["generator"] =  generator_name + ".cpp"
    internal_config["generator_bin"] = generator_name

    with open(config_path, "w") as f:
        yaml.dump(internal_config, f)

    # running

    ver_status = verfify.internal_verify_package(cpus, verbose - 1, False, raport)

    if not ver_status:
        if verbose > 0:
            print("Testcases or generator fail when run on the master package. " \
            "This can be either because of master input verifier finding mistakes " \
            "or because your tests are too weak and some solutions pass more subtasks " \
            "than they should. For more info use higher verbosity.")
        return False
    
    if verbose > 0:
        print("Testcases and generator are high quality.")

    os.chdir(save_dir)

    # judge_model

    try:
        success = judge_solution(cpus, raport, verbose)
    except Exception as e:
        if verbose > 0:
            print(f"Judge_solution failed: {e}")
        return False

    if not success:
        if verbose > 0:
            print("Your model solution fails the master package tests.")
        return False
    
    if verbose > 0:
        print("Your model solution is high quality.")

    # time for user other solutions

    os.chdir(save_dir)

    restore_master()

    os.chdir(os.path.join(judge_dir, problem_tag))

    if verbose > 0:
        print("Judging other solutions on master tests.")

    # altering config and copying binaries
    # on the side extracting all expected combs
    all_subtask_combs_user = set()

    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        internal_config = yaml.load(f) or {}

    programs = []

    other_solutions = user_config.get("other_solutions")

    internal_bin = os.path.join(judge_dir, problem_tag, "tmp", "bin")

    for prog in other_solutions:

        prog_bin = os.path.splitext(os.path.basename(prog["program"]))[0]

        prog["program"] = f"user_{prog['program']}"
        programs.append(prog["program"])
            
        if prog.get("program_bin") is not None:
            prog_bin = prog["program_bin"]
            prog["program_bin"] = f"user_{prog['program_bin']}"

        user_prog_bin_path = os.path.join(user_path, "tmp", "bin", prog_bin)
        internal_prog_bin_path = os.path.join(internal_bin, "user_" + prog_bin)

        if Path(user_prog_bin_path).exists():
            shutil.copy2(user_prog_bin_path, internal_prog_bin_path)
        else:
            raise Exception(f"Binary of program {prog["pogram"]} missing in user package. Run make.")

        all_subtask_combs_user.add(tuple(prog["pass_subtasks"]))

    internal_config["other_solutions"] = other_solutions    

    internal_config["trusted_brute_force_solution"] = None

    with open(config_path, "w") as f:
        yaml.dump(internal_config, f)

    # running other solutions

    ver_status = verfify.internal_verify_package(cpus, verbose - 1, False, raport)

    if not ver_status:
        if verbose > 0:
            print("Some other_solutions do not behave according to config.")
        return False
    
    if verbose > 0:
        print("All other_solutions behave according to config.")

    # end

    if verbose > 0:
        print("Checking if the user package contains an other_solution " \
        "that passes every sensible subtask combination.")

    all_subtask_combs_master = set()

    other_solutions_master = master_config.get("other_solutions")
    for prog in other_solutions_master:
        all_subtask_combs_master.add(tuple(prog["pass_subtasks"]))

    missing_combs = all_subtask_combs_master - all_subtask_combs_user

    if missing_combs:
        if verbose > 0:
            print("List of subtask combinations for which a natural solution " \
            "exists (as seen in master) that are not represented in user package:")
            print(missing_combs)
            print("A quality package should contain an other_solution for every " \
            "reasonable subtask combination.")
        return False
    
    bonus_combs = all_subtask_combs_user - all_subtask_combs_master

    if bonus_combs and verbose > 0:
        print("Your package has some solutions which pass a subtask combination not " \
        "present anywhere in master. This means that either: you thought of a very " \
        "interesting solution, you specifically used subtask constraints to achieve this " \
        "artificially or the master package is imperfect after all.")
        print("If you truly outsmarted the master package - congratulations!")
        print(f"Your unique combinations: {bonus_combs}")

    os.chdir(save_dir)

    return True


def judge_package_command():
    parser = argparse.ArgumentParser(description="Judges the entire user package.")

    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel running.")
    
    parser.add_argument("-r", "--raport", action="store_true",
                help="Prepare judging raport for the phase that fails.")

    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="How verbose should the output be. 1 " \
                        "for information on judging phases and which one failed." \
                        "0 (default) for only the overall verdict. " \
                        "2 for more details.")

    args = parser.parse_args()

    try:
        success = judge_package(args.cpus, args.raport, args.verbose)
        if success:
            print("Your package is high quality.")
        else:
            print("Your package still needs some work.")

    except Exception as e:
        print(f"Judge_package failed: {e}")