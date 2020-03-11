#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


from pymeasure.instruments.newport import ESP300
from pymeasure.instruments import list_resources

from pymeasure.display import widgets as pw
from pymeasure.display.inputs import *

import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from ftd2xx import listDevices, getDeviceInfoDetail

import pymeasure.experiment.parameters as pars

from time import sleep
from pymeasure.experiment import Procedure
from pymeasure.experiment import IntegerParameter

import sys

FTDIresources = listDevices()
FTDIresources
serial = FTDIresources[0]

def mirror(switch):
    """Switch 'on' or 'off'"""
    serial = FTDIresources[0]
    # Raw byte commands for "MGMSG_MOT_MOVE_JOG".
#     on = b"\x6A\x04\x00\x01\x21\x01"  # x01 up
#     off = b"\x6A\x04\x00\x02\x21\x01"  # x02 down
    
    if switch == 'on':
        motor = ftd2xx.openEx(serial)
        print(motor.getDeviceInfo())
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
        motor = ftd2xx.openEx(serial)
        print(motor.getDeviceInfo())
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






