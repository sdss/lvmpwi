#!/bin/bash

ENDLESS=true
LANG=C
SERVER='192.168.80.55'
BUSID='4-1'

trap_exit() {
    ENDLESS=false
    for PORT in $(/usr/sbin/usbip port | /usr/bin/grep ^Port | /usr/bin/cut -d':' -f1 | /usr/bin/awk '{print$2}'); do
        /usr/sbin/usbip detach -p $PORT
    done
    exit 0
}

trap trap_exit SIGINT
trap trap_exit SIGTERM
trap trap_exit SIGKILL

while $ENDLESS; do
    if ! /usr/sbin/usbip port | /usr/bin/grep "usbip:.*${SERVER}.*${BUSID}$" &> /dev/null; then
        /usr/sbin/usbip attach -r ${SERVER} -b ${BUSID}
    fi
    sleep 5
done

trap_exit
