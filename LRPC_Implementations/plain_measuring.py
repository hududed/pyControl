# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 14:08:30 2022

@author: UWAdmin
"""
#%%

import LRPC_Rev3 as LRPC
import time
import numpy as np
import random

#%%

class laser_power_up:
    def __init__(self):
        sc.flip_down_mirror()
        sc.set_line_power(700)
        sc.power_on_laser()
        print("Laser on signal sent") 
        self.start_time = time.time()
    def wait_till_powered(self, wait_time = 60):
        while (time.time() - self.start_time < 60):
            None # Wait untill time 


sc = LRPC.SystemControl()


lp = laser_power_up()


sc.reset_stage_position()
sc.print_stage_positions()
sc.connect_to_pump()
# sc.pressure_control.to_ambient()
# sc.pressure_control.to_ambient()




class MeasurePlain:
    def __init__(self, start_z:float)->None:
        self.x = 0
        self.y = 0
        self.z = start_z
        self.grid_spots = []

    def MeasureSpot(self,x:float,y:float):
        scan_x = x
        scan_x = y
        marker_z = self.z

        try:
            sc.move_stage_to_coordinates(scan_x,scan_y,marker_z)
        except:
            sc.power_off_laser()

        sc.vacuum_air_and_fill_inert_gas(120,1)
        sc.flip_up_mirror()

        #place one dot to mark the sample
        lp.wait_till_powered()
        sc.flip_up_mirror()
        print("Placing Dot")
        time.sleep(30)
        sc.flip_down_mirror()



        sc._laser.power = 0.10
        sc.initialize_LightField()

        sc.flip_up_mirror()

        print("Enter z value (enter 0 when done):")
        z_request= 0


        while True:
            print(z_request)
            z_request = input(':') 
            if z_request == '':
                break
            z_request = float(z_request)

            if z_request > 5.3:
                bound = 5.3
                print(f"z cannot exceed {bound}")
                print(f"z set to {bound}")
                z_request = 5.3

            sc.move_stage_to_coordinates(scan_x,scan_y,z_request)
            self.z = z_request
            
            
        sc.flip_down_mirror()
        sc.print_stage_positions()

        self.grid_spots.append([scan_x,scan_y,self.z])
        

scan_x = 4.5
scan_y = 12
marker_z = 2.95

Plain = MeasurePlain(2.95)

Plain.MeasureSpot(4.5+1,12-(12-5)/2)
Plain.MeasureSpot(4.5-1,12-(12-5)/2)

Plain.MeasureSpot(4.5,12)
Plain.MeasureSpot(4.5,12-5)



print('Here are the grid locations:', Plain.grid_spots)


#%%
sc.move_stage_to_coordinates(7,7,1.8)
sc.power_off_laser()
sc.pressure_control.to_ambient()

print("Program Finished")

# %%
