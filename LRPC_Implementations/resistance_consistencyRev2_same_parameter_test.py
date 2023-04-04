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
sc.move_stage_to_coordinates(start_x,start_y,4.9)
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

#(power, time)
pressure = 120
sc.vacuum_air_and_fill_inert_gas(pressure,1)



def pattern_column(start_x,start_y, power_range, time_range):
    line_length = 2
    print('Line Length = ', line_length)
    
    add_position = 1
    line = 1
    # power_range = np.append(power_range,power_range[-1])
    for i in range(len(power_range)):
        drawing_line(line)
        set_power_line(power_range[i])
        setting_travel_time(time_range[i])
        
        sc.move_stage_to_coordinates(start_x,start_y,4.9)
        sc.pattern_line(line_length,axis="X")
        start_y += add_position
        line+=1
        # sc.vacuum_air_and_fill_inert_gas(120,0.5)
        time.sleep(5)


index = []
powers = []
times = []
# settings_set = [(1,450,2000), (2,525,2000), (3,600, 2000), (4,675,2000),  (5,750,2000)]*10
# settings_set =  [(1,350,2000),(2,376.92307692,2000),(3,403.84615385,2000), (4,430.76923077,2000), (5,457.69230769, 2000), (6,484.61538462,2000),  (7,511.53846154,2000), (8,538.46153846,2000), (9,565.38461538,2000), (10,592.30769231, 2000), (11,619.23076923,2000),  (12,646.15384615,2000), (13,673.07692308,2000),  (14,700,2000)]
settings_set = [(1, 415,2000)]*15
random.shuffle(settings_set)
shuffled_set = settings_set[0:14]

for s in shuffled_set:
    i, p, t = s
    index.append(i)
    powers.append(p)
    times.append(t)

power_test = powers
power_test_c1 = power_test[:len(power_test)//2]
power_test_c2 = power_test[len(power_test)//2:]

times_test = times
times_test_c1 = times_test[:len(power_test)//2]
times_test_c2 = times_test[len(power_test)//2:]
print(f'Here is index:{index}')



pattern_column(3-1.5,5+1.5,power_test_c1, times_test_c1)
sc.vacuum_air_and_fill_inert_gas(pressure,0.5)
pattern_column(6-1.5,5+1.5,power_test_c2, times_test_c2)





#%%
#sc.vacuum_air_and_fill_inert_gas(120,1)


#%%
sc.move_stage_to_coordinates(12,7,1.8)
sc.power_off_laser()
sc.pressure_control.to_ambient()

print("Program Finished")
print(f'Here is index:{index}')
# %%
