#!/usr/bin/env python

from pyModbusTCP.client import ModbusClient
import time
# import numpy as np
from pymeasure.instruments.edwards import NXDS
# from pymeasure.instruments import list_resources
# import pandas as pd

# TCP auto connect on first modbus request (MKS Newport PAC100)
#default MKS Newport PAC100 IP address: 192.168.1.3
#Manually Set IP address: 192.168.254.77
c = ModbusClient(host="192.168.254.77", port=502, auto_open=True) #new IP address
# connect to NXDS vacuum pump
pump = NXDS('ASRL5::INSTR')

def current_pressure():
    p = c.read_input_registers(5000, 1)[0]/32767*3000 # transform provided by MKS
    return int(p)


def open_valve(name):
    if name == "mid": # Nitrogen
        c.write_single_register(5000,32768)
    elif name == "argon": # Argon
        c.write_single_register(5001,32768)
    elif name == "vac": # vacuum
        c.write_single_register(5002,32768)
    elif name == "out": # out
        c.write_single_register(5003,32768)
        
def close_valve(name):
    if name == "mid":
        c.write_single_register(5000,0) 
    elif name == "argon":
        c.write_single_register(5001,0) 
    elif name == "vac":
        c.write_single_register(5002,0)
    elif name == "out":
        c.write_single_register(5003,0)
        
def close_all():
    valves = ["mid","argon","vac","out"]
    for i in valves:
        close_valve(i)
        
        
        

def gopr(pr:int, print_pressure_timer:float = 10):
    """
    pr: go to pressure (psi)
    print_pressure_timer: time between printing the pressure (s)
    """
    print_pressure_timer = print_pressure_timer * 10
    
    while current_pressure()>pr:
        open_valve('out')
        print(current_pressure())
    close_valve('out')
    print('done')
    time.sleep(1)
    close_all()

    counter = 0
    while current_pressure()<pr:
#         if current_pressure()<pr:
        
        open_valve('mid')
        open_valve('argon')
        time.sleep(.1)
        if current_pressure()>=pr:
            close_valve('mid')
            close_valve('argon')
        if counter >= print_pressure_timer:
            print(current_pressure())
            counter = 0
        counter += 1
    current_pressure()

def to_ambient():
    """Brings to ambient pressure"""
    close_valve('mid')
    close_valve('argon')
    open_valve("out")
    time.sleep(1)
    if current_pressure() < 30:
        close_valve("out")
        current_pressure()
    else:
        time.sleep(1)
        close_valve("out")
    return current_pressure()

def quick_fill():
    """Fill chamber with Argon for 1 sec"""
    open_valve("argon")
    open_valve("mid")
    time.sleep(1)
    close_valve("argon")
    close_valve("mid")
    return current_pressure()

def to_vacuum(t):
    """Brings to vacuum
       t: time in minutes
    """
    
    open_valve("vac")
    time.sleep(3)
    pump.start()
    time.sleep(t*60)
    pump.stop()
    close_valve("vac")
    return current_pressure()

if __name__ == "__main__":
    import numpy as np
    try:
        close_all()
        print('closed')
        time.sleep(1)
        # to_ambient()
        gopr(800)

        close_all()
        print("Finished, no errors")
    except:
        close_all()
