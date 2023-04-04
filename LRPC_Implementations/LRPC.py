
"""
Laser Ramen Platform System Control - Library
Created on Sat Dec 11 16:11:19 2021

@author: Todd Muller
@contact_email: todd.m.muller12@gmail.com
"""
#%%
import os, glob #import libraries
import os 
from pymeasure.instruments.lighthousephotonics import Sprout

from threading import Thread
import time
from time import sleep
from datetime import datetime, timedelta

from random import randrange

from newportxps import NewportXPS

import numpy as np
import pandas as pd
from write_utils import write_data_files, get_mean, get_move_y, duplicate_to_dataset

import numpy as np
import csv
        
from flipper import mirror #import flipper mirror codes
from spectra import capture_photo #import spectrometer codes

from pathlib import Path

# from spectra import *
import spectra as IsoPlane

# from pressure import close_valve,open_valve,close_all,current_pressure,gopr, to_ambient, to_vacuum, quick_fill
import pressure as pressure_control
from pymeasure.instruments.edwards import NXDS

from fits import new_plot_LIG
import threading

#%% Import Libraries



# import pressure as pressure_control
#%% Operational Setup
os.getcwd() #get directory
os.chdir(r'C:\Users\UWAdmin')

#Initialize connections
xpsd_remoteip = '192.168.254.254' #xps ip address 
hostname = 'XPS-1b81' #login host name
xps = NewportXPS(xpsd_remoteip) #connecting to the xps
xps = NewportXPS(xpsd_remoteip)
if not isinstance(xps,NewportXPS):
    print("xps is a critical variable and is improper data type\n",
          "Expected: \"newportxps.newportxps.NewportXPS\"")
    print("Stopping Program")
    os.sys.exit()
 #check if xps is proper instance
print(xps.status_report()) #get xps status
print("Connected to xps")
#%%


    

class SystemControl:
    
    def __init__(self, XPS=xps, pressure_control=pressure_control):
        self._XPS = XPS
        self.pressure_control = pressure_control
        
        self.reset_stage_position()
        self.print_stage_positions()
        
        self.connect_to_pump()
        
        #Connecting to Laser
        print("Connecting to laser")
        self._laser = Sprout('COM4')
        self._laser.adapter.connection.baud_rate = 19200
        self._laser.adapter.connection.read_termination = '\r'
        self._laser.adapter.connection.write_termination = '\r'
        self._laser.write("OPMODE=Off")
        print("Laser Connected")
        
        #Connecting to Raman
        self._XPS = XPS
        #self.GD_ratios = pd.DataFrame()
        
        #Defining instance variables
        self.line_number = 0 #used to track number of lines printed per run
        

    def reset_stage_position(self):
        self._XPS.kill_group('XYZ') #clear XYZ group
        self._XPS.initialize_allgroups() #initialize addressing
        self._XPS.home_allgroups() #send control plate to origin
        
    def print_stage_positions(self):
        print("Platform Positions\n-------------------")
        for sname, _ in self._XPS.stages.items():
            print('{}: {}'.format(sname, self._XPS.get_stage_position(sname)))
    
    def sync_stage_current_position(self):
        positions = []
        for sname, _ in self._XPS.stages.items():
            positions.append(self._XPS.get_stage_position(sname))
        self.x_position, self.y_position, self.z_position = positions
    
    """PRESSURE CONTROL METHODS"""
    def connect_to_pump(self,resource_name='ASRL5::INSTR'):
        self.pressure_control.NXDS(resource_name)
        
        
    def fill_with_inert(self):
        self.pressure_control.quick_fill()
        self.pressure_control.close_all()
        
    def decompress_to_pressure(self,final_pressure):
        for i in range(5): self.pressure_control.gopr(final_pressure)
        
    def vacuum_air_and_fill_inert_gas(self, final_pressure = 120, vacuum_time=1):
        
        print("Current Pressure: ",self.pressure_control.current_pressure())
        self.pressure_control.close_all()
        self.pressure_control.to_ambient()
        self.pressure_control.to_vacuum(vacuum_time)
        print("Vacuumed Pressure: ",self.pressure_control.current_pressure())
        
        time.sleep(5)
        vacuum_pressure = self.pressure_control.current_pressure()
        
        #5 is an arbitrary low number and can be changed as needed
        if vacuum_pressure < 5:
            self.fill_with_inert()
            self.decompress_to_pressure(final_pressure)
        elif vacuum_pressure > 5000:
            #Assume this pressure is an overlaod value, and the real value is near 0
            self.fill_with_inert()
            self.decompress_to_pressure(final_pressure)
        else:
            print("Current Pressure: ",vacuum_pressure)
            self.power_off_laser()
            os.sys.exit("Vacuum not established!!!")
            
        print("Final Pressure")
        print("Here is the innert pressure", self.pressure_control.current_pressure())
        

    def flip_up_mirror(self):
        mirror("on")
        
    def flip_down_mirror(self):
        mirror("down")

    """LASER CONTROL METHODS"""
    def move_stage_to_coordinates(self,x,y,z):
        self._XPS.move_stage('XYZ.X',x)
        self._XPS.move_stage('XYZ.Y',y)
        self._XPS.move_stage('XYZ.Z',z)
        
        self.current_x_position=x
        self.current_y_position=y
        self.current_z_position=z
        self.sync_stage_current_position()
        
#        print("Stage moved to:\nx={}\ny={}\nz={}"\
#              .format(x,y,z))
        
    def power_on_laser(self):
        self._laser.write("OPMODE=On")

    def power_off_laser(self):    
        self._laser.write("OPMODE=Off")
        
    def set_line_power(self, laser_power):
        # self._laser.power = (laser_power/0.0994)/1000
        self._laser.power = (laser_power/0.2163)/1000

        
    
    def set_line_travel_time(self, line_travel_time=2000):
        self._line_travel_time = line_travel_time
        
    
    """RAMAN CONTROL METHODS"""
    def initialize_LightField(self):
        print("Initializing LightField")
        IsoPlane.capture_photo("start",2,1,0) #launch LightField software
        exposure=1000
        center_wavelength=1500
        # input("Please confirm LightField application has properly started and that \
        #       the following paraters have been properly set:\n\
        #       Exposure: %f\n\
        #       Center Wavelenth: %f\n\
        #       (Press Enter on the Kernel to Confirm)\n" % 
        #       (exposure, center_wavelength))
        
    def measure_raman(self):
        self.line_length
        check=[float(self._start_location)+
               self.line_length/10*i for i in range(1,10)]
          
        
        
        for i in range(9):
            
            self._XPS.move_stage(self._axis, check[i])
            self.print_stage_positions()
            
            for j in range(1):
                self.flip_up_mirror()
                print("post patterning...")
                IsoPlane.capture_photo("on", i, self.line_number, j)
                
                self.flip_down_mirror()
                time.sleep(5)
                
        one=[]
        bg=[]
        fit=[]
        
        
        a="line "
        b=str(i)+"*.csv"
        c=a+b
        for file in glob.glob(c):one.append(f"{file}")
        for file in glob.glob("background*.csv"):bg.append(f"{file}")    
        print(len(one))
        
        increment=0
        line_number=i
        for ix in range(int(len(one)/2)):
            d1 = pd.read_csv(one[increment])
            d2 = pd.read_csv(one[increment+1])
            _d1 = pd.read_csv(bg[0])
            _d2 = pd.read_csv(bg[1])
            increment+=2
            f=new_plot_LIG(d1,d2,_d1,_d2, ix, 0, line_number)
            print(ix)
            fit.append(f)
            print("Here is the g/d that was scanned:")
            print(f)
        print("done")
        
       
    def patterning_motion_control_thread(self): #This was formerly A2
        
        if self._trajectory_df['ramptime'][0]<0.5:
            time.sleep(.5-self._trajectory_df['ramptime'][0])
        print("motion controller started")
        xps.run_trajectory('foreward',) #Send execution command for trajectory
        time.sleep(np.sum(self._trajectory_df['ramptime'])) #sleep while line is drawn
        #laser_power.power=0.01 #this is setting the laser_power back to a default of 0.1 -Todd
        print("finished and current position is:\n")
        self.print_stage_positions()



    def patterning_mirror_control_thread(self): #This was formerly B2
        
        for i in range(2):
           
            if i==0:
                if self._trajectory_df['ramptime'][0]<0.5: #This dataFrame is being defined in Section C line 41 -Todd
                    print("i: {}, mirror on".format(i))
                    start_time = time.monotonic()
                    mirror('on')
                    end_time = time.monotonic()
                    print("i: {}, {}".format(i,timedelta(seconds=end_time - start_time)))
                    time.sleep(self._trajectory_df['ramptime'][1]) #time for linear line    
                else:
                    time.sleep(self._mirror_sleep)
                    print("mirror on")
                    start_time = time.monotonic()
                    mirror('on')
                    end_time = time.monotonic()
    #                 print("time to put the mirror on: ",start_time-end_time)
                    print("i: {}, {}".format(i,timedelta(seconds=end_time - start_time)))
                    time.sleep(self._trajectory_df['ramptime'][1]) #time for linear line
            else:
                mirror('off')
                print("mirror off")     
            
    def pattern_line(self,line_length, axis="X"):
        print("Patterning is starting")
        
        #Track number of lines printed with this run
        self.line_number = self.line_number + 1
        
        self.line_length = line_length
        
        if axis == "X":
            self._start_location = self.x_position
            self._stop_location = self.x_position + self.line_length
            self._axis = 'XYZ.X'
        elif axis == "Y":
            self._start_location = self.y_position
            self._stop_location = self.y_position + self.line_length
            self._axis = 'XYZ.Y'
        else:
            print("Running X as default")
            self._start_location = self.x_position
            self._stop_location = self.x_position + self.line_length
            self._axis = 'XYZ.X'
        
        
        time.sleep(10)
        self.sync_stage_current_position()
               
        #save_line_power = self._laser.power
        #self._laser.power = 0.01
        
        
        self.print_stage_positions()
        
        self._XPS.define_line_trajectories(start=self._start_location,
                                           stop=self._stop_location,
                                           step=0.01,
                                           scantime=(self._line_travel_time/1000),
                                           axis=self._axis[-1] #This gets just the last character of the string
                                           )
        
        self._XPS.download_trajectory('foreward.trj')
        
        self._trajectory_df = pd.read_csv('foreward.trj', header=None)
        self._trajectory_df = self._trajectory_df.loc[:, (self._trajectory_df != 0).any(axis=0)] 
        #delete all columns that contain only zeros
        
        self._trajectory_df.columns = ['ramptime','rampdist','rampvel']
        
        
        self._mirror_sleep = self._trajectory_df['ramptime'][0]-.5
        
        print(self._trajectory_df)
        
        line_ramping_distance = self._trajectory_df['rampdist'][0]
        self._XPS.move_stage(self._axis, 
                             self._start_location-line_ramping_distance)
        self._XPS.move_stage
        self.print_stage_positions()
        time.sleep(15) #sleep for 15 seconds       
        print("\n\n")
        self.flip_down_mirror()
        
        #self._laser.power = save_line_power
        
        time.sleep(20)
        
        #Draw Lines
        
        print("Patterning")
        
        #For threading discription see referances at bottom of file
        motion_control = threading.Thread(target=self.patterning_motion_control_thread)
        mirror_control = threading.Thread(target=self.patterning_mirror_control_thread)
        
        motion_control.start()
        print("Motion Control Thread Started")
        mirror_control.start()
        print("Mirror Control Thread Started")
        
        motion_control.join()
        print("Motion Control Thread Joined")
        mirror_control.join()
        print("Mirror Control Thread Joined")
        
        
        
        self.sync_stage_current_position()
                
        # time.sleep(10)
                
        print("\nLine Drawn")
        
        # self._XPS.move_stage(axis, self._stop_location)
        # self.sync_stage_current_position()
        
        time.sleep(15)
        print("Line Finished\n\n")

        
        
        
        

        
#%%
"""
Threading Referance:
https://stackoverflow.com/questions/15365406/run-class-methods-in-threads-python
"""

    
    

    
    
    
    
    
    
    