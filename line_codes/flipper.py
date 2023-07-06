#!/usr/bin/env python

import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from ftd2xx import listDevices, getDeviceInfoDetail

from time import sleep

import sys

# FTDIresources = listDevices()
#serial = [FTDIresources[i] for i,s in enumerate(FTDIresources) if b'37000805' in s] # TO-DO: avoid hard-coding - get index of item with pattern `37000805`
#serial = b'37000805'

def mirror(switch):
    """Switch 'on' or 'off'"""
    serial = b'37000805'
    # Raw byte commands for "MGMSG_MOT_MOVE_JOG".
#     on = b"\x6A\x04\x00\x01\x21\x01"  # x01 up
#     off = b"\x6A\x04\x00\x02\x21\x01"  # x02 down
    
    if switch == 'on':
        print("MIRROR UP")
        motor = ftd2xx.openEx(serial)
        motor.setBaudRate(115200)
        motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
        sleep(.05)
        motor.purge()
        sleep(.05)
        motor.resetDevice()
        motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
        motor.setRts()

        # Send raw bytes to USB driver.
        motor.write(b"\x6A\x04\x00\x01\x21\x01")  # up or 
        motor.close()
    else:
        print("MIRROR DOWN")
        motor = ftd2xx.openEx(serial)
        motor.setBaudRate(115200)
        motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
        sleep(.05)
        motor.purge()
        sleep(.05)
        motor.resetDevice()
        motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
        motor.setRts()

        # Send raw bytes to USB driver.
        motor.write(b"\x6A\x04\x00\x02\x21\x01")  # up or 
        motor.close()
        
        
if __name__ == "__main__":
    """optional location for parameters"""
    print(sys.argv[0])






