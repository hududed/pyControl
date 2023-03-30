#%% Import Libraries

#Program and System Control Libraries
import os 
from threading import *
import time
from time import sleep
from datetime import datetime, timedelta

#Cell Control Libraries (e.g. position, pressure, mirrors)
from newportxps import NewportXPS
from flipper import mirror
import pressure as pressure_control

#from pymeasure.instruments.edwards import NXDS

#Raman Device and Software Control Libraries
import spectra as IsoPlane #import spectrometer codes

#Laser Control Libraries
from pymeasure.instruments.lighthousephotonics import Sprout


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

#%%
class PressureCellControl:
    
    def __init__(self, XPS=xps, pressure_control=pressure_control):
        self._XPS = XPS
        self.pressure_control = pressure_control
        
        self.reset_platform_position()
        self.print_platform_positions()
        
        self.connect_to_pump()

    def reset_platform_position(self):
        self._XPS.kill_group('XYZ') #clear XYZ group
        self._XPS.initialize_allgroups() #initialize addressing
        self._XPS.home_allgroups() #send control plate to origin
        
    def print_platform_positions(self):
        print("Platform Positions\n-------------------")
        for sname, _ in self._XPS.stages.items():
            print('{}: {}'.format(sname, self._XPS.get_stage_position(sname)))
    
    def connect_to_pump(self,resource_name='ASRL5::INSTR'):
        self.pressure_control.NXDS(resource_name)
        
    def print_cell_pressure(self):    
        print("Current Pressure\n-----------------")
        self.pressure_control.current_pressure()
        
    def vacuum_air_and_fill_inert_gas(self,
                                      final_pressure = 120, vacuum_time=1):
        
        self.print_cell_pressure()
        self.pressure_control.close_all()
        self.pressure_control.to_ambient()
        self.pressure_control.vacuum(vacuum_time)
        self.print_cell_pressure()
        
        vacuum_pressure = self.pressure_control.current_pressure()
        #5 is an arbitrary low number and can be changed as needed
        if vacuum_pressure < 5:
            self.fill_with_inert()
        else:
            print("Vacuum not established!!!")
            print("Current Pressure: "+vacuum_pressure)
            
        print("Final Pressure")
        self.print_cell_pressure()
        
    def fill_with_inert(self):
        self.pressure_control.quick_fill()
        self.pressure_control.close_all()
        #iterate through to get to 120psi
        for i in range(5): self.pressure_control.gopr(120) 
        
    def move_stage_to_coordinates(self,x,y,z):
        self._XPS.move_stage('XYZ.X',x)
        self._XPS.move_stage('XYZ.Y',y)
        self._XPS.move_stage('XYZ.Z',z)
#        print("Stage moved to:\nx={}\ny={}\nz={}"\
#              .format(x,y,z))
        
    def flip_up_mirror(self):
        mirror("on")
        
    def flip_down_mirror(self):
        mirror("down")
        
        
#%%
class RamanSpectrometer:
    def __init__(self, XPS=xps):
        self._XPS = XPS
        
    def initialize_LightField(self):
        IsoPlane.capture_photo("start",2,1,0) #launch LightField software
    
#%%     
class LaserSystem:      
    def __init__(self):
		#Connect to laser
        self._laser = Sprout('COM4')
        self._laser.adapter.connection.baud_rate = 19200
        self._laser.adapter.connection.read_termination = '\r'
        self._laser.adapter.connection.write_termination = '\r'
        self._laser.write("OPMODE=On")
        
    def power_on_laser(self):
        self._laser.write("OPMODE=On")

    def power_off_laser(self):    
        self._laser.write("OPMODE=Off")
        
    def set_laserpower(self, laserpower=0.01):
		#Units of watts
        self._laser.power= laserpower
        
    
    
    
    
    
    
    
    
    
    


    