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
import socket
from pathlib import PosixPath

container_bin = 'podman'
lvm_root = os.environ["PWD"]
lvm_image_source_local = "localhost"
lvm_image_source_remote = "ghcr.io/sdss"
lvm_image_name = 'lvmpwi'
lvm_rmq = socket.gethostname()

default_pwi = 'lvm.pwi'

# podman run --rm -ti --name pwi --network=host -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z --device /dev/dri -v ~/.Xauthority:/root/.Xauthority:Z  -e PWI_NAME=pwi localhost/lvmpwi

# podman run --rm -ti --name pwi -v /home/briegel/workspace/lvmt/lvmpwi:/root/lvmt:Z -e PWI_NAME=pwi localhost/lvmpwi

def isRunning(name: str = default_pwi):
    command = subprocess.run(shlex.split(f"{container_bin} container exists {name}"))
    return not command.returncode # True if running

def getXauthority():
    for xa in [f"/run/user/{os.getuid()}/gdm/Xauthority", '~/.Xauthority']:
        xa=PosixPath(xa).expanduser()
        if xa.exists():
            return xa
    return None

def next_free_port( port=5900, max_port=5909 ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    print('no free ports')
    return None


@click.command()   
@click.option("--lvm_root", default=lvm_root, type=str)
@click.option("--use-cache/--no-cache", default=True)
def build(lvm_root:str, use_cache: bool):
    pwi_dockerfile = f"{lvm_root}/container"
    lvm_image_fullbuild = "" if use_cache else " --no-cache"
    build = f"{container_bin} build --tag {lvm_image_name}{lvm_image_fullbuild} --rm --file {pwi_dockerfile}/Dockerfile ."
    print(build)
    command = subprocess.run(shlex.split(build))


@click.command()   
@click.option("--name", "-n", default=default_pwi, type=str)
@click.option("--debug", "-d", default=False, type=bool)
def autotuner(name: str, debug:bool):
    run_autotuner = f"-v {lvm_root}:/root/lvmt:Z -e PWI_NAME={name}"
    run = f"{container_bin} exec -ti {name} /opt/autotuner-1.0.3beta1/run-autotuner_nogl"
    command = subprocess.run(shlex.split(f"{run}"))


@click.command()   
@click.option("--lvm_root", default=lvm_root, type=str)
@click.option("--with-ui/--without-ui", default=True)
@click.option("--rmq_host", default=lvm_rmq, type=str)
@click.option("--name", "-n", default=default_pwi, type=str)
@click.option("--debug/--no-debug", "-d", default=False)
@click.option("--simulator/--elmo", default=False)
@click.option("--kill/--no-kill", default=False)
@click.option("--geom", "-g", default='800x600', type=str)
def start(name: str, with_ui: bool, lvm_root:str, rmq_host:str, debug:bool, simulator:bool, kill:bool, geom:str):
    if not subprocess.run(shlex.split(f"{container_bin} image exists {lvm_image_source_local}/{lvm_image_name}")).returncode:
       lvm_image = f"{lvm_image_source_local}/{lvm_image_name}"
    else:
       if subprocess.run(shlex.split(f"{container_bin} image exists {lvm_image_source_remote}/{lvm_image_name}")).returncode:
           subprocess.run(shlex.split(f"{container_bin} pull {lvm_image_source_remote}/{lvm_image_name}:latest"))
       lvm_image = f"{lvm_image_source_remote}/{lvm_image_name}"

    vnc_port=None

    if kill:
        subprocess.run(shlex.split(f"{container_bin} kill {name}"))
        
    run_base = f"--rm -d --name {name}"
    system_xauthority = getXauthority()
    
    run_base += f" -e LVM_RMQ_HOST={rmq_host}"
    
    if with_ui and os.environ.get("DISPLAY") and system_xauthority:
        run_base +=  f" -e DISPLAY -v {system_xauthority}:/root/.Xauthority:Z --ipc=host  --network=host"
        if os.path.exists('/dev/dri'):
            run_base += ' --device /dev/dri'
    else:
        vnc_port = next_free_port()
        run_base +=  f" -p {vnc_port}:5900 -e PWI_GEOM={geom}"
#        run_base +=  f" -p 3389"
        
    if debug:
        run_base +=  f" -p 8220 -e LVM_DEBUG=true"

    if simulator:
        run_base +=  f" -e PWI_SIMULATOR=true"

    ## Ugly hack - fixme with udev rule
    #if os.path.exists('/dev/ttyACM0'):
    #    run_base +=  ' --device /dev/ttyACM0  --device /dev/ttyACM1'
    
    # doesnt work on opensuse
    run_base += " -v /dev:/dev:rslave"
    
    system_xauthority=PosixPath('~/.Xauthority').expanduser()
    run_pwi = f"-v {lvm_root}:/root/{os.path.basename(lvm_root)}:Z -e PWI_NAME={name}"
    run = f"{container_bin} run {run_base} {run_pwi} {lvm_image}"
    print(run)
    #child = pexpect.spawn(run)
    #child.expect('BSC loaded')
    #assert isRunning(name) == True
    command = subprocess.run(shlex.split(f"{run}"))
    logs = subprocess.run(shlex.split(f"{container_bin} logs -f {name}"))
    if vnc_port and os.environ.get("DISPLAY") and system_xauthority:
        vncclient = subprocess.run(shlex.split(f"vncviewer :{vnc_port - 5900}"))
    
    print("done")

@click.command()   
@click.option("--name", "-n", default=default_pwi, type=str)
def stop(name: str):
    command = subprocess.run(shlex.split(f"{container_bin} kill {name}"))


