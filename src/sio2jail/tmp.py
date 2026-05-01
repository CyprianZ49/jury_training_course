import os
import subprocess
import sys
import shutil
import tarfile
import tempfile
import requests
from pathlib import Path

import util


def sio2jail_supported():
    return util.is_linux()


def check_sio2jail(path):
    try:
        sio2jail = subprocess.Popen(path + " --version", shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = sio2jail.communicate()
        out = out.decode(sys.stdout.encoding)
        # TODO: maybe parse and check version
        if "SIO2jail" not in out:
            util.exit_with_error(f"Couldn't recognize output of SIO2jail binary ({path}): {out}")
    except Exception as e:
        util.exit_with_error(f"Failed to check SIO2jail binary ({path}): {e}")


def install_sio2jail(directory):
    """
    Downloads and installs sio2jail to the specified directory, creating it if it doesn't exist
    """
    path = os.path.join(directory, 'sio2jail')
    if os.path.exists(path):
        check_sio2jail(path)
        return

    print(f'`sio2jail` not found in `{path}`, attempting download...')

    os.makedirs(directory, exist_ok=True)

    url = 'https://oij.edu.pl/zawodnik/srodowisko/oiejq.tar.gz'
    try:
        request = requests.get(url)
    except requests.exceptions.ConnectionError:
        util.exit_with_error('Couldn\'t download oiejq ({url} couldn\'t connect)')
    if request.status_code != 200:
        util.exit_with_error('Couldn\'t download oiejq ({url} returned status code: ' + str(request.status_code) + ')')

    # oiejq is downloaded to a temporary directory and not to the `.cache` dir,
    # as there is no guarantee that the current directory is the package directory.
    # The `.cache` dir is only used for files that are part of the package and those
    # that the package creator might want to look into.
    with tempfile.TemporaryDirectory() as tmpdir:
        oiejq_path = os.path.join(tmpdir, 'oiejq.tar.gz')
        with open(oiejq_path, 'wb') as oiejq_file:
            oiejq_file.write(request.content)

        with tarfile.open(oiejq_path) as tar:
            util.extract_tar(tar, tmpdir)
        shutil.copy(os.path.join(tmpdir, 'oiejq', 'sio2jail'), directory)

    check_sio2jail(path)
    print(f'`sio2jail` was successfully installed in `{path}`')



current_dir = Path(__file__).resolve().parent
install_sio2jail(current_dir.parent.parent / "bin")