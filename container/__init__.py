# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-06-15
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import subprocess
import sys
import os
import time
import pexpect
import shlex
import click
from pathlib import PosixPath

#from podman import PodmanClient
#uri = "unix:///run/user/1000/podman/podman.sock"
#podman container exists ubuntu_lvmt_pwi # 0=True, 1=False


container_bin = 'podman'
lvmt_root = os.environ["PWD"]
lvmt_image_name = 'ubuntu_lvmt_pwi'

default_pwi = 'lvm_pwi'


def isRunning(name: str = default_pwi):
    command = subprocess.run(shlex.split(f"{container_bin} container exists {name}"))
    return not command.returncode # True if running
  
@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvmt_root:str, use_cache: bool):
    pwi_dockerfile = f"{lvmt_root}/container"
    lvmt_image_fullbuild = "" if use_cache else " --no-cache"
    print(f"{container_bin} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {pwi_dockerfile}")
    build = f"{container_bin} build --tag {lvmt_image_name}{lvmt_image_fullbuild} --rm {pwi_dockerfile}"
    command = subprocess.run(shlex.split(build))


@click.command()   
@click.option("--lvmt_root", default=lvmt_root, type=str)
@click.option("--name", "-n", default=default_pwi, type=str)
def start(name: str, lvmt_root:str):
    lvmt_image = f"localhost/{lvmt_image_name}"

    run_base = f"--rm -t --name {name} --network=host -v /dev:/dev:rslave"
    system_xauthority=PosixPath('~/.Xauthority').expanduser()
    run_base +=  f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host"
    if os.path.exists('/dev/dri'):
        run_base +=  ' --device /dev/dri'
    run_pwi = f"-v {lvmt_root}:/root/lvmt:Z -e PWI_NAME={name}"
    run = f"{container_bin} run {run_base} {run_pwi} {lvmt_image}"
    print(run)
    child = pexpect.spawn(run)
    child.expect('BSC loaded')
    assert isRunning(name) == True
    

@click.command()   
@click.option("--name", "-n", default=default_pwi, type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))

