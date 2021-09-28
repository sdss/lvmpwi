# lvmpwi

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmpwi/badge/?version=latest)](https://sdss-lvmpwi.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmpwi)](https://travis-ci.org/sdss/lvmpwi)
[![codecov](https://codecov.io/gh/sdss/lvmpwi/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmpwi)

Lvm Planewave PWI Clu Wrapper

## Features

- CLU based wrapper for Planewave PWI.
- Uses a container for deployment and testing. 
- Uses podman¹ for building the container.

¹ Setting an alias to use docker might work.

    alias podman="sudo docker"

## Todo
- Container not using the host network
    
## Prerequisites

Some linux distributions do not have python >= 3.7 as the standard python3 version.

### Centos 8.X

    # as root
    yum install python38-devel
    # as user 
    python3.8  -m pip  install --user --upgrade pip
    pip3.8 install poetry
    export PATH=~/.local/bin/:$PATH

### OpenSuSe 15.2/15.3

    # as root
    zypper ar https://download.opensuse.org/repositories/devel:/languages:/python:/Factory/openSUSE_Leap_15.2/ devel_python
    zypper install python39-devel
    # as user 
    python3.9  -m pip  install --user --upgrade pip
    pip3.9 install poetry
    export PATH=~/.local/bin/:$PATH

## Quick start

### Download
    git clone https://github.com/sdss/lvmpwi.git
    cd lvmpwi      

### Build
    # update local py env
    poetry update
    poetry install
    
    # build sdist & wheel (optional)
    poetry build
    
    # build pwi container
    poetry run container_build
    # rebuild pwi container from scratch
    poetry run container_build --no-cache
        
### Run container

    poetry run container_start
    
    # with pwi4 port 8220 exposed
    poetry run container_start --debug
    poetry run container_stop
    
    # run container with vnc - uses a free port between 5900 - 5909
    poetry run container_start --without-ui
    
    # start multiple pwi container with simulation screen size for vnc sessions
    poetry run container_start --simulator --name=lvm.sci.pwi&
    poetry run container_start --simulator --geom=800x600 --without-ui --name=lvm.skye.pwi&
    poetry run container_start --simulator --geom=800x600 --without-ui --name=lvm.skyw.pwi&
    poetry run container_start --simulator --geom=800x600 --without-ui --name=lvm.spec.pwi&
    
    # run autotuner from container
    # Note: the standard autotuner needs opengl, which is not available with tigervnc/tightvnc, only with turbovnc and native display.
    poetry run container_autotuner
    
### Run tests 

    # run tests
    poetry run pytest
    # ... include slow tests with enabled log to stdout
    poetry run pytest -p no:logging -s -v --runslow
    
### Run native pwi client interface


    # run python with path to native pwi interface¹
    export PYTHONPATH=python/lvmpwi/pwi/:$PYTHONPATH
    poetry run python
    
    # see also lvmpwi/python/lvmpwi/pwi/pwi4_client_demo.py²
    # the documentation of the api is inside the code.
    import time
    from pwi4_client import PWI4
    pwi4 = PWI4()
    s = pwi4.status()
    if not s.mount.is_connected:
        print ("Connecting to mount...")
        s = pwi4.mount_connect()
        print ("Mount connected:", s.mount.is_connected)
        
¹ [pwi4_client.py](https://github.com/sdss/lvmpwi/blob/main/python/lvmpwi/pwi/pwi4_client.py) 
² [pwi4_client_demo.py](https://github.com/sdss/lvmpwi/blob/main/python/lvmpwi/pwi/pwi4_client_demo.py) 
    
### Publish
    # publish to pypi
    poetry publish --username=USER --password=PASS
    # build rpm package
    poetry run python setup.py bdist_rpm
    # build deb package - needs python3-stdeb
    poetry run python setup.py --command-packages=stdeb.command bdist_deb
