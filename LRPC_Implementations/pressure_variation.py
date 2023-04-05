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


scan_x = 4.5
scan_y = 12
marker_z = 2.95


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


while input('Is LightField Scan Stopped?:(yes/no)')!='yes':
    continue


#%%
start_x = 5
start_y = 3
sc.move_stage_to_coordinates(start_x,start_y,z)
sc.print_stage_positions()
sc.power_on_laser()
#%%
def drawing_line(line_number):
    print("\nSTARTING LINE %2.1f\n" % (line_number))

def setting_travel_time(time):
    print("\nSetting Travel Time at %i ms\n" % (time))
    sc.set_line_travel_time(time)

def set_power_line(power):
    print(f"\Setting Laser Power to: {power}")
    sc.set_line_power(power)

#(power, time)




def pattern_column(start_x,start_y, power_range, time_range):
    line_length = 2
    print('Line Length = ', line_length)
    
    add_position = 1
    line = 1
    # power_range = np.append(power_range,power_range[-1])
    for i in range(len(power_range)):
        drawing_line(line)
        set_power_line(power_range[i])
        print('Waiting 40 seconds for laser to power up')
        time.sleep(40)
        setting_travel_time(time_range[i])
        
        sc.move_stage_to_coordinates(start_x,start_y,z)
        sc.pattern_line(line_length,axis="X")
        # sc._laser.power = 0.1
        # sc.measure_raman()
        start_y += add_position
        line+=1
        # sc.vacuum_air_and_fill_inert_gas(120,0.5)
        time.sleep(5)



index = []
powers = []
times = []
#%%
fast_time = 2000
time_range = np.linspace(2000, 12000,6)
# power_range = np.linspace(1500,4000,12)
power1 = 700
power2 = 800
# power_range = [357]*12
settings_set = []
for i in range(0,6):
    settings_set.append((i, power1,time_range[i]))
for i in range(6,12):
    settings_set.append((i, power2,time_range[np.mod(i,6)]))
#%%
# random.shuffle(settings_set)
shuffled_set = settings_set[0:12]

for s in shuffled_set:
    i, p, t = s
    index.append(i)
    powers.append(p)
    times.append(t)

power_test = powers


power_test_c1 = power_test[:len(power_test)//2]
power_test_c2 = power_test[len(power_test)//2:]

times_test = times
times_test_c1 = times_test[:len(power_test)//2]
times_test_c2 = times_test[len(power_test)//2:]
print(f'Here is index:{index}')


pressure = 120
sc.vacuum_air_and_fill_inert_gas(pressure,2)
pattern_column(3-1.5,5+1.5,power_test_c1, times_test_c1)
sc.vacuum_air_and_fill_inert_gas(pressure,2)
pattern_column(6-1.5,5+1.5,power_test_c2, times_test_c2)



#%%
sc.move_stage_to_coordinates(7,7,1.8)
sc.power_off_laser()
sc.pressure_control.to_ambient()

print("Program Finished")
print(f'Here is index:{index}')
# print(f'Here are the powers:{power_range}')
# %%
