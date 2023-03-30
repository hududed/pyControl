# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:08:30 2022

@author: UWAdmin
"""


import LRPC


#%%

#laser = LRPC.LaserSystemControl()
#raman = LRPC.RamanSpectrometerControl()
#cell = LRPC.CellAndMirrorControl()

sc = LRPC.SystemControl()

sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

vacuum_time = 0.15
sc.vacuum_air_and_fill_inert_gas(120,vacuum_time)
#%%
sc.move_stage_to_coordinates(2,7,2.5)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

line = 1
sc.set_line_power(870)
sc.set_line_travel_time(1500)
drawing_line(line)
sc.move_stage_to_coordinates(2,6,2.5)
sc.pattern_line(2,line_axis="Y")
sc.move_stage_to_coordinates(2,6,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

line_length = 4

drawing_line(line)
sc.move_stage_to_coordinates(3,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(4,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(5,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(6,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(7,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(8,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(9,6,2.5)
sc.pattern_line(line_length,line_axis="Y")
line = line+1


#%%
sc.power_off_laser()
sc.pressure_control.to_ambient()


