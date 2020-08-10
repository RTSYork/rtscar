#!/usr/bin/env python3
"""Script to monitor and display car battery state."""
from time import sleep
from datetime import datetime
from smbus import SMBus
import argparse
import subprocess


MIN_VOLTAGE = 3.3 * 3
MAX_VOLTAGE = 4.2 * 3
BAT_LOW_VOLTAGE = 3.6 * 3
BAT_VLOW_VOLTAGE = 3.5 * 3
BAT_CRIT_VOLTAGE = 3.35 * 3
VOLTAGE_RANGE = MAX_VOLTAGE - MIN_VOLTAGE
INA260_ADDR = 0x45
I2C_BUS = 0

REG_CONFIG       = 0x00 # CONFIGURATION REGISTER (R/W)
REG_CURRENT      = 0x01 # CURRENT REGISTER (R)
REG_BUSVOLTAGE   = 0x02 # BUS VOLTAGE REGISTER (R)
REG_POWER        = 0x03 # POWER REGISTER (R)
REG_MASK_ENABLE  = 0x06 # MASK ENABLE REGISTER (R/W)
REG_ALERT_LIMIT  = 0x07 # ALERT LIMIT REGISTER (R/W)
REG_MFG_UID      = 0xFE # MANUFACTURER UNIQUE ID REGISTER (R)
REG_DIE_UID      = 0xFF # DIE UNIQUE ID REGISTER (R)

broadcast_messages = False
shutdown_control = False
csv_output = False
quiet_output = False
sent_low_broadcast = False
sent_vlow_broadcast = False

bus = SMBus(I2C_BUS)


def read_register(reg):
    data = bus.read_i2c_block_data(INA260_ADDR, reg, 2)
    val = (data[0] << 8) + data[1]
    return val


def raw_to_amps(value):
    return (value * 1.25) / 1000.0


def amps_to_raw(value):
    return (value * 1000.0) / 1.25


def raw_to_volts(value):
    return (value * 1.25) / 1000.0


def volts_to_raw(value):
    return (value * 1000.0) / 1.25


def raw_to_watts(value):
    return (value * 10.0) / 1000.0


def watts_to_raw(value):
    return (value * 1000.0) / 10.0


def get_current():
    val = read_register(REG_CURRENT)
    return raw_to_amps(val)


def get_voltage():
    val = read_register(REG_BUSVOLTAGE)
    return raw_to_volts(val)


def get_power():
    val = read_register(REG_POWER)
    return raw_to_watts(val)


def get_battery_state():
    """Get battery status."""
    voltage = get_voltage()
    percentage = (voltage - MIN_VOLTAGE) / VOLTAGE_RANGE
    if percentage < 0.0:
        percentage = 0.0
    elif percentage > 1.0:
        percentage = 1.0
    return voltage, percentage


def output_level(voltage, percentage):
    """Print battery level output."""
    if not quiet_output:
        if csv_output:
            print(datetime.now(), voltage, percentage, sep=",")
        else:
            print("{:.3f}V ({:.2%})".format(voltage, percentage))


def broadcast_message(message):
    """Send a broadcast message to all users."""
    if broadcast_messages:
        subprocess.run(["wall", message])


def broadcast_level(message, voltage, percentage):
    """Broadcast a battery level message."""
    broadcast_message("Warning: battery level {} ({:.3f}V / {:.2%})".format(message, voltage, percentage))


def trigger_shutdown():
    """Trigger a system shutdown."""
    if shutdown_control:
        broadcast_message("Warning: battery level critical. Shutting down now...")
        subprocess.run(["shutdown", "now"])


def check_battery():
    """Check battery level and respond appropriately."""
    global sent_low_broadcast, sent_vlow_broadcast
    voltage, percentage = get_battery_state()
    output_level(voltage, percentage)
    if voltage <= BAT_CRIT_VOLTAGE:
        broadcast_level("critical", voltage, percentage)
        trigger_shutdown()
    elif voltage <= BAT_VLOW_VOLTAGE:
        if not sent_vlow_broadcast:
            broadcast_level("very low", voltage, percentage)
            sent_vlow_broadcast = True
    elif voltage <= BAT_LOW_VOLTAGE:
        if not sent_low_broadcast:
            broadcast_level("low", voltage, percentage)
            sent_low_broadcast = True


def main():
    """Entry point."""
    global broadcast_messages, shutdown_control, csv_output, quiet_output

    parser = argparse.ArgumentParser(description="Monitor car battery level.")
    parser.add_argument("-r", "--repeat", action="store_true", help="repeat monitoring in a loop")
    parser.add_argument("-d", "--delay", type=float, default=5, help="repeat delay in seconds (default 5)")
    parser.add_argument("-b", "--broadcast", action="store_true", help="broadcast battery low messages")
    parser.add_argument("-s", "--shutdown", action="store_true",
                        help="shutdown Jetson when battery gets critical (requires root)")
    parser.add_argument("-c", "--csv", action="store_true", help="use CSV output format")
    parser.add_argument("-q", "--quiet", action="store_true", help="do not print output to terminal")
    args = parser.parse_args()

    repeat = args.repeat
    delay = args.delay
    broadcast_messages = args.broadcast
    shutdown_control = args.shutdown
    csv_output = args.csv
    quiet_output = args.quiet

    bus = SMBus(I2C_BUS)

    if csv_output and not quiet_output:
        print("datetime, voltage, percentage")

    check_battery()

    if repeat:
        try:
            while True:
                sleep(delay)
                check_battery()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
