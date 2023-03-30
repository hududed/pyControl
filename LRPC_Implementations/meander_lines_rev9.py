# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:51:11 2022

@author: UWAdmin
"""


from LRPC import SystemControl
sc = SystemControl()



#%%
sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()

sc.vacuum_air_and_fill_inert_gas(120,0.15)
sc.move_stage_to_coordinates(2,7,2.5)
sc.print_stage_positions()

sc.power_on_laser()
sc.set_line_power(870)
sc.set_line_travel_time(2000)

class meandor_line:
    def __init__(self, start_location=[2,7,2.5]):
        sc.move_stage_to_coordinates(start_location[0],start_location[1],
                                     start_location[2])
        
        self.meandor_number = 0
        
    def meandor(self, x_length, y_length):
        self.meandor_number = self.meandor_number + 1
        line_number = 0
        
        def print_step():
            print("Starting Line #:%i of Meandor #:%i"%(line_number,self.meandor_number))
        
        line_number += 1
        print_step()
        sc.pattern_line(x_length, line_axis="X")
        sc.pattern_line(x_length, line_axis="X")
        
        line_number += 1
        print_step()
        sc.pattern_line(y_length, line_axis="Y")
        
        line_number += 1
        print_step()
        sc.pattern_line(x_length, line_axis="X")
        
        sc.move_stage_to_coordinates(sc.x_position,sc.current_y_position,sc.z_position)
        line_number += 1
        print_step()
        sc.pattern_line(y_length, line_axis="Y")
        
        sc.move_stage_to_coordinates(sc.x_position,sc.current_y_position,sc.z_position)
               

ml = meandor_line()
ml.meandor(1.5,2)
ml.meandor(1.5,2)
ml.meandor(1.5,2)
ml.meandor(1.5,2)
#%%
sc.power_off_laser()
sc.pressure_control.to_ambient()