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

from commands.util import print_red, print_yellow, print_green


# verifications are always break_on_fail = True
def internal_verify_package(cpus, verbose = 1, skip_gen = False, raport = False, extra_info = None):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    time_limit = config.get("time_limit")

    if not time_limit:
        if verbose > 0:
            print_red("Verification failed: time limit not provided.")
        return False
        
    memory_limit = config.get("memory_limit")

    if not memory_limit:
        if verbose > 0:
            print_red("Verification failed: memory limit not provided.")
        return False

    subtasks = config.get("subtasks")

    if not subtasks:
        if verbose > 0:
            print_red("Verification failed: subtasks not provided.")
        return False

    gen_test_number = config.get("number_of_generated_testcases_per_subtask")

    if not gen_test_number or len(gen_test_number) != subtasks:
        if verbose > 0:
            print_red("Verification failed: number of tests to generate for each subtask not provided.")
        return False

    checker = config.get("checker")

    if not checker:
        if verbose > 0:
            print_red("Verification failed: checker not provided.")
        return False
    
    checker_bin = config.get("checker_bin")
    if not checker_bin:
        checker_bin = os.path.splitext(os.path.basename(checker))[0]


    model_solution = config.get("model_solution")

    if not model_solution:
        if verbose > 0:
            print_red("Verification failed: model_solution not provided.")
        return False
    
    model_solution_bin = config.get("model_solution_bin")
    if not model_solution_bin:
        model_solution_bin = os.path.splitext(os.path.basename(model_solution))[0]

    trusted_brute = config.get("trusted_brute_force_solution")

    if not trusted_brute:
        if verbose > 0:
            print_yellow("Verification warning: trusted_brute_force_solution not selected.")

    generator = config.get("generator")

    if not generator:
        if verbose > 0:
            print_red("Verification failed: generator not provided.")
        return False
    
    generator_bin = config.get("generator_bin")
    if not generator_bin:
        generator_bin = os.path.splitext(os.path.basename(generator))[0]
    
    input_verifier = config.get("input_verifier")

    if not input_verifier:
        if verbose > 0:
            print_red("Verification failed: input_verifier not provided.")
        return False
    
    input_verifier_bin = config.get("input_verifier_bin")
    if not input_verifier_bin:
        input_verifier_bin = os.path.splitext(os.path.basename(input_verifier))[0]

    if verbose > 0:
        print("Config verified.")

    if not skip_gen:

        if verbose > 0:
            print("Deleting old generated tests and generating new ones.")

        for s in range(1, subtasks + 1):
            try:
                gen.delete_tests(s, verbose - 1)
            except Exception as e:
                if verbose > 0:
                    print(f"Verification failed: Old generated test deletion failed for subtask {s}.")
                    print(e)
                return False
            
            try:
                gen.generate_tests(s, 1, gen_test_number[s - 1], cpus, verbose - 1)
            except Exception as e:
                if verbose > 0:
                    print(f"Verification failed: Test generation failed for subtask {s}.")
                    print(e)
                return False
        
        if verbose > 0:
            print("Verifying tests.")

        gen_test_path = os.path.join("tmp", "gen")
        test_dirs = [gen_test_path, "testcases"]

        for t_dir in test_dirs:
            for s in range(1, subtasks + 1):
                try:
                    passed, _ = inver.verify_tests(s, cpus, t_dir, verbose - 1, True)
                    if not passed:
                        raise Exception(f"Tests for subtask {s} from {t_dir} didn't pass the input verifier.")
                except Exception as e:
                    if verbose > 0:
                        print_red(f"Verification failed: input verification didn't pass.")
                        print(e)
                    if extra_info is not None:
                        extra_info.append("inver")
                    return False

    if skip_gen and verbose > 0:
        print("Test generation and verification was skipped.")

    # test inver

    if verbose > 0:
        print("Verifing that input verifier doesn't pass any inver_tests.")

    for s in range(1, subtasks + 1):
        try:
            passed = inver.test_inver(s, cpus, 0)
            if not passed:
                raise Exception(f"Input verifier passed some tests from inver_tests for subtask {s}")
        except Exception as e:
            if verbose > 0:
                print_red(f"Verification failed: inver_tests verification didn't pass.")
                print(e)
            if extra_info is not None:
                extra_info.append("inver_tests")
            return False
        
    # 

    if verbose > 0:
        print("Verifying model_solution using testcases and trusted brute-force solution.")

    try:
        success = run.check_model(cpus, verbose - 1, no_cleanup = False, break_on_fail = True)
        if not success:
            raise Exception("Model solution check returns False.")
    except Exception as e:
        if verbose > 0:
            print("Verification failed: model_solution didn't pass.")
            print(e)
        if extra_info is not None:
            extra_info.append("model")
        return False

    if verbose > 0:
        print("Running all provided programs on all tests and checking if correct subtasks pass.")

    #

    programs = []
    for entry in config.get("other_solutions", []):
        programs.append(entry.get("program"))

    all_expected = True
    all_results = []

    for p in programs:

        expected_program = True
        if verbose > 1:
            print(f"Running program {p} on all tests.")

        for s in range(1, subtasks + 1):
            
            if verbose > 1:
                print(f"Subtask {s}.")

            try:
                accepted_hand, expected, results = run.run_tests(s, cpus, "testcases", p, verbose - 1, False, True)
                all_results.append((p, s, "testcases", results))
            except Exception as e:
                if verbose > 1:
                    print(f"Running tests for program {p} on subtask {s} raised an exception:")
                    print(e)
                    print("This is considered a failure.")
                expected_program = False
                break

            gen_test_path = os.path.join("tmp", "gen")
            try:
                accepted_gen, expected, results = run.run_tests(s, cpus, gen_test_path, p, verbose - 1, False, True)
                all_results.append((p, s, "generated", results))
            except Exception as e:
                if verbose > 1:
                    print(f"Running tests for program {p} on subtask {s} raised an exception:")
                    print(e)
                    print("This is considered a failure.")
                expected_program = False
                break

            accepted_subtask = accepted_hand and accepted_gen

            if verbose > 2:
                if expected and accepted_subtask:
                    print(f"Program {p} PASSES subtask {s}.")
                    print(f"This is expected behaviour.")
                elif expected and not accepted_subtask:
                    print(f"Program {p} FAILS subtask {s}.")
                    print(f"This is unexpected as it does not match with config. "
                        "Check for bugs in the program or reconsider it's runtime.")
                elif not expected and accepted_subtask:
                    print(f"Program {p} PASSES subtask {s}.")
                    print(f"This is unexpected as it does not match with config. "
                        "Consider generating more tests or making tests for this subtask more difficult.")
                elif not expected and not accepted_subtask:
                    print(f"Program {p} FAILS subtask {s}.")
                    print(f"This is expected behaviour.")

                print("")

            if accepted_subtask != expected:
                expected_program = False
        
        if expected_program:
            if verbose > 0:
                print_green(f"Program {p} behaviour matches config.")
        else:
            if verbose > 0:
                print_red(f"Program {p} behaviour doesn't match config.")
            all_expected = False

    if raport:
        run.generate_html_report(all_results, "verification_results", verbose)

    if verbose > 0:
        if all_expected:
            print_green("All programs behave according to config.")
        else:
            print_red("Some programs do not behave according to config.")
            
    if not all_expected:
        if extra_info is not None:
            extra_info.append("other")
        return False

    return True


def command_internal_verify_package():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Verifies package quality internally.")

    parser.add_argument("-c", "--cpus", type=int, default=1, 
                    help="Number of CPU cores to use for parallel tasks.")
    
    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="How verbose should the output be. 1 (default) " \
                        "for basic info on verification phases. 2+ for more detailed information " \
                        "(verification phases are run on verbosity 1 level lower than this). " \
                        "0 for only the overall verdict.")

    parser.add_argument("-s", "--skip_gen", action="store_true",
                help="Skip tests generation and verification. Use with caution!")

    parser.add_argument("-r", "--raport", action="store_true",
                help="Prepare an execution raport.")

    args = parser.parse_args()

    res = internal_verify_package(args.cpus, args.verbose, args.skip_gen, args.raport)

    if res:
        print_green("This package is internally consistent.")
    else:
        print_red("This package has internal problems.")