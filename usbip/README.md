
# Prerequisites
## Installation RasperyPi & friends

    sudo apt-get install usbip
    sudo modprobe usbip_host
    sudo echo 'usbip_host' >> /etc/modules

    sudo modprobe usbip_host

    
## Find the usb id of the planewave mount

    root@raspberrypi:/home/pi# usbip list -l
     - busid 1-1.1 (0424:ec00)
       Standard Microsystems Corp. : SMSC9512/9514 Fast Ethernet Adapter (0424:ec00)

     - busid 1-1.4 (1cbe:0267)
       Luminary Micro Inc. : unknown product (1cbe:0267)

       
# Setup

## Serverside:
* Copy the above github files to its designated areas

      /etc/systemd/system/usbipd.service
      /etc/udev/rules.d/20-planewave.rules

* Fix usb id in 20-planewave.rules detected from above.

## Clientside:

      /etc/systemd/system/usbip_planewave.service
      /usr/local/sbin/usbip_planewave.sh

* Change IP address and USB ID from above in /usr/local/sbin/usbip_planewave.sh:

      SERVER=
      BUSID=

 
 After installing systemd scripts /etc/systemd/system/*.service, the systemd daemon has to be restarted.
 
  sudo systemctl daemon-reload
  sudo systemctrl start usbip_planewave
  sudo systemctrl enable usbip_planewave
  sudo systemctrl status usbip_planewave

# TODO
* Currently this only works for one mount.
