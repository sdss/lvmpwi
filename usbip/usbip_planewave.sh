#!/bin/bash

ENDLESS=true
LANG=C
SERVER='192.168.80.55'
BUSID='4-1'
TTYDEV=/dev/ttyACM0
USBIP=$(which usbip)

trap_exit() {
    ENDLESS=false
    for PORT in $($USBIP port | /usr/bin/grep ^Port | /usr/bin/cut -d':' -f1 | /usr/bin/awk '{print$2}'); do
        $USBIP detach -p $PORT
    done
    exit 0
}

trap trap_exit SIGINT
trap trap_exit SIGTERM
trap trap_exit SIGKILL

while $ENDLESS; do
  if [ ! -c "$TTYDEV" ]; then
    if ! $USBIP port | /usr/bin/grep "usbip:.*${SERVER}.*${BUSID}$" &> /dev/null; then
      $USBIP attach -r ${SERVER} -b ${BUSID} &> /dev/null
      rc=$?
      if test $rc -eq 0; then
          sleep 0.7
          /usr/bin/chmod 666 /dev/ttyACM[01];
      fi
    fi
  fi
  sleep 1
done

trap_exit
