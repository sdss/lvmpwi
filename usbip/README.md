
# Prerequisites
## Installation on RasperyPi & friends

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

* Remember the busid of the planewave mount aka Luminary Micro Inc.
    
## Client side
- Ubuntu
    apt-get install -y linux-tools-generic

- OpenSuse
    zypper install -y usbip

Temporary load the kernel module.

    sudo modprobe vhci-hcd

Add it to /etc/modules or in a file inside /etc/modprobe.d

    sudo echo 'vhci-hcd' >> /etc/modules
     
## Quick check
      [root@nicelab lvmt]# usbip list -r 192.168.70.55 
      Exportable USB devices
      ======================
       - 192.168.70.55
            1-1.4: Luminary Micro Inc. : unknown product (1cbe:0267)
                 : /sys/devices/platform/soc/20980000.usb/usb1/1-1/1-1.4
                 : Miscellaneous Device / ? / Interface Association (ef/02/01)

      [root@nicelab lvmt]# usbip attach -r 192.168.70.55 -b 1-1.4
      # quick hack - changing group is way more clean.
      [root@nicelab lvmt]# chmod 666 /dev/ttyACM*


# Setup

## Serverside:
* Copy the above github files to its designated areas

      /etc/systemd/system/usbipd.service
      /etc/udev/rules.d/20-planewave.rules

* Fix planewave busid in 20-planewave.rules found before

## Clientside:

      /etc/systemd/system/usbip_planewave.service
      /usr/local/sbin/usbip_planewave.sh

* Change IP address and planewave busid found before in /usr/local/sbin/usbip_planewave.sh:

      SERVER=
      BUSID=

 
 After installing systemd scripts /etc/systemd/system/*.service, the systemd daemon has to be restarted.
 
    sudo systemctl daemon-reload
    sudo systemctrl start usbip_planewave
    sudo systemctrl enable usbip_planewave
    sudo systemctrl status usbip_planewave

# TODO
* Currently this only works for one mount.
