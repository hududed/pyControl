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
start_x = 5
start_y = 3
sc.move_stage_to_coordinates(start_x,start_y,2.9)
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



def pattern_column(start_x,start_y, power_range):
    line_length = 2
    print('Line Length = ', line_length)
    setting_travel_time(4000)
    add_position = 1.5
    line = 1
    power_range = np.append(power_range,power_range[-1])
    for pow in power_range:
        drawing_line(line)
        pow = round(pow,2)
        set_power_line(pow)
        sc.move_stage_to_coordinates(start_x,start_y,2.5)
        sc.pattern_line(line_length,axis="X")
        start_y += add_position
        line+=1
        # sc.vacuum_air_and_fill_inert_gas(120,0.5)
        time.sleep(5)

power_test = np.linspace(250,1200,10)
power_test_c1 = power_test[:5]
power_test_c2 = power_test[len(power_test)//2:]

pattern_column(3,5,power_test_c1)
sc.vacuum_air_and_fill_inert_gas(120,0.5)
pattern_column(6,5,power_test_c2)





#%%
#sc.vacuum_air_and_fill_inert_gas(120,1)


#%%
sc.power_off_laser()
sc.pressure_control.to_ambient()

print("Program Finished")
# %%
