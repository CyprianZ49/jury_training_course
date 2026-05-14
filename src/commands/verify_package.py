import os
import sys
import argparse
import commands.util as util
import shutil
from ruamel.yaml import YAML


# verification process

# check if all required fields are filled
# clean all generated tests
# generate new tests in amount specified in config
# verify all inputs -> handcrafted and newly generated
# 

def command_verify_package():
    util.ensure_workdir()
    util.ensure_package()

    parser = argparse.ArgumentParser(description="Verifies package quality")

    parser.add_argument("-c", "--cpus", type=int, default=1, 
                    help="Number of CPU cores to use for parallel tasks.")
    
    args = parser.parse_args()