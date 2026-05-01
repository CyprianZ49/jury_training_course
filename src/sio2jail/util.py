import glob, importlib, os, sys, requests, yaml
import math
import platform
import tarfile
import hashlib
import multiprocessing
import resource
from typing import Union
from packaging.version import parse as parse_version

def is_linux():
    """
    Function to check if the program is running on Linux (including WSL).
    """
    return sys.platform == "linux"

def extract_tar(tar: tarfile.TarFile, destination: str):
    if sys.version_info.major == 3 and sys.version_info.minor >= 12:
        tar.extractall(destination, filter='tar')
    else:
        tar.extractall(destination)

def color_red(text): return "\033[91m{}\033[00m".format(text)
def color_green(text): return "\033[92m{}\033[00m".format(text)
def color_yellow(text): return "\033[93m{}\033[00m".format(text)
def color_gray(text): return "\033[90m{}\033[00m".format(text)
def bold(text): return "\033[01m{}\033[00m".format(text)

def info(text):
    return bold(color_green(text))
def warning(text):
    return bold(color_yellow(text))
def error(text):
    return bold(color_red(text))

###
def exit_with_error(text, func=None):
    print(error(text))
    try:
        func()
    except TypeError:
        pass
    exit(1)


def has_sanitizer_error(output, exit_code):
    return ('ELF_ET_DYN_BASE' in output or 'ASan' in output) and exit_code != 0
