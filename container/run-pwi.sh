#!/usr/bin/bash

LVM_ROOT=${HOME}
LVM_ACTOR="lvmpwi"

LVM_ACTOR_PATH=$(ls -1 -d ${LVM_ROOT}/lvm/${LVM_ACTOR} ${LVM_ROOT}/${LVM_ACTOR} 2> /dev/null)

export MESA_GL_VERSION_OVERRIDE=4.5

start_actor() {

    if [ $LVM_RMQ_HOST ]; then
        LVM_ACTOR_ARGS="--rmq_url amqp://guest:guest@${LVM_RMQ_HOST}:5672/"
    fi

    LVM_ACTOR_CONFIG_ABS="${LVM_ACTOR_PATH}/python/${LVM_ACTOR}/etc/${LVM_ACTOR_CONFIG:-$PWI_NAME}.yml"

    sed "s/lvm.pwi/$PWI_NAME/" < ${LVM_ACTOR_PATH}/python/${LVM_ACTOR}/etc/lvm.pwi.yml > ${LVM_ACTOR_CONFIG_ABS}

    while true
    do
       sleep 2
       /root/.local/bin/lvmpwi --config ${LVM_ACTOR_CONFIG_ABS} ${LVM_ACTOR_ARGS} start --debug
    done
}

setup_pwi4() {

    LVM_CONFIG_PATH=${LVM_ACTOR_PATH}/config/planewave/$PWI_NAME

    mkdir -p ~/PlaneWave\ Instruments/PWI4/

    rm -rf ~/PlaneWave\ Instruments/PWI4/Mount
    mkdir -p ${LVM_CONFIG_PATH}/Mount/
    (cd ~/PlaneWave\ Instruments/PWI4/ && ln -s ${LVM_CONFIG_PATH}/Mount/ )

    rm -rf ~/PlaneWave\ Instruments/PWI4/Settings
    mkdir -p ${LVM_CONFIG_PATH}/Settings/
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

    cat > ~/.vnc/xstartup<< EOF
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
startxfce4
EOF

    chmod +x ~/.vnc/xstartup
    /usr/bin/vncserver -fg -depth 24 -geometry $PWI_GEOM -port 5900 -SecurityTypes None --I-KNOW-THIS-IS-INSECURE -localhost no :0 &

    export DISPLAY=:0

    unset SESSION_MANAGER
    unset DBUS_SESSION_BUS_ADDRESS
    startxfce4 &

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
