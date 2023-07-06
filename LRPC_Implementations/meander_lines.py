# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 15:18:44 2022

@author: Todd Muller
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

sc.set_line_power(870)
sc.set_line_travel_time(2000)

line=1

#%% X-lines
drawing_line(line)
sc.move_stage_to_coordinates(1,7.5,2.5)
sc.pattern_line(1.0,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,vacuum_time)


drawing_line(line)
sc.move_stage_to_coordinates(1,7.5,2.5)
sc.pattern_line(1.0,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(3,7.5,2.5)
sc.pattern_line(1.0,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(5,7.5,2.5)
sc.pattern_line(1,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(7,7.5,2.5)
sc.pattern_line(1,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(2,9,2.5)
sc.pattern_line(1,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(4,9,2.5)
sc.pattern_line(1,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(6,9,2.5)
sc.pattern_line(1,line_axis="X")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)


#%% Y-lines
drawing_line(line)
sc.move_stage_to_coordinates(2,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(3,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(4,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(5,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(6,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(7,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1
#sc.vacuum_air_and_fill_inert_gas(120,1)

drawing_line(line)
sc.move_stage_to_coordinates(7,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1



sc.power_off_laser()

sc.pressure_control.to_ambient()

