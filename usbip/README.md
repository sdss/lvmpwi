
# Prerequisites
## Installation RasperyPi & friends

    sudo apt-get install usbip
    sudo modprobe usbip_host
    sudo echo 'usbip_host' >> /etc/modules

## Find the usb id of the planewave mount

    modprobe usbip_host

    
    root@raspberrypi:/home/pi# usbip list -l
     - busid 1-1.1 (0424:ec00)
       Standard Microsystems Corp. : SMSC9512/9514 Fast Ethernet Adapter (0424:ec00)

     - busid 1-1.4 (1cbe:0267)
       Luminary Micro Inc. : unknown product (1cbe:0267)


       
# Setup
* Copy the above files to its designated areas
* Change IP address in /usr/local/sbin/usbip_planewave.sh: SERVER=

## Serverside:

 /etc/systemd/system/usbipd.service
 /etc/udev/rules.d/20-planewave.rules

## Clientside:

 /etc/systemd/system/usbip_planewave.service
 /usr/local/sbin/usbip_planewave.sh
 
 After installing systemd scripts /etc/systemd/system/*.service, the systemd daemon has to be restarted.
 
  sudo systemctl daemon-reload
  sudo systemctrl start usbip_planewave
  sudo systemctrl enable usbip_planewave
  sudo systemctrl status usbip_planewave
