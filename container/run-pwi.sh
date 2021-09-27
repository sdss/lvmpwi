#!/usr/bin/bash

LVMT_PATH=/root/lvmt
LVMT_CONFIG_PATH=$LVMT_PATH/config/planewave/$PWI_NAME

setup_pwi4() {
    mkdir -p $LVMT_CONFIG_PATH/Settings/
    mkdir -p ~/PlaneWave\ Instruments/PWI4/
    rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
    (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s $LVMT_CONFIG_PATH/Settings/ )
    if [ ! -f  $LVMT_CONFIG_PATH/Settings/PWI4.cfg]; then
        cp $LVMT_CONFIG_PATH/../pwi/Settings/PWI4.cfg $LVMT_CONFIG_PATH/Settings/PWI4.cfg
    fi
    if [ $PWI_SIMULATOR ]; then 
        sed  -i "s/elmo/simulator/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
    else
        sed  -i "s/simulator/elmo/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
    fi

    mkdir -p $LVMT_CONFIG_PATH/Mount\ Tuning/
    rm -rf ~/PlaneWave\ Instruments/Mount\ Tuning
    (cd ~/PlaneWave\ Instruments/ && ln -s $LVMT_CONFIG_PATH/Mount\ Tuning/ )
    mkdir -p $LVMT_PATH/data
    (cd $PWI_PATH && ln -sf $LVMT_PATH/data data )

    
}

start_pwi4() {
    cd $PWI_PATH
    ./run-pwi4
}

max_pwi4() {
    while [[ -z $(wmctrl -l) ]]; do sleep 0.1; done
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

use_vnc() {
    echo -e "${PASSWD:-lvmt}\n${PASSWD:-lvmt}" | passwd
    cp $LVMT_PATH/container/xrdp.ini /etc/xrdp/ 
    Xvnc :0 -geometry 1100x800 &
    export DISPLAY=:0
    fluxbox &
}


start_actor() {
    # lets give the pwi sw some time to startup
    if [ ! -f $LVMT_PATH/python/lvmpwi/etc/$PWI_NAME.yml ]; then
       cat $LVMT_PATH/python/lvmpwi/etc/lvm.pwi.yml | sed "s/lvm.pwi/$PWI_NAME/; s/host: localhost/host: $LVMT_RMQ/" \
            > $LVMT_PATH/python/lvmpwi/etc/$PWI_NAME.yml
       sed  -i "s/elmo/simulator/" $LVMT_CONFIG_PATH/Settings/PWI4.cfg
    fi
    sleep 1
    if [ $PWI_DEBUG ]; then 
        PYTHONPATH=$LVMT_PATH/python/:$PYTHONPATH
    fi
    
    echo $PYTHONPATH
    
    python3 $LVMT_PATH/python/lvmpwi/__main__.py -c $LVMT_PATH/python/lvmpwi/etc/$PWI_NAME.yml start 
}

setup_pwi4

if [ -z $DISPLAY ]; then
#    use_xrdp
    use_vnc
    max_pwi4 &
fi

start_actor & 

start_pwi4


