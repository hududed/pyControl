#!/usr/bin/env python
# coding: utf-8

# # Make directory

# In[1]:


import os, glob #import libraries
# os.mkdir(r'line stuff')
os.chdir(r'C:\Users\UWAdmin\line stuff') #change the directory to read/write to


# ## Import libraries

# In[2]:


import os 
os.getcwd() #get directory


# In[3]:


os.chdir(r'C:\Users\UWAdmin')
from threading import *
import time
from time import sleep
from datetime import datetime, timedelta

from random import randrange

from newportxps import NewportXPS

import numpy as np
import csv
        
from flipper import *
from spectra import * #import spectrometer codes


# In[4]:


xpsd_remoteip = '192.168.254.254' #xps ip address
# xpsd_hostip ='192.168.0.254' 
hostname = 'XPS-1b81' #login host name

xps = NewportXPS(xpsd_remoteip) #connecting to the xps
print(xps.status_report()) #get xps status

xps.kill_group('XYZ') #clear XYZ group
xps.initialize_allgroups() #initialize addressing
xps.home_allgroups() #send control plate to origin

def pos_all():
    for sname, _ in xps.stages.items():
        print('{}: {}'.format(sname, xps.get_stage_position(sname)))


# In[5]:


xps.kill_group('XYZ')
xps.initialize_allgroups()
xps.home_allgroups()

pos_all()


# In[9]:


#connecting Laser via modbus
from pymeasure.instruments.lighthousephotonics import Sprout
laser_power = Sprout('COM4')
laser_power.adapter.connection.baud_rate = 19200
laser_power.adapter.connection.read_termination = '\r'
laser_power.adapter.connection.write_termination = '\r'
laser_power.power=0.01


# In[10]:


#turns on laser (does the same thing as pressing the on button)
laser_power.write("OPMODE=On")


# # Launch the LightField / Spectrometer

# In[21]:


from spectra import * #import library for the raman
capture_photo("start",2,1,0) #launch LightField software


# # Vacuum the chamber

# In[22]:


from pressure import close_valve,open_valve,close_all,current_pressure,gopr, to_ambient, to_vacuum, quick_fill
from pymeasure.instruments.edwards import NXDS


# connect to NXDS vacuum pump
pump = NXDS('ASRL5::INSTR')

current_pressure() #check current pressure


# In[23]:


close_all() #close all valves
current_pressure() #check current pressure
# gopr(20)


# In[24]:


to_ambient() #open valve to atmosphere then close valve


# In[25]:


to_vacuum(t=1) # turns on vacuum pump for 1 minute


# In[26]:


current_pressure() # check pressure


# In[27]:


quick_fill() #fills chamber with innert gas (argon/nitrogen)


# In[28]:


close_all()#once done, close the vacuum

#you may want to check the pressure again

current_pressure()


# # Adjust the pressure

# In[29]:


for i in range(5): gopr(120) #iterate through to get to 120psi
current_pressure()


# In[30]:


current_pressure() #check that there's no leaks (run a few times)


# # Position the motion controller

# In[47]:


#pos_all() tells about current position of the motion controller
print('old coordinates')
pos_all()


xps.move_stage('XYZ.X',2) #moves x axis
xps.move_stage('XYZ.Y',9) #moves y axis
xps.move_stage('XYZ.Z',2.5) #moves z axis
print('')
print('new coordinates')
pos_all() #print position of new coordinates


# In[40]:


mirror("on") #flips up mirror (use when you want to get
#the spectra from LightField when focusing Z axis)


# In[41]:


mirror("off") #use when z has been focused


# # Control the laser power and switch on/off the mirror

# # Option 1: Prepare initial Data 

# # Option 2: customize your dataset

# # Adjust the z axis

# ## Define thread class

# In[42]:


class A2(Thread):
    def run(self):
        if d['ramptime'][0]<0.5:
            time.sleep(.5-d['ramptime'][0])
        print("motion controller started")
        xps.run_trajectory('foreward',) #Send initiation command for trajectory
        time.sleep(total_time)
        laser_power.power=0.01
        print("finished and current position is:\n")
        pos_all()

        
class B2(Thread):
    def run(self):
        for i in range(2):
           
            if i==0:
                if d['ramptime'][0]<0.5:
                    print("i: {}, mirror on".format(i))
                    start_time = time.monotonic()
                    mirror('on')
                    end_time = time.monotonic()
                    print("i: {}, {}".format(i,timedelta(seconds=end_time - start_time)))
                    time.sleep(d['ramptime'][1]) #time for linear line    
                else:
                    time.sleep(mirror_sleep)
                    print("mirror on")
                    start_time = time.monotonic()
                    mirror('on')
                    end_time = time.monotonic()
    #                 print("time to put the mirror on: ",start_time-end_time)
                    print("i: {}, {}".format(i,timedelta(seconds=end_time - start_time)))
                    time.sleep(d['ramptime'][1]) #time for linear line
            else:
                mirror('off')
                print("mirror off")


# ## Section (A) : Insert line number, parameters for the line and then define the line coordinate details

# In[48]:


os.chdir(r'C:\Users\UWAdmin\line stuff')
from fits import new_plot_LIG

#Please remember indexing begins from 0.

df=pd.read_csv('data.csv')
print("Enter Line Number: ")
#line_no=int(input())
line_no=1#int(input())

print("Enter your power, time, pressure for line number ", line_no)
powr,tm,pr=[650, 2000, 120]#input().split()

df.loc[line_no,'power']=powr
df.loc[line_no,'time']=tm
df.loc[line_no,'pressure']=pr

df.to_csv('data.csv',index=False)


power=[]
time=[]
pressure=[]
for i in range(9):
        power.append(powr)
        time.append(tm)
        pressure.append(pr)

row=['power','time','pressure','ratio']
with open('dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if line_no==0:writer.writerow(row)
        writer.writerows(zip(power,time,pressure))

        
with open('dataset-pre.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if line_no==0:writer.writerow(row)
        writer.writerows(zip(power,time,pressure))


# # Section (B) :

# In[49]:



print("Enter number of lines, starting point for x axis, y axis and step size for y axis:")


#lines,startx,starty,step_y= [x for x in input().split()]
lines,startx,starty,step_y = [1,2,9,1]
print(lines,startx,starty,step_y)
# move_y=[0 for i in range(int(lines))]

move_y=float(starty)

print("Lines will be made at following y axis:",move_y,"\n")


# Enter number of lines, starting point for x axis, y axis and step size for y axis:
# 4 4.2 7 .5

# # Section (C) :

# In[50]:


df2=pd.read_csv('data.csv')
print("Patterning is to be started\n")
import time
time.sleep(5)
cc=0
steps=0

for i in range(line_no,line_no+1):
    print("Line number: ",i) # row idx in data.csv
    line=i
    laser_power.power=0.01
    
    #move the axes to their start position
    xps.move_stage('XYZ.Y',move_y)
    pos_all()
    print("\n\n")
    df2=pd.read_csv('data.csv')
    time_of_file=df2['time'][i]
    #scantime=time_of_file/1000
    
    #define the trajectory
    length = 2 # Change number to alter line length (length is in mm)
    xps.define_line_trajectories(start=float(startx),
                             stop=float(startx)+length, 
                             step=0.01,
                             scantime=(time_of_file/1000),
                             axis='X') # Pos1
    
    print("\nCurrent time is:",time_of_file)
        
    pressure_of_file=df2['pressure'][i]
    for ip in range(5):gopr(pressure_of_file)

    print("\n Pressure is now : ",pressure_of_file,"\n")
    

    xps.download_trajectory('foreward.trj')
    import pandas as pd
    d = pd.read_csv('foreward.trj',header=None) # scantime 2 (see segment 1 or row1)
    d = d.loc[:, (d != 0).any(axis=0)]
    d.columns = ['ramptime','rampdist','rampvel']

    total_time=np.sum(d['ramptime'])
    mirror_sleep=d['ramptime'][0]-.5
    
    print(d)
    
    
    #power will be set to assigned value and make sure mirror is off and power is given enough time to reach it's value
    power_of_file=df2["power"][i]



    print("power is now:",power_of_file)

    xps.move_stage('XYZ.X',(float(startx)-d['rampdist'][0]))
    pos_all()
    time.sleep(15)
    print("\n\n")
    mirror("off")
    pp=power_of_file
    laser_power.power=((pp+21.167)/0.1013)/1000
    time.sleep(15)
    
    ##Draw Lines
    time.sleep(5)
    
    print("patterning!")
    import sys
    a=A2()
    b=B2()
    # stop_threads = False
    a.start()
    print('a started')
    b.start()
    print('b started')
    
    
    a.join()
    print('a joined')
    b.join()
    print('b joined')
    
    time.sleep(10)
    print("\n Line drawn - END\n")
    
    
    
    ##raman spectra analysis
    laser_power.power=0.01
    time.sleep(15)


# In[51]:


print("line drawn, post pattern starts")

# check=[(float(startx)+2),float(startx)+4,(float(startx)+6)]
length=2
check=[float(startx)+length/10*i for i in range(1,10)]

for kk in range(9):
    xps.move_stage('XYZ.X',check[kk])
    print(pos_all())

    for iii in range(1):
        mirror("on")
        #writing G/D of 3 spots in 3 lines inside dataset.csv
#         capture_photo("on",kk,line)
        print("post patterning...")
        GD=capture_photo("on",kk,line,iii)

        mirror("off")
        time.sleep(5)
        

 ### The following code saves spectra by reading the csv files. 
 ### For example: if current line number is 3, following codes will find the csvs that start 
 ###with " line 0 ..." and will save 
 ### raman spectra for all the files whose name starts with line 0        
        
import glob
import pandas as pd


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
    
print("done")


# In[103]:


laser_power.write("OPMODE=Off")


# In[40]:


laser_power.write("OPMODE=On")


# In[146]:


to_ambient()


# In[147]:


mirror("off")


# In[ ]:



# power_of_file=df2["power"][i]
ij=3
laser_power.power=0.01
power_of_file=380
print("power is now:",power_of_file)
xps.move_stage('XYZ.X',(float(startx)-d['rampdist'][0]))
pos_all()
time.sleep(15)
print("\n\n")
mirror("off")
a=power_of_file
laser_power.power=(0.5178*a-5.2215)/1000


# In[ ]:


In[135]


# In[ ]:


mirror("off")


# In[ ]:


pos_all()


# In[ ]:


mv=float(mv)
type(mv)


# In[ ]:


# rsum=robjects.r['sourin']
# rsum((1))
write_more()
repeats()


# In[ ]:


os.getcwd()


# In[ ]:


def write_more():
    d=pd.read_csv('data.csv')
    ln=d.shape[0]

    vpower=d['power'][ln-1]
    vtime=d['time'][ln-1]
    vpressure=d['pressure'][ln-1]

    d1=pd.read_csv('dataset.csv')
    ln=d1.shape[0]
    d1.loc[ln,"power"]=vpower
    d1.loc[ln,"time"]=vtime
    d1.loc[ln,"pressure"]=vpressure
    d1.to_csv('dataset.csv',index=False)
    d1.to_csv('dataset-pre.csv',index=False)


# In[ ]:


time_of_file=8554/1000
xps.define_line_trajectories(start=float(startx),
                             stop=float(startx)+2,
                             step=0.01,
                             scantime=time_of_file,
                             axis='X') # Pos1

xps.download_trajectory('foreward.trj')
import pandas as pd
d = pd.read_csv('foreward.trj',header=None) # scantime 2 (see segment 1 or row1)
d = d.loc[:, (d != 0).any(axis=0)]
d.columns = ['ramptime','rampdist','rampvel']

d


# In[ ]:


import glob
import pandas as pd
from fits import new_plot_LIG

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
    f=new_plot_LIG(d1,d2,_d1,_d2,ix,line_number)
    print(ix)
    fit.append(f)    

