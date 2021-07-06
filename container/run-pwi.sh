#!/usr/bin/bash -l

LVMT_PATH=/root/lvmt
LVMT_CONFIG_PATH=$LVMT_PATH/config/lvm/$PWI_NAME

PATH=$LVMT_PATH/scripts:$PATH
PYTHONPATH=$LVMT_PATH/python/:$PYTHONPATH

PWI_VERSION=4.0.9beta21


download_pwi4() {
    mkdir -p $LVMT_PATH/3rdparty/
    test -e $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz || wget http://planewave.com/files/software/PWI4/pwi-$PWI_VERSION.tar.gz -O $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz
    echo unpacking ...
    (cd $LVMT_PATH/ && tar xzf $LVMT_PATH/3rdparty/pwi-$PWI_VERSION.tar.gz)
}

setup_pwi4() {
    mkdir -p ~/PlaneWave\ Instruments/PWI4/
    rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
    (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s $LVMT_CONFIG_PATH/PWI4/Settings/ )
}

start_pwi4() {
    cd ~/lvmt/pwi-$PWI_VERSION/
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
    python3 setup.py install
    python3 $LVMT_PATH/python/lvmpwi/__main__.py -c $LVMT_PATH/python/lvmpwi/etc/lvmpwi.yml start 
}

if [ ! -d $LVMT_PATH/pwi-$PWI_VERSION ]; then
    download_pwi4
fi

setup_pwi4

if [ -z $DISPLAY ]; then
    use_xrdp
    max_pwi4 &
fi

start_actor & 

start_pwi4


