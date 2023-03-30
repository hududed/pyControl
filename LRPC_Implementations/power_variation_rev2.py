# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:08:30 2022

@author: UWAdmin
"""
#%%

import LRPC_Rev3 as LRPC
import time
import numpy as np
#%%

#laser = LRPC.LaserSystemControl()
#raman = LRPC.RamanSpectrometerControl()
#cell = LRPC.CellAndMirrorControl()

sc = LRPC.SystemControl()

sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

vacuum_time = 0.15
# sc.vacuum_air_and_fill_inert_gas(120,vacuum_time)
#%%
start_x = 2
sc.move_stage_to_coordinates(start_x,7,2.9)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

def setting_travel_time(time):
    print("\nSetting Travel Time at %i ms\n" % (time))
    sc.set_line_travel_time(time)

def set_power_line(power):
    print(f"\Setting Laser Power to: {power}")
    sc.set_line_power(power)



sc.vacuum_air_and_fill_inert_gas(120,1)


line_length = 2
print('Line Length = ', line_length)
axis = "Y"

setting_travel_time(5000)
add_position = 1.5
line = 1
power_test = np.linspace(600,900,6)
power_test = np.append(power_test,power_test[-1]) #doesn't print last value
for pow in power_test:
    drawing_line(line)
    pow = round(pow,2)
    set_power_line(pow)
    sc.move_stage_to_coordinates(start_x,7,2.5)
    sc.pattern_line(line_length,axis="Y")
    start_x += add_position
    line+=1
    time.sleep(5)

#%%
#sc.vacuum_air_and_fill_inert_gas(120,1)


#%%
sc.power_off_laser()
sc.pressure_control.to_ambient()

print("Program Finished")
# %%
