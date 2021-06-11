#!/usr/bin/env python
# coding: utf-8

from pyModbusTCP.client import ModbusClient
from pymeasure.instruments.edwards import NXDS


# TCP auto connect on first modbus request (MKS Newport PAC100)
c = ModbusClient(host="192.168.1.3", port=502, auto_open=True)

# connect to NXDS vacuum pump
pump = NXDS('ASRL7::INSTR')


def current_pressure():
    # transform provided by MKS
    p = c.read_input_registers(5000, 1)[0]/32767*3000
    return int(p)


def open_valve(name):
    if name == "mid":  # Nitrogen
        c.write_single_register(5000, 32768)
    elif name == "argon":  # Argon
        c.write_single_register(5001, 32768)
    elif name == "vac":  # vacuum
        c.write_single_register(5002, 32768)
    elif name == "out":  # out
        c.write_single_register(5003, 32768)


def close_valve(name):
    if name == "mid":
        c.write_single_register(5000, 0)
    elif name == "argon":
        c.write_single_register(5001, 0)
    elif name == "vac":
        c.write_single_register(5002, 0)
    elif name == "out":
        c.write_single_register(5003, 0)


def close_all():
    valves = ["mid", "argon", "vac", "out"]
    for i in valves:
        close_valve(i)


close_all()


def gopr(pr):
    """Goes to pressure input"""
    while current_pressure() > pr:
        open_valve('out')
    close_valve('out')
    print('done')
    import time
    time.sleep(1)
    close_all()
    while current_pressure() < pr:
        #         if current_pressure()<pr:
        open_valve('mid')
        open_valve('argon')
        time.sleep(.1)
        if current_pressure() >= pr:
            close_valve('mid')
            close_valve('argon')

    current_pressure()
