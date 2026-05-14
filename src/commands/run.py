import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import signal


class Result:
    pass


def check(checker_path, in_dir_path, out_dir_path, test_name, model_solution_path):
    os.makedirs(in_dir_path, exist_ok=True)
    os.makedirs(out_dir_path, exist_ok=True)
    test_input = os.path.join(in_dir_path, f"{test_name}.in")
    prog_output = os.path.join(out_dir_path, f"{test_name}.out")

    if not os.path.exists(test_input):
        return -1, f"Checker error: {test_input} not found."
    
    if not os.path.exists(prog_output):
        return -1, f"Checker error: {prog_output} not found."
    
    if not os.path.exists(model_solution_path):
        return -1, f"Checker error: {model_solution_path} not found."

    try:
        result = subprocess.run(
            [checker_path, str(test_input), str(prog_output), str(model_solution_path)],
            check=False, capture_output=True, text=True)
        return result.returncode, result.stdout.strip()
    except Exception as e:
        return -1, f"Checker error: Exception {e}."


def run(jail_path, in_dir_path, out_dir_path, test_name, program_bin_path, time_limit, 
        memory_limit, checker_path, model_solution_path):
    
    print("RUN!")

    test_input = os.path.join(in_dir_path, f"{test_name}.in")
    prog_output = os.path.join(out_dir_path, f"{test_name}.out")
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

            # print(command)
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

        result.time = int(time_ms)
        result.memory = int(memory_kb)
    except Exception as e:
        print(f"Failed to run sio2jail on program {program_bin_path}"
              f"\n\tcommand: `{command}` \n\tstderr:{stderr}\n")
        raise Exception("Failed to run sio2jail")

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
                                      test_name, model_solution_path)
        
        if check_code == 0:
            result.status = "ACC"
        else:
            result.status = "WA"

    return result


def run_tests(subtask, cpus, test_dir, prog):
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
        print(f"Model solution binary not found at {solution_path}. Run make first.")
        sys.exit(1)

    # checker
    checker = config.get("checker")
    checker_bin = config.get("checker_bin")

    if not checker_bin:
        checker_bin = os.path.splitext(os.path.basename(checker))[0]
    
    checker_path = os.path.join("tmp", "bin", checker_bin)

    if not os.path.exists(checker_path):
        print(f"Checker binary not found at {checker_path}. Run make first.")
        sys.exit(1)

    #limits
    time_limit = config.get("time_limit")
    if not time_limit:
        print("No time limit set!")
        sys.exit(1)

    memory_limit = config.get("memory_limit")
    if not memory_limit:
        print("No memory limit set!")
        sys.exit(1)

    # prog

    target_prog = None
    for entry in config.get("other_solutions", []):
        if entry.get("program") == prog:
            target_prog = entry
            break

    if target_prog == None:
        print(f"No such program {prog} in other solutions section of config.")
        sys.exit(1)

    prog_bin = target_prog.get("program_bin")
    if not prog_bin:
        prog_bin = os.path.splitext(os.path.basename(prog))[0]

    prog_path = os.path.join("tmp", "bin", prog_bin)

    if not os.path.exists(prog_path):
        print(f"Program '{prog}' binary not found at {prog_path}. Run make first.")
        sys.exit(1)

    # jail

    jail_path = util.get_jail_path()
    if jail_path == None or not os.path.exists(jail_path):
        print(f"Sio2jail binary not found at {jail_path}. Consider running 'setup_sio2jail'.")
        sys.exit(1)

    # in/out dir paths
    in_dir_path = os.path.join(test_dir, str(subtask), "in")
    out_dir_path = os.path.join(test_dir, str(subtask), "out")
    os.makedirs(in_dir_path, exist_ok=True)
    os.makedirs(out_dir_path, exist_ok=True)

    # preparing tasks
    tests = [t.name.removesuffix(".in") for t in Path(in_dir_path).glob("*.in")]

    tasks = [(jail_path, in_dir_path, out_dir_path, t, prog_path, time_limit, memory_limit,
              checker_path, solution_path) for t in tests]

    failed_tests = 0
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        futures = [executor.submit(run, *task) for task in tasks]
        
        for i, future in enumerate(futures, 0):
            result = future.result()
            print(result)

            if result.status != "ACC":
                failed_tests += 1
                print(f"Test {tasks[i][3]} failed with {result.status}. Subtask: {subtask} from {test_dir}")
                
                if result.status == "WA":
                    print(result.msg)

            else:
                print(f"Passed test: {tasks[i][3]}. Subtask: {subtask} from {test_dir}.")

    expected = target_prog.get("pass_subtasks")

    if subtask in expected and failed_tests == 0:
        print(f"Tests for subtask {subtask} from {test_dir} have passed.")
        print(f"This is expected behaviour.")
    elif subtask in expected and failed_tests > 0:
        print(f"Tests for subtask {subtask} from {test_dir} did not pass.")
        print(f"This is unexpected and it does not match with config."
              "Check for bugs in program or consider it's runtime.")
    elif subtask not in expected and failed_tests == 0:
        print(f"Tests for subtask {subtask} from {test_dir} have passed.")
        print(f"This is unexpected and it does not match with config."
              "Consider generating more tests or making tests for this subtask more difficult.")
    elif subtask not in expected and failed_tests > 0:
        print(f"Tests for subtask {subtask} from {test_dir} did not pass.")
        print(f"This is expected behaviour.")


def test_run():
    gen_test_path = os.path.join("tmp", "gen")
    run_tests(1, 1, gen_test_path, "b.cpp")


# def command_run_program():
#     util.ensure_workdir()
#     util.ensure_package()

#     parser = argparse.ArgumentParser(description="Runs selected program on generated and .")
    
#     parser.add_argument("-c", "--cpus", type=int, default=1, 
#                         help="Number of CPU cores to use for parallel running.")

#     parser.add_argument("-s", "--subtask", required=True,
#                         help="Subtask number or 'all'.")
    
#     parser.add_argument("-p", "--")
    
#     args = parser.parse_args()

#     yaml = YAML()
#     config_path = "config.yaml"

#     with open(config_path, 'r') as f:
#         config = yaml.load(f) or {}

#     subtask_number = config.get("subtasks")

#     if not subtask_number:
#         print("No subtask number in config. Aborting.")
#         sys.exit(1)

#     if args.subtask.lower() == "all":
#         subtasks = range(1, subtask_number + 1)
#     else:
#         try:
#             subtasks = [int(args.subtask)]
#         except ValueError:
#             print(f"Error: Subtask must be a number or 'all'. Received: {args.subtask}")
#             sys.exit(1)

#     if subtasks[-1] > subtask_number:
#         print("Cannot verify a subtask with number larger than subtask number in config. Aborting.")
#         sys.exit(1)

#     for s in subtasks:
#         verify_tests(subtask=s, cpus=args.cpus, test_dir="testcases")
#         gen_test_path = os.path.join("tmp", "gen")
#         verify_tests(subtask=s, cpus=args.cpus, test_dir=gen_test_path)
