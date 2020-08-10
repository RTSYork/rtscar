# Monitoring power and battery voltage

The INA260 power monitor can be used to monitor the instantaneous power draw of the Jetson and accessories, as well as the voltage of the smaller battery.
This voltage should be monitored periodically to ensure the battery is not over discharged, as there is no electrical protection for this.


## INA260 Python scripts

A number of scripts are provided to show basic reading of data from the power monitor board.

### Prerequisites

```
sudo apt install python3-smbus
```


## Battery monitoring service

The service can be used to run a Python script that monitors the car's battery voltage via the INA260, and will warn users and automatically shutdown the Jetson when the battery gets low.
Note that this only monitors the Jetson/lidar battery, and not the VESC battery.

**This software service will not completely cut off battery power, so the physical power switch also needs to be used after the Jetson has finished shutting down.**

### Install

Run `service-install.sh`, or install manually with:

```
sudo apt install python3-smbus
sudo cp battery-monitor.py /usr/bin
sudo cp battery-monitor.service /etc/systemd/system
sudo systemctl enable battery-monitor.service
sudo systemctl start battery-monitor.service
```
