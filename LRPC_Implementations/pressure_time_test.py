# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:08:30 2022

@author: UWAdmin
"""
#%%

import LRPC
import time
import numpy as np
import random
sc = LRPC.SystemControl()
#%%




class PressureTest:
    def __init__(self):
        self.pressure_time = [list]
        sc.pressure_control.to_vacuum(0.5)
    def time_pressurization(self, pressure:float):
        sc.pressure_control.to_ambient()
        start_time = time.time()
        sc.pressure_control.gopr(pressure)
        pres_time = time.time() - start_time
        self.pressure_time.append([pressure,pres_time])
        print(self.pressure_time)
#%%

test = PressureTest()
for p in np.linspace(50,800,10):
    test.time_pressurization(p)
    pres_time = test.pressure_time

sc.pressure_control.to_ambient()
#%%
print("Program Finished")
print(f'Here is preessurization times [pressure, time]:{pres_time}')

# print(f'Here are the powers:{power_range}')
# %%
