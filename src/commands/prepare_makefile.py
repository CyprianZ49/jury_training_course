import os
import sys
import argparse
from ruamel.yaml import YAML
import commands.util as util

def prepare_makefile(compiler):
    yaml = YAML()
    config_path = "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.load(f) or {}
    
    standard_programs = [
        "checker",
        "model_solution",
        "generator",
        "input_verifier"
    ]

    to_compile = []
    for p in standard_programs:
        prog = config.get(p)
        if prog:
            bin = config.get(p + "_bin")
            if not bin:
                bin = os.path.splitext(os.path.basename(prog))[0]
            if not prog.endswith(('.cpp', '.cc', '.cxx')):
                print(f"Default makefile only supports c++ files. Skipping {prog}.")
                continue

            to_compile.append((prog, bin))

    for entry in config.get("other_solutions", []):
        prog = entry.get("program")
        if prog:
            bin = entry.get("program_bin")
            if not bin:
                bin = os.path.splitext(os.path.basename(prog))[0]
            
            if not prog.endswith(('.cpp', '.cc', '.cxx')):
                print(f"Default makefile only supports c++ files. Skipping {prog}.")
                continue
                
            to_compile.append((prog, bin))

    bin_dir = os.path.join("tmp", "bin")

    lines = [
        f"CXX = {compiler}",
        f"BIN_DIR = {bin_dir}",
        "DEFAULT_FLAGS = -O2 -Wall -std=c++17",
        ""
    ]

    for prog, _ in to_compile:
        name = os.path.splitext(os.path.basename(prog))[0].upper()
        lines.append(f"{name}_FLAGS = $(DEFAULT_FLAGS)")

    target_list = " ".join([f"$(BIN_DIR)/{bin}" for _, bin in to_compile])

    lines.extend(
        [
            "",
            f"TARGETS = {target_list}",
            "",
            "all: $(BIN_DIR) $(TARGETS)",
            "",
            "$(BIN_DIR):",
            "\tmkdir -p $(BIN_DIR)",
            "",
        ]
    )

    for prog, bin in to_compile:
        name = os.path.splitext(os.path.basename(prog))[0].upper()
        lines.append(f"$(BIN_DIR)/{bin}: {prog}")
        lines.append(f"\t$(CXX) $({name}_FLAGS) {prog} -o $(BIN_DIR)/{bin}")
        lines.append("")

    lines.append("clean:")
    lines.append("\trm -rf $(BIN_DIR)/*")

    with open("Makefile", 'w') as f:
        f.write("\n".join(lines))
    
    print(f"Prepared Makefile based on config")


def command_prepare_makefile():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Prepares a default makefile for a config.")

    parser.add_argument("compiler", help="c++ compiler")

    args = parser.parse_args()

    prepare_makefile(args.compiler)