# based on Sinol-make by Tomasz Grześkiewicz

import os
import subprocess
import sys
import shutil
import tarfile
import tempfile
import requests
from pathlib import Path

def check_sio2jail(path):
    try:
        sio2jail = subprocess.Popen(path + " --version", shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = sio2jail.communicate()
        out = out.decode(sys.stdout.encoding)
        if "SIO2jail" not in out:
            print(f"Couldn't recognize output of SIO2jail binary ({path}): {out}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to check SIO2jail binary ({path}): {e}")
        sys.exit(1)


def install_sio2jail(directory):
    """
    Downloads and installs sio2jail to the specified directory, creating it if it doesn't exist
    """
    path = os.path.join(directory, 'sio2jail')
    if os.path.exists(path):
        check_sio2jail(path)
        return

    print(f"'sio2jail' not found in '{path}', attempting download...")

    os.makedirs(directory, exist_ok=True)

    url = 'https://oij.edu.pl/zawodnik/srodowisko/oiejq.tar.gz'
    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f'Couldn\'t download oiejq ({url} couldn\'t connect)')
        sys.exit(1)
    if request.status_code != 200:
        print(f'Couldn\'t download oiejq ({url} returned status code: ' + str(request.status_code) + ')')
        sys.exit(1)

    # oiejq is downloaded to a temporary directory and not to the `.cache` dir,
    # as there is no guarantee that the current directory is the package directory.
    # The `.cache` dir is only used for files that are part of the package and those
    # that the package creator might want to look into.
    with tempfile.TemporaryDirectory() as tmpdir:
        oiejq_path = os.path.join(tmpdir, 'oiejq.tar.gz')
        with open(oiejq_path, 'wb') as oiejq_file:
            oiejq_file.write(request.content)

        with tarfile.open(oiejq_path) as tar:
            extract_tar(tar, tmpdir)
        shutil.copy(os.path.join(tmpdir, 'oiejq', 'sio2jail'), directory)

    check_sio2jail(path)
    print(f"'sio2jail' was successfully installed in '{path}'")


def extract_tar(tar: tarfile.TarFile, destination: str):
    if sys.version_info.major == 3 and sys.version_info.minor >= 12:
        tar.extractall(destination, filter='tar')
    else:
        tar.extractall(destination)


def setup_sio2jail():
    current_dir = Path(__file__).resolve().parent
    bin_path = os.path.join(current_dir.parent.parent, "bin")
    install_sio2jail(bin_path)