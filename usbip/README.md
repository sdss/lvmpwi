* Copy the above files to its designated areas
* Change IP address in /usr/local/sbin/usbip_planewave.sh: SERVER=

Serverside:

 /etc/systemd/system/usbipd.service
 /etc/udev/rules.d/20-planewave.rules

Clientside:

 /etc/systemd/system/usbip_planewave.service
 /usr/local/sbin/usbip_planewave.sh
 
 After installing systemd scripts /etc/systemd/system/*.service, the systemd daemon has to be restarted.
 
  sudo systemctl daemon-reload
  sudo systemctrl start usbip_planewave
  sudo systemctrl enable usbip_planewave
  sudo systemctrl status usbip_planewave