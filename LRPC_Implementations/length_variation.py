# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:08:30 2022

@author: UWAdmin
"""
#%%

import LRPC


#%%



sc = LRPC.SystemControl()

sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

vacuum_time = 0.15
# sc.vacuum_air_and_fill_inert_gas(120,vacuum_time)
#%%
sc.move_stage_to_coordinates(2,7,2.5)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

def setting_travel_time(time):
    print("\nSetting Travel Time at %i ms\n" % (time))
    sc.set_line_travel_time(time)


line = 1
sc.set_line_power(870)
sc.set_line_travel_time(2000)
drawing_line(line)
#sc.vacuum_air_and_fill_inert_gas(120,1)

line_length = 1
axis = "Y"

setting_travel_time(4000)

sc.move_stage_to_coordinates(2,7,2.5)
sc.pattern_line(line_length,axis="Y")

setting_travel_time(1200)
#%%
line = 2
sc.move_stage_to_coordinates(3,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 3
#sc.vacuum_air_and_fill_inert_gas(120,vacuum_time)

setting_travel_time(1400)

drawing_line(line)
sc.move_stage_to_coordinates(4,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 4
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(1600)

drawing_line(line)
sc.move_stage_to_coordinates(5,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 5
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(1800)

drawing_line(line)
sc.move_stage_to_coordinates(6,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 6
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(2000)

drawing_line(line)
sc.move_stage_to_coordinates(7,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 7
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(2200)

drawing_line(line)
sc.move_stage_to_coordinates(8,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 8
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(2400)

drawing_line(line)
sc.move_stage_to_coordinates(9,7,2.5)
sc.pattern_line(line_length,axis="Y")
line = 9
#sc.vacuum_air_and_fill_inert_gas(120,1)

setting_travel_time(2600)

drawing_line(line)
sc.move_stage_to_coordinates(10,7,2.5)
sc.pattern_line(line_length,axis="Y")

#sc.vacuum_air_and_fill_inert_gas(120,1)


#%%
sc.power_off_laser()
sc.pressure_control.to_ambient()



# %%
