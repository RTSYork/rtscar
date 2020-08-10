#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "Please re-run this install script as root."
	exit
fi

apt install python3-smbus
cp -v battery-monitor.py /usr/bin
cp -v battery-monitor.service /etc/systemd/system
systemctl enable battery-monitor.service
systemctl start battery-monitor.service
