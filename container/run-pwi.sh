#!/usr/bin/bash

LVMT_PATH=/root/lvmt
LVMT_CONFIG_PATH=$LVMT_PATH/config/lvm/$PWI_NAME

setup_pwi4() {
    mkdir -p ~/PlaneWave\ Instruments/PWI4/
    rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
    (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s $LVMT_CONFIG_PATH/PWI4/Settings/ )
    (cd ~/PlaneWave\ Instruments/ && ln -s $LVMT_CONFIG_PATH/PWI4/Mount\ Tuning/ )
    mkdir -p $LVMT_PATH/data
    (cd $PWI_PATH && ln -sf $LVMT_PATH/data/ data/ )
}

start_pwi4() {
    cd $PWI_PATH
    ./run-pwi4
}

max_pwi4() {
    while [-z $(wmctrl -l)]; do sleep 0.1; done
    wmctrl -r ':ACTIVE:' -b toggle,fullscreen
}

use_xrdp() {
    echo -e "${PASSWD:-lvmt}\n${PASSWD:-lvmt}" | passwd
    cp $LVMT_PATH/container/xrdp.ini /etc/xrdp/ 
    Xvnc :2 -geometry 1200x1000 &
    /usr/sbin/xrdp-sesman
    /usr/sbin/xrdp
    export DISPLAY=:2 
    fluxbox &
}

start_actor() {
    # lets give the pwi sw some time to startup
    sleep 1
    python3 $LVMT_PATH/python/lvmpwi/__main__.py -c $LVMT_PATH/python/lvmpwi/etc/lvmpwi.yml start 
}

setup_pwi4

if [ -z $DISPLAY ]; then
    use_xrdp
    max_pwi4 &
fi

start_actor & 

start_pwi4


