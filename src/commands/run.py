import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import signal
import html


class Result:
    pass


def check(checker_path, in_dir_path, out_dir_path, test_name, model_solution_path, use_default_out = False):
    os.makedirs(in_dir_path, exist_ok=True)
    os.makedirs(out_dir_path, exist_ok=True)
    test_input = os.path.join(in_dir_path, f"{test_name}.in")
    prog_output = os.path.join(out_dir_path, f"{test_name}.prog_out")
    model_output = os.path.join(out_dir_path, f"{test_name}.model_out")

    if not os.path.exists(test_input):
        return -1, f"Checker error: {test_input} not found."
    
    if not os.path.exists(prog_output):
        return -1, f"Checker error: {prog_output} not found."
    
    if not os.path.exists(model_solution_path):
        return -1, f"Checker error: {model_solution_path} not found."

    if use_default_out:
        model_output = os.path.join(out_dir_path, f"{test_name}.out")
        if not os.path.exists(model_output):
            return -1, f"Checker error: {model_output} not found. When using default_out it is required."
    else:
        try:
            with open(test_input, "r") as input_file, \
                open(model_output, 'w') as output_file:

                result = subprocess.run(
                    [model_solution_path], stdin=input_file, stdout=output_file, check=True
                )
        except Exception as e:
            return -1, f"Checker error: Model solution {model_solution_path} failed to run on input"


    try:
        result = subprocess.run(
            [checker_path, str(test_input), str(prog_output), str(model_output)],
            check=False, capture_output=True, text=True)
        return result.returncode, result.stdout.strip()
    except Exception as e:
        return -1, f"Checker error: Exception {e}."


def run(jail_path, in_dir_path, out_dir_path, test_name, program_bin_path, time_limit, 
        memory_limit, checker_path, model_solution_path, do_cleanup, use_default_out = False):
    
    test_input = os.path.join(in_dir_path, f"{test_name}.in")
    prog_output = os.path.join(out_dir_path, f"{test_name}.prog_out")
    jail_msg = os.path.join(out_dir_path, f"{test_name}.msg")

    if not os.path.exists(test_input):
        return -1, f"{test_input} not found."
    
    os.makedirs(out_dir_path, exist_ok=True)
    
    if not os.path.exists(program_bin_path):
        return -1, f"{program_bin_path} not found."
    
    if not os.path.exists(jail_path):
        return -1, f"{jail_path} not found."

    # based on Sinol-make by Tomasz Grześkiewicz
    command = (f'{jail_path}'
        ' --mount-namespace off'
        ' --pid-namespace off'
        ' --uts-namespace off'
        ' --ipc-namespace off'
        ' --net-namespace off'
        ' --capability-drop off'
        ' --user-namespace off'
        f' --instruction-count-limit {int(2 * time_limit)}M'
        f' --rtimelimit {int(16 * time_limit + 1000)}ms'
        f' --memory-limit {int(memory_limit)}K'
        ' --output-limit 51200K'
        ' --output oiaug'
        f' -- {program_bin_path}'
    )

    execution_dir = os.getcwd()
    result = Result()

    try:
        with open(test_input, "r") as input_file, \
            open(prog_output, "w") as output_file, \
            open(jail_msg, "w") as result_file:

            process = subprocess.Popen(command, shell=True, stdin=input_file, stdout=output_file,
                                        stderr=result_file, preexec_fn=os.setsid, cwd=execution_dir)

            def sigint_handler(signum, frame):
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass
                sys.exit(1)
            signal.signal(signal.SIGINT, sigint_handler)

            process.wait()

        with open(jail_msg, "r") as result_file:
            stderr = result_file.read()
        # with open(prog_output, "r") as output_file:
        #     stdout = output_file.read()

        status_line, message = stderr.splitlines()
        status, code, time_ms, _, memory_kb, _ = status_line.split()

        # print(stderr)
        result.time = int(time_ms)
        result.memory = int(memory_kb)
    except Exception as e:
        raise Exception(f"Failed to run sio2jail on program {program_bin_path}"
                        f"\n\tcommand: `{command}` \n\tstderr:{stderr}\n")

    try:
        os.remove(jail_msg)
    except FileNotFoundError:
        pass

    # sio2 expects ignoring status
    if message.lower() == 'ok':
        result.status = "OK"
    elif message == 'time limit exceeded':
        result.status = "TLE"
    elif message == 'real time limit exceeded':
        result.status = "TLE"
    elif message == 'memory limit exceeded':
        result.status = "MLE"
    elif message == 'output limit exceeded':
        result.status = "RE"
    elif message.startswith('intercepted forbidden syscall'):
        result.status = "RE"
    elif message.startswith('process exited due to signal'):
        result.status = "RE"
    else:
        result.status = "RE"

    if result.status == "OK":
        check_code, result.msg = check(checker_path, in_dir_path, out_dir_path,
                                      test_name, model_solution_path, use_default_out)
        
        if check_code == 0:
            result.status = "ACC"
        else:
            result.status = "WA"

        if do_cleanup:
            prog_output = os.path.join(out_dir_path, f"{test_name}.prog_out")
            try:
                os.remove(prog_output)
            except Exception:
                pass

            model_output = os.path.join(out_dir_path, f"{test_name}.model_out")
            try:
                os.remove(model_output)
            except Exception:
                pass

    return result


def run_tests(subtask, cpus, test_dir, prog, verbose = 1, no_cleanup = False, break_on_fail = False):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    # model_solution
    solution = config.get("model_solution")
    solution_bin = config.get("model_solution_bin")

    if not solution_bin:
        solution_bin = os.path.splitext(os.path.basename(solution))[0]
    
    solution_path = os.path.join("tmp", "bin", solution_bin)

    if not os.path.exists(solution_path):
        raise Exception(f"Model solution binary not found at {solution_path}. Run make first.")

    # checker
    checker = config.get("checker")
    checker_bin = config.get("checker_bin")

    if not checker_bin:
        checker_bin = os.path.splitext(os.path.basename(checker))[0]
    
    checker_path = os.path.join("tmp", "bin", checker_bin)

    if not os.path.exists(checker_path):
        raise Exception(f"Checker binary not found at {checker_path}. Run make first.")

    #limits
    time_limit = config.get("time_limit")
    if not time_limit:
        raise Exception("No time limit set!")

    memory_limit = config.get("memory_limit")
    if not memory_limit:
        raise Exception("No memory limit set!")

    # prog
    target_prog = None
    for entry in config.get("other_solutions", []):
        if entry.get("program") == prog:
            target_prog = entry
            break

    if target_prog == None:
        raise Exception(f"No such program {prog} in other solutions section of config.")

    prog_bin = target_prog.get("program_bin")
    if not prog_bin:
        prog_bin = os.path.splitext(os.path.basename(prog))[0]

    prog_path = os.path.join("tmp", "bin", prog_bin)

    if not os.path.exists(prog_path):
        raise Exception(f"Program '{prog}' binary not found at {prog_path}. Run make first.")

    # jail
    jail_path = util.get_jail_path()
    if jail_path == None or not os.path.exists(jail_path):
        raise Exception(f"Sio2jail binary not found at {jail_path}. Consider running 'setup_sio2jail'.")

    # in/out dir paths
    in_dir_path = os.path.join(test_dir, str(subtask), "in")
    out_dir_path = os.path.join(test_dir, str(subtask), "out")
    os.makedirs(in_dir_path, exist_ok=True)
    os.makedirs(out_dir_path, exist_ok=True)

    # preparing tasks
    tests = [t.name.removesuffix(".in") for t in Path(in_dir_path).glob("*.in")]

    do_cleanup = not no_cleanup

    tasks = [(jail_path, in_dir_path, out_dir_path, t, prog_path, time_limit, memory_limit,
              checker_path, solution_path, do_cleanup, False) for t in tests]

    if verbose > 0:
        print(f"Running program {prog}")

    expected = target_prog.get("pass_subtasks")
    expect_success = subtask in expected

    failed_tests = 0
    test_results = {}
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        future_to_task = {executor.submit(run, *task): task for task in tasks}
        futures_iterator = as_completed(future_to_task) if break_on_fail else future_to_task.keys()

        for future in futures_iterator:
            result = future.result()

            task = future_to_task[future]
            test_name = test_name = task[3]
            test_results[test_name] = result

            if result.status != "ACC":
                failed_tests += 1
                
                if verbose > 1:
                    print(f"Test {test_name} failed with {result.status}. Subtask: {subtask} from {test_dir}")
                    if result.status == "WA":
                        print(result.msg)

                if break_on_fail and expect_success:
                    if verbose > 1:
                        print("break_on_fail is enabled. Canceling pending tests and exiting.")
                
                    for f in future_to_task:
                        f.cancel()
                    break
                

            elif verbose > 2:
                print(f"Passed test: {test_name}. Subtask: {subtask} from {test_dir}.")

    if verbose > 0:
        print(f"Ran {len(test_results)} tests for subtask {subtask} from {test_dir}.")
        if failed_tests == 0:
            print(f"All passed.")
        else:
            print(f"Failed.")

    return (failed_tests == 0), expect_success, test_results


def command_run_tests():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Runs selected program on generated and handcrafted tests.")
    
    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel running.")

    parser.add_argument("-s", "--subtask", required=True,
                        help="Subtask number or 'all'.")
    
    parser.add_argument("-p", "--program", required=True,
                        help="Program to run or 'all'.")
    
    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="How verbose should the output be. 1 (default) " \
                        "for each program and subtask results. 2+ for individual test results. " \
                        "0 for only the overall verdict.")
    
    parser.add_argument("-b", "--break_on_fail", action="store_true",
                help="Break execution immediately on the first failure.")
    
    parser.add_argument("-nc", "--no_cleanup", action="store_true",
                help="Don't clean up output files.")
    
    parser.add_argument("-r", "--raport", action="store_true",
                help="Prepare an execution raport.")
    
    args = parser.parse_args()

    no_cleanup = args.no_cleanup

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
        if no_cleanup:
            print("Running all with no_cleanup isn't advised as it may easily mislead.")
    else:
        try:
            subtasks = [int(args.subtask)]
        except ValueError:
            print(f"Error: Subtask must be a number or 'all'. Received: {args.subtask}")
            sys.exit(1)

    if subtasks[-1] > subtask_number:
        print("Cannot run a subtask with number larger than subtask number in config. Aborting.")
        sys.exit(1)

    if args.verbose < 0:
        print("Verbose shouldn't be negative be positive.")
        sys.exit(1)

    programs = []
    if args.program.lower() == "all":
        for entry in config.get("other_solutions", []):
            programs.append(entry.get("program"))
    else:
        target_prog = None
        for entry in config.get("other_solutions", []):
            if entry.get("program") == args.program:
                target_prog = entry
                break

        if target_prog == None:
            print("No such program in config. Aborting.")
            sys.exit(1)

        programs.append(args.program)

    all_expected = True
    all_results = []

    break_on_fail = args.break_on_fail

    for p in programs:
        # print(p)
        for s in subtasks:
    
            try:
                accepted_hand, expected, results = run_tests(subtask=s, cpus=args.cpus, test_dir="testcases", prog=p, verbose=args.verbose, no_cleanup=no_cleanup, break_on_fail=break_on_fail)
                all_results.append((p, s, "testcases", results))
            except Exception as e:
                if args.verbose > 0:
                    print(f"Running tests for program {p} on subtask {s} raised an exception:")
                    print(e)
                    print("This is considered a failure.")
                all_expected = False
                break

            gen_test_path = os.path.join("tmp", "gen")
            try:
                accepted_gen, expected, results = run_tests(subtask=s, cpus=args.cpus, test_dir=gen_test_path, prog=p, verbose=args.verbose, no_cleanup=no_cleanup, break_on_fail=break_on_fail)
                all_results.append((p, s, "generated", results))
            except Exception as e:
                if args.verbose > 0:
                    print(f"Running tests for program {p} on subtask {s} raised an exception:")
                    print(e)
                    print("This is considered a failure.")
                all_expected = False
                break

            accepted_subtask = accepted_hand and accepted_gen

            if args.verbose > 0:
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
                all_expected = False

            # if args.break_on_fail and not all_expected:
            #     break

        # if args.break_on_fail and not all_expected:
        #     break


    if all_expected:
        print("For each selected program and subtask the results matches the config.")
    else:
        print("Some results do not match the config.")
        if args.verbose == 0:
            print("For more info use higher verbosity.")

    if args.raport:
        report_name = "results_" + args.program
        generate_html_report(all_results, report_name, args.verbose)


def generate_html_report(all_results, filename="results", verbose = 1):
    css_styles = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 30px; background-color: #f9f9f9; color: #333; }
        .table-container { margin-bottom: 40px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        h3 { margin-top: 0; color: #444; border-bottom: 2px solid #eaeaea; padding-bottom: 8px; }
        
        .results-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }
        
        .test-card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 6px;
            text-align: center;
            min-width: 80px;
            background: #fdfdfd;
        }
        
        .test-name { font-weight: 600; font-size: 13px; margin-bottom: 3px; display: block; }
        .status-badge { display: block; font-weight: bold; padding: 4px 6px; border-radius: 4px; color: white; margin-bottom: 0px; font-size: 12px; }
        .acc { background-color: #2e7d32; }
        .wa  { background-color: #d32f2f; }
        .tle { background-color: #fbc02d; color: #333; }
        .mle { background-color: #ef6c00; }
        .re { background-color: #0288d1; }
        .time-label { font-size: 11px; color: #666; font-family: monospace; }
    </style>
    """

    html_content = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<title>Report</title>",
        css_styles,
        "</head>",
        "<body>",
        "<h1>Report</h1>"
    ]

    for p, s, directory, results in all_results:
        sorted_tests = sorted(results.keys())
        
        html_content.append('<div class="table-container">')
        html_content.append(f'<h3>Program: <strong>{html.escape(str(p))}</strong> | Subtask: <strong>{html.escape(str(s))}</strong> | Directory: <strong>{html.escape(str(directory))}</strong></h3>')

        html_content.append('<div class="results-grid">')
        
        for test_name in sorted_tests:
            result = results[test_name]            
            html_content.append('<div class="test-card">')
            html_content.append(f'<span class="test-name">{html.escape(str(test_name))}</span>')
            html_content.append(f'<span class="status-badge {result.status.lower()}">{html.escape(result.status)}</span>')
            html_content.append(f'<span class="time-label">{result.time}s</span>')
            html_content.append('</div>')
            
        html_content.append('</div>')
        html_content.append('</div>')

    html_content.extend(["</body>", "</html>"])

    out_file = filename + ".html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
    
    if verbose > 0:
        print(f"Report successfully generated: {out_file}")


def check_model(cpus, verbose = 1, no_cleanup = False, break_on_fail = False):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    # model_solution
    solution = config.get("model_solution")
    solution_bin = config.get("model_solution_bin")

    if not solution_bin:
        solution_bin = os.path.splitext(os.path.basename(solution))[0]
    
    solution_path = os.path.join("tmp", "bin", solution_bin)

    if not os.path.exists(solution_path):
        raise Exception(f"Model solution binary not found at {solution_path}. Run make first.")

    # checker
    checker = config.get("checker")
    checker_bin = config.get("checker_bin")

    if not checker_bin:
        checker_bin = os.path.splitext(os.path.basename(checker))[0]
    
    checker_path = os.path.join("tmp", "bin", checker_bin)

    if not os.path.exists(checker_path):
        raise Exception(f"Checker binary not found at {checker_path}. Run make first.")

    #limits
    time_limit = config.get("time_limit")
    if not time_limit:
        raise Exception("No time limit set!")

    memory_limit = config.get("memory_limit")
    if not memory_limit:
        raise Exception("No memory limit set!")

    # jail
    jail_path = util.get_jail_path()
    if jail_path == None or not os.path.exists(jail_path):
        raise Exception(f"Sio2jail binary not found at {jail_path}. Consider running 'setup_sio2jail'.")

    # for each subtasks we run model on handcrafted testcases
    
    any_fails = False

    # 

    subtask_number = config.get("subtasks")
    subtasks = range(1, subtask_number + 1)

    test_dir="testcases"

    for subtask in subtasks:

        if verbose > 0:
            print(f"Running model solution on testcases from subtask {subtask}.")

        # in/out dir paths
        in_dir_path = os.path.join(test_dir, str(subtask), "in")
        out_dir_path = os.path.join(test_dir, str(subtask), "out")
        os.makedirs(in_dir_path, exist_ok=True)
        os.makedirs(out_dir_path, exist_ok=True)

        # preparing tasks
        tests = [t.name.removesuffix(".in") for t in Path(in_dir_path).glob("*.in")]

        do_cleanup = not no_cleanup

        tasks = [(jail_path, in_dir_path, out_dir_path, t, solution_path, time_limit, memory_limit,
                checker_path, solution_path, do_cleanup, True) for t in tests]

        expect_success = True

        failed_tests = 0
        test_results = {}
        with ProcessPoolExecutor(max_workers=cpus) as executor:
            future_to_task = {executor.submit(run, *task): task for task in tasks}
            futures_iterator = as_completed(future_to_task) if break_on_fail else future_to_task.keys()

            for future in futures_iterator:
                result = future.result()

                task = future_to_task[future]
                test_name = test_name = task[3]
                test_results[test_name] = result

                if result.status != "ACC":
                    failed_tests += 1
                    
                    if verbose > 1:
                        print(f"Test {test_name} failed with {result.status}. Subtask: {subtask} from {test_dir}")
                        if result.status == "WA":
                            print(result.msg)

                    if break_on_fail and expect_success:
                        if verbose > 1:
                            print("break_on_fail is enabled. Canceling pending tests and exiting.")
                    
                        for f in future_to_task:
                            f.cancel()
                        break
                    

                elif verbose > 2:
                    print(f"Passed test: {test_name}. Subtask: {subtask} from {test_dir}.")

        if verbose > 0:
            print(f"Ran {len(test_results)} tests for subtask {subtask} from {test_dir}.")
            if failed_tests == 0:
                print(f"All passed.")
            else:
                print(f"Failed.")

        if failed_tests > 0:
            any_fails = True

        if any_fails and break_on_fail:
            break

    if any_fails and break_on_fail:
        if verbose > 0:
            print(f"Model solution failed on provided testcases. As break_on_fail is on there is "
                  f"on need to continue testing using trusted brute-force solution.")
        return False

    # then we run model against trusted brute
    # preparing subtasks to do it on and the brute

    trused_brute = config.get("trusted_brute_force_solution")

    if trused_brute == None:
        if verbose > 0:
            print(f"Trusted brute-force solution not provided. Skipping.")
        return True

    target_prog = None
    for entry in config.get("other_solutions", []):
        if entry.get("program") == trused_brute:
            target_prog = entry
            break

    if target_prog == None:
        raise Exception(f"No such program {trused_brute} in other solutions section of config.")

    prog_bin = target_prog.get("program_bin")
    if not prog_bin:
        prog_bin = os.path.splitext(os.path.basename(trused_brute))[0]

    prog_path = os.path.join("tmp", "bin", prog_bin)

    if not os.path.exists(prog_path):
        raise Exception(f"Program '{trused_brute}' binary not found at {prog_path}. Run make first.")

    subtasks = target_prog.get("pass_subtasks")

    for subtask in subtasks:

        if verbose > 0:
            print(f"Running model solution against {trused_brute} on subtask {subtask}.")
        
        test_dir = os.path.join("tmp", "gen")
        
        # in/out dir paths
        in_dir_path = os.path.join(test_dir, str(subtask), "in")
        out_dir_path = os.path.join(test_dir, str(subtask), "out")
        os.makedirs(in_dir_path, exist_ok=True)
        os.makedirs(out_dir_path, exist_ok=True)

        # preparing tasks
        tests = [t.name.removesuffix(".in") for t in Path(in_dir_path).glob("*.in")]

        do_cleanup = not no_cleanup

        tasks = [(jail_path, in_dir_path, out_dir_path, t, solution_path, time_limit, memory_limit,
                checker_path, prog_path, do_cleanup, False) for t in tests]

        expect_success = True

        failed_tests = 0
        test_results = {}
        with ProcessPoolExecutor(max_workers=cpus) as executor:
            future_to_task = {executor.submit(run, *task): task for task in tasks}
            futures_iterator = as_completed(future_to_task) if break_on_fail else future_to_task.keys()

            for future in futures_iterator:
                result = future.result()

                task = future_to_task[future]
                test_name = test_name = task[3]
                test_results[test_name] = result

                if result.status != "ACC":
                    failed_tests += 1
                    
                    if verbose > 1:
                        print(f"Test {test_name} failed with {result.status}. Subtask: {subtask} from {test_dir}")
                        if result.status == "WA":
                            print(result.msg)

                    if break_on_fail and expect_success:
                        if verbose > 1:
                            print("break_on_fail is enabled. Canceling pending tests and exiting.")
                    
                        for f in future_to_task:
                            f.cancel()
                        break
                    

                elif verbose > 2:
                    print(f"Passed test: {test_name}. Subtask: {subtask} from {test_dir}.")

        if verbose > 0:
            print(f"Ran {len(test_results)} tests for subtask {subtask} from {test_dir} against {trused_brute} as solution.")
            if failed_tests == 0:
                print(f"All passed.")
            else:
                print(f"Failed.")

        if failed_tests > 0:
            any_fails = True

        if any_fails and break_on_fail:
            break

    if any_fails:
        if verbose > 0:
            print(f"Model solution failed against {trused_brute}. Check for bugs in both.")
        return False
    
    return True


def check_model_command():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Checks the model solution by running it on handcrafted testcases "
                                     "and against the trusted brute-force solution.")
    
    parser.add_argument("-c", "--cpus", type=int, default=1, 
                        help="Number of CPU cores to use for parallel running.")

    parser.add_argument("-v", "--verbose", type=int, default=1,
                    help="How verbose should the output be.")

    parser.add_argument("-b", "--break_on_fail", action="store_true",
                help="Break execution immediately on the first failure.")

    parser.add_argument("-nc", "--no_cleanup", action="store_true",
                help="Don't clean up output files.")
    
    args = parser.parse_args()

    try:
        status = check_model(cpus=args.cpus, verbose=args.verbose, no_cleanup=args.no_cleanup, break_on_fail=args.break_on_fail)
    except Exception as e:
        status = False
        print(e)
    
    if status:
        print("Model solution passes verification.")


def generate_testcase_outputs_command():
    util.ensure_workdir()
    util.ensure_package()

    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}

    solution = config.get("model_solution")
    solution_bin = config.get("model_solution_bin")

    if not solution_bin:
        solution_bin = os.path.splitext(os.path.basename(solution))[0]
    
    solution_path = os.path.join("tmp", "bin", solution_bin)

    if not os.path.exists(solution_path):
        print(f"Model solution binary not found at {solution_path}. Run make first.")
        sys.exit(1)

    subtask_number = config.get("subtasks")
    subtasks = range(1, subtask_number + 1)

    test_dir="testcases"

    for subtask in subtasks:
        # in/out dir paths
        in_dir_path = os.path.join(test_dir, str(subtask), "in")
        out_dir_path = os.path.join(test_dir, str(subtask), "out")
        os.makedirs(in_dir_path, exist_ok=True)
        os.makedirs(out_dir_path, exist_ok=True)

        # preparing tasks
        tests = [t.name.removesuffix(".in") for t in Path(in_dir_path).glob("*.in")]
        
        for t in tests:
            test_input = os.path.join(in_dir_path, f"{t}.in")
            model_output = os.path.join(out_dir_path, f"{t}.out")

            try:
                with open(test_input, "r") as input_file, \
                    open(model_output, 'w') as output_file:

                    result = subprocess.run(
                        [solution_path], stdin=input_file, stdout=output_file, check=True
                    )
            except Exception as e:
                print(f"Model solution {solution_path} failed to run on subtask {subtask} test {t}.in")
                sys.exit(1)

    print("Generated outputs for testcases using model_solution. This is somewhat ill advised.")