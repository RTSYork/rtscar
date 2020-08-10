#!/usr/bin/env python3

from smbus import SMBus
from time import sleep

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

print('INA260 Power Monitor Test')

bus = SMBus(I2C_BUS)

while True:
    current = get_current()
    voltage = get_voltage()
    power = get_power()

    print()
    print("Voltage: {}V".format(round(voltage, 3)))
    print("Current: {}A".format(round(current, 3)))
    print("Power:   {}W".format(round(power, 3)))

    sleep(10)
