# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:00:00 2022

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

sc.vacuum_air_and_fill_inert_gas(120,1)
#%%
sc.move_stage_to_coordinates(2,7,2.5)
sc.set_line_travel_time(2000)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))
line = 1

drawing_line(line)
sc.move_stage_to_coordinates(1,3,2.5)
sc.pattern_line(1,line_axis="X")
sc.set_line_power(1000)
sc.set_line_travel_time(2000)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(2,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(100)
sc.set_line_travel_time(2000)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(3.5,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(200)
sc.set_line_travel_time(2000)

sc.vacuum_air_and_fill_inert_gas(120,1)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(5,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(300)
sc.set_line_travel_time(2000)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(6.5,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(400)
sc.set_line_travel_time(2000)

sc.vacuum_air_and_fill_inert_gas(120,1)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(8,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(500)
sc.set_line_travel_time(2000)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(9.5,7,2.5)
sc.pattern_line(3,line_axis="Y")
sc.set_line_power(600)
sc.set_line_travel_time(2000)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(9.5,3,2.5)
sc.pattern_line(1,line_axis="Y")
sc.set_line_power(1000)
sc.set_line_travel_time(2000)

sc.power_off_laser()

