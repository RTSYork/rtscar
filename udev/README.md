# udev Rules

In order to access the various USB-connected devices on the car reliably and easily, each can be mapped to a specific endpoint in `/dev` using custom udev rules.

After installing the rules file, the following devices will be symlinked to `/dev/car`:

- `/dev/car/camera` - Logitech BRIO (UVC device)
- `/dev/car/vesc` - VESC (TTY device)
- `/dev/car/razor` - SparkFun Razor IMU (TTY device)


## Installation

Run `rules-install.sh`, or copy the included rules file to `/etc/udev/rules.d/`.
Reboot for the new rules to take effect.
