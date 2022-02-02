# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 18:59:03 2022

@author: UWAdmin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:11:19 2021

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
sc.move_stage_to_coordinates(2,7,2.5)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

sc.set_line_power(650)
sc.set_line_travel_time(2000)

line=1

#%% X-lines
drawing_line(line)
sc.move_stage_to_coordinates(1,7.5,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1


drawing_line(line)
sc.move_stage_to_coordinates(3,7.5,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(5,7.5,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(7,7.5,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(2,9,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(4,9,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(6,9,2.5)
sc.pattern_line(1.5,line_axis="X")
line = line+1


#%% Y-lines
drawing_line(line)
sc.move_stage_to_coordinates(2,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(3,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(4,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(5,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(6,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1

drawing_line(line)
sc.move_stage_to_coordinates(7,7,2.5)
sc.pattern_line(2,line_axis="Y")
line = line+1





sc.power_off_laser()

sc.pressure_control.to_ambient()

