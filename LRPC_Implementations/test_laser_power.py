# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:00:00 2022

@author: UWAdmin
"""

import LRPC


#%%



sc = LRPC.SystemControl()

sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

vaccum_time = 0.25
sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)
#%%
sc.move_stage_to_coordinates(2,7,2.5)
sc.set_line_travel_time(2000)
sc.print_stage_positions()
sc.set_line_power(0.01)
sc.power_on_laser() 
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))
line = 1

#drawing_line(line)
#sc.move_stage_to_coordinates(1,3,2.5)
#sc.pattern_line(1,line_axis="X")
#sc.set_line_power(1000)
#sc.set_line_travel_time(2000)
import numpy as np
p = np.round(np.array(np.linspace(5.5,6.5,6)),1)
print(p)
#%%

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(2,7,2.5)
sc._laser.power = p[0]
sc.pattern_line(3,line_axis="Y")

#sc.set_line_power(100)
sc.set_line_travel_time(2000)
#sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)
line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(3.5,7,2.5)
sc._laser.power = p[1]
sc.pattern_line(3,line_axis="Y")

#sc.set_line_power(200)
sc.set_line_travel_time(2000)

sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(5,7,2.5)
sc._laser.power = p[2]
sc.pattern_line(3,line_axis="Y")

#sc.set_line_power(300)
sc.set_line_travel_time(2000)
#sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)
line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(6.5,7,2.5)
sc._laser.power = p[3]
sc.pattern_line(3,line_axis="Y")
#sc.set_line_power(400)
sc.set_line_travel_time(2000)

sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)

line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(8,7,2.5)
sc._laser.power = p[4]
sc.pattern_line(3,line_axis="Y")
#sc.set_line_power(500)
sc.set_line_travel_time(2000)
#sc.vacuum_air_and_fill_inert_gas(120,vaccum_time)
line = line+1
drawing_line(line)
sc.move_stage_to_coordinates(9.5,7,2.5)
sc._laser.power = p[5]
sc.pattern_line(3,line_axis="Y")
#sc.set_line_power(600)
sc.set_line_travel_time(2000)


sc.power_off_laser()

