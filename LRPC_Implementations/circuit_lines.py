# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 16:11:19 2021

@author: UWAdmin
"""

import LRPC


#%%


sc = LRPC.SystemControl()

sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

sc.vacuum_air_and_fill_inert_gas(120,1)
sc.move_stage_to_coordinates(2,7,2.5)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line_comment(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

sc.set_line_power(650)
sc.set_line_travel_time(2000)

drawing_line_comment(1)
sc.move_stage_to_coordinates(2,7,2.5)
sc.pattern_line(2,line_axis="Y")

drawing_line_comment(2)
sc.move_stage_to_coordinates(3,7,2.5)
sc.pattern_line(3,line_axis="Y")

drawing_line_comment(3)
#fell out of range here
sc.move_stage_to_coordinates(4,7,2.5)
sc.pattern_line(4,line_axis="Y")

drawing_line_comment(4)
sc.move_stage_to_coordinates(5,7,2.5)
sc.pattern_line(5,line_axis="Y")


