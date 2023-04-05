#!/usr/bin/env python

from pyModbusTCP.client import ModbusClient
import time
from pymeasure.instruments.edwards import nxds



class PressureControl:
    def __init__(self, MKS_host:str = "192.168.254.77", MRS_port:int = 502):
        #Connect to controller
        self._contoller = ModbusClient(host="192.168.254.77", port=502, auto_open=True) #new IP address
        # connect to vacuum pump
        self.pump = nxds('ASRL5::INSTR')

    def current_pressure(self)->int:
        p = self._controller.read_input_registers(5000, 1)[0]/32767*3000 # transform provided by MKS
        return int(p)


    def open_valve(self, name)->None:
        if name == "mid": # Nitrogen
            self._controller.write_single_register(5000,32768)
        elif name == "argon": # Argon
            self._controller.write_single_register(5001,32768)
        elif name == "vac": # vacuum
            self._controller.write_single_register(5002,32768)
        elif name == "out": # out
            self._controller.write_single_register(5003,32768)
            
    def close_valve(self, name)->None:
        if name == "mid":
            self._controller.write_single_register(5000,0) 
        elif name == "argon":
            self._controller.write_single_register(5001,0) 
        elif name == "vac":
            self._controller.write_single_register(5002,0)
        elif name == "out":
            self._controller.write_single_register(5003,0)
            
    def close_all(self)->None:
        valves = ["mid","argon","vac","out"]
        for i in valves:
            self.close_valve(i)

    def go_to_pressure(self, pressure)->None:
        """Goes to pressure input"""
        while self.current_pressure()>pressure:
            self.open_valve('out')
        self.close_valve('out')
        print('done')
        import time
        time.sleep(1)
        self.close_all()
        while self.current_pressure()<pressure:
            self.open_valve('mid')
            self.open_valve('argon')
            time.sleep(.1)
            if self.current_pressure()>=pressure:
                self.close_valve('mid')
                self.close_valve('argon')

        self.current_pressure()

    def to_ambient(self)->None:
        """Brings to ambient pressure"""
        self.close_valve('mid')
        self.close_valve('argon')
        self.open_valve("out")
        time.sleep(1)
        if self.current_pressure() < 30:
            self.close_valve("out")
            self.current_pressure()
        else:
            time.sleep(1)
            self.close_valve("out")
        return self.current_pressure()

    def quick_fill(self)->None:
        """Fill chamber with Argon for 1 sec"""
        self.open_valve("argon")
        self.open_valve("mid")
        time.sleep(1)
        self.close_valve("argon")
        self.close_valve("mid")
        return self.current_pressure()

    def to_vacuum(self, t)->None:
        """Brings to vacuum
        t: time in minutes
        """
        self.open_valve("vac")
        self.time.sleep(3)
        self.pump.start()
        time.sleep(t*60)
        self.pump.stop()
        self.close_valve("vac")
        return self.current_pressure()
