#!/usr/bin/bash

PYTHON=/usr/bin/python3

LVM_ROOT=${HOME}
#LVM_PATH=/root/lvm

LVM_ACTOR="lvmpwi"

LVM_ACTOR_PATH=$(ls -1 -d ${LVM_ROOT}/lvm/${LVM_ACTOR} ${LVM_ROOT}/${LVM_ACTOR} 2> /dev/null)
export PYTHONPATH=$(ls -1 -d ${LVM_ROOT}/lvm/*/python ${LVM_ROOT}/${LVM_ACTOR}/python 2>/dev/null | tr "\n" ":")

echo $(${PYTHON} -c "import ${LVM_ACTOR} as _; print(_.__path__[0])")


start_actor() {

    if [ $LVM_RMQ_HOST ]; then
        # echo $LVM_RMQ_HOST
        LVM_ACTOR_ARGS="--rmq_url amqp://guest:guest@${LVM_RMQ_HOST}:5672/"
    fi

    LVM_ACTOR_CONFIG_ABS="${LVM_ACTOR_PATH}/python/${LVM_ACTOR}/etc/${LVM_ACTOR_CONFIG:-$PWI_NAME}.yml"
    # echo ${LVM_ACTOR_CONFIG_ABS}

    sed "s/lvm.pwi/$PWI_NAME/" < ${LVM_ACTOR_PATH}/python/${LVM_ACTOR}/etc/lvm.pwi.yml > ${LVM_ACTOR_CONFIG_ABS}
  
    while true 
    do
       sleep 2
       ${PYTHON} ${LVM_ACTOR_PATH}/python/${LVM_ACTOR}/__main__.py --config ${LVM_ACTOR_CONFIG_ABS} ${LVM_ACTOR_ARGS} start --debug
    done
}

setup_pwi4() {

    LVM_CONFIG_PATH=${LVM_ACTOR_PATH}/config/planewave/$PWI_NAME

    mkdir -p ${LVM_CONFIG_PATH}/Settings/
    mkdir -p ~/PlaneWave\ Instruments/PWI4/
    rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
    (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s ${LVM_CONFIG_PATH}/Settings/ )
    if [ ! -f  ${LVM_CONFIG_PATH}/Settings/PWI4.cfg ]; then
        cp ${LVM_CONFIG_PATH}/../pwi/Settings/PWI4.cfg ${LVM_CONFIG_PATH}/Settings/PWI4.cfg
    fi
    if [ $PWI_SIMULATOR ]; then 
        sed  -i "s/elmo/simulator/" ${LVM_CONFIG_PATH}/Settings/PWI4.cfg
    else
        sed  -i "s/simulator/elmo/" ${LVM_CONFIG_PATH}/Settings/PWI4.cfg
    fi

    mkdir -p ${LVM_CONFIG_PATH}/Mount\ Tuning/
    rm -rf ~/PlaneWave\ Instruments/Mount\ Tuning
    (cd ~/PlaneWave\ Instruments/ && ln -s ${LVM_CONFIG_PATH}/Mount\ Tuning/ )
    mkdir -p ${LVM_ACTOR_PATH}/data
    (cd ${PWI_PATH} && ln -sf ${LVM_ACTOR_PATH}/data data )
}

start_pwi4() {
    cd ${PWI_PATH}
    while true 
    do
       ./run-pwi4
       sleep 2
    done

}

max_pwi4() {
    while [[ -z $(wmctrl -l) ]]; do sleep 0.1; done
    wmctrl -r ':ACTIVE:' -b toggle,fullscreen
}

use_vnc() {
#    echo -e "${PASSWD:-lvmt}\n${PASSWD:-lvmt}" | passwd
#    cp ${LVM_ACTOR_PATH}/container/xrdp.ini /etc/xrdp/ 
    Xvnc :0 -geometry $PWI_GEOM &
    export DISPLAY=:0
    fluxbox &
    (cd /usr/share/novnc/ && ~/novnc_server &)
}

setup_pwi4

if [ -z $DISPLAY ]; then
    use_vnc
#    max_pwi4 &
fi

start_actor & 

start_pwi4 & 

trap : TERM INT; sleep infinity & wait
