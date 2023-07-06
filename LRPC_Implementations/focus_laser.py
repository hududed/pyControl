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

class laser_power_up:
    def __init__(self):
        self.start_timer

    def start_timer(self):
        sc.flip_down_mirror()
        sc.set_line_power(700)
        sc.power_on_laser()
        print("Laser on signal sent")
        self._start_time = time.time()
    def wait_till_powered(self, wait_time = 60):
        while (time.time() - self._start_time < 60):
            None # Wait untill time 


def pattern_dot(x_position:float=4.5, y_position:float=12, z_position:float=2.95)->None:
    lp.start_timer()
    try:
        sc.move_stage_to_coordinates(x_position,y_position,z_position)
    except:
        sc.power_off_laser()
    #place one dot to mark the sample
    lp.wait_till_powered()
    sc.flip_up_mirror()
    print("Placing Dot")
    time.sleep(30)
    sc.flip_down_mirror()

    


def get_intensity()->float:
    measured_peak:float = LRPC.capture_photo('adjust',0,0,0)
    return measured_peak
def get_intensity_average(n:int)->float:
    intensities = []
    for i in range(n):
        intensities.append(get_intensity())
    
    intensity_avg: float = np.average(intensities)
    return intensity_avg




def state_intensity(intensity:float, z:float):
    print(f'The best intesity found is = {intensity}\nThe best z value is found at z={z}')

def search_focus_space(scan_x, scan_y, z_low_bound:float, z_high_bound:float)->float:
    time.sleep(2)
    best_intensity = 0
    best_z = 0
    search_range:np.ndarray = np.linspace(z_low_bound, z_high_bound,10)
    for z in search_range:
        sc.move_stage_to_coordinates(scan_x, scan_y, z)
        new_intensity = get_intensity_average(3)
        if new_intensity>best_intensity:
            best_intensity = new_intensity
            best_z = z
            print("Test statement:")
            state_intensity(best_intensity,best_z)

    state_intensity(best_intensity,best_z)
    return best_z

def auto_find_focus(scan_x:float, scan_y:float, start_z:float)->float:
    sc._laser.power = 0.1
    precision:float = 0.1
    updated_z:float = search_focus_space(scan_x, scan_y, start_z-precision,start_z+precision)
    return updated_z
        
def manually_find_z(scan_x:float,scan_y:float,z_request:float):
    time.sleep(1)
    sc._laser.power = 0.1
    sc.flip_up_mirror()
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
        z = z_request
    return z



if __name__ == "__main__":
    sc = LRPC.SystemControl()
    lp = laser_power_up()
    sc.initialize_LightField()

    sc.reset_stage_position()
    sc.print_stage_positions()
    sc.connect_to_pump()    

    x, y, z = 3.5, 13, 2.95
    sc.vacuum_air_and_fill_inert_gas(120,1)
    pattern_dot(x,y,z)
    focused_z:float = manually_find_z(x,y,z)
    input("LightField Stopped?")
    focused_z = auto_find_focus(x,y,focused_z)
    second_x,second_y, = 4.5,12
    # sc.vacuum_air_and_fill_inert_gas(120,1)
    pattern_dot(second_x,second_y,focused_z)
    # final_focus_z:float = auto_find_focus(second_x,second_y,second_z)

    print(f"Here is the final focus of z: {focused_z}")
    sc.flip_down_mirror()
    sc.print_stage_positions()
    sc.power_off_laser()
