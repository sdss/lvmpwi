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
- Implement full pwi interface
- Container not using the host network
    
## Prerequisites

Some linux distributions do not have python >= 3.7 as the standard python3 version.

### Centos 8.X

    # as root
    yum install python38
    # as user 
    python3.8  -m pip  install --user --upgrade pip
    pip3.8 install poetry
    export PATH=~/.local/bin/:$PATH

### OpenSuSe 15.2/15.3

    # as root
    zypper ar https://download.opensuse.org/repositories/devel:/languages:/python:/Factory/openSUSE_Leap_15.2/ devel_python
    zypper install python39
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
    poetry run container_stop
    # run container with rdp
    poetry run container_start --without-ui
    # linux ( should also work under windows with MS rdesktop)
    xfreerdp  +glyph-cache /relax-order-checks /v:YOUR_HOST
    
### Run tests 

    # run tests
    poetry run pytest
    # ... include slow tests with enabled log to stdout
    poetry run pytest -p no:logging -s -v --runslow
    
    
### Publish
    # publish to pypi
    poetry publish --username=USER --password=PASS
    # build rpm package
    poetry run python setup.py bdist_rpm
    # build deb package - needs python3-stdeb
    poetry run python setup.py --command-packages=stdeb.command bdist_deb
