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

scan_x = 4.5
scan_y = 12
marker_z = 4.0

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



sc._laser.power = 0.1
sc.initialize_LightField()

sc.flip_up_mirror()

print("Enter z value (enter 0 when done):")
z_request= 0


def get_intensity()->float:
    measured_peak:float = LRPC.capture_photo("adjust", 1, 1, 1, target='GD')
    return measured_peak

def get_intensity_average(n:int)->float:
    intensities = [float]
    for i in range(n):
        intensities.append(get_intensity())
    
    intensity_avg: float = np.average(intensities)
    return intensity_avg

def not_precise(z_focus:float, precision:float)->bool:
    if precision >= z_focus:
        return True
    else:
        return False

def search_focus(low_bound:float, high_bound:float)->list:
    best_intensity = 0
    best_z = 0
    search_range:np.ndarray = np.linspace(low_bound, high_bound,10)
    for z in search_range:
        sc.move_stage_to_coordinated(scan_x,scan_y,z)
        new_intensity = get_intensity_average(5)
        if new_intensity>best_intensity:
            best_intensity = new_intensity
            best_z = z

    return [best_intensity,z]

def state_intensity(intensity, z):
    print(f'The best intesity found is = {intensity}\nThe best z value is found at z={z}')

def find_focus(start_z):
    precision:float = 0.1
    intensity, z = search_focus(start_z-precision,start_z+precision)
    state_intensity(intensity, z)
    precision:float = 0.01
    search_focus(z-precision,z+precision)
    state_intensity(intensity, z)
        




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
    
    
sc.flip_down_mirror()
sc.print_stage_positions()
