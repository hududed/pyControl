#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import glob
import matplotlib.pyplot as plt
import clr
import sys
import os
from System.IO import *
from System import String
from System.Threading import AutoResetEvent
from System.Collections.Generic import List
# from fit_code2 import ration
# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import CameraSettings
from PrincetonInstruments.LightField.AddIns import ExperimentSettings
from PrincetonInstruments.LightField.AddIns import DeviceType
from PrincetonInstruments.LightField.AddIns import SpectrometerSettings

import time
    
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline
# %pylab inline


import pandas as pd # python data manipulation and analysis library
import numpy as np #  Library with large collection of high-level mathematical functions to operate on arrays
import matplotlib.pyplot as plt #python plotting library
import peakutils #baselining library

from scipy.optimize import curve_fit
import os,glob
 # Library with operating system dependent functionality. Example: Reading data from files on the computer

import csv
# from pathlib import *
import mplcursors

from sklearn import preprocessing

from lmfit import Parameters, minimize
from scipy import stats









def capture_photo(begin,exp_no,line,iii):
    global device_found
    global experiment
    global save_file
    global file_manager
    
    if begin=="start":
        def save_file(filename):    
        # Set the base file name
            experiment.SetValue(
                ExperimentSettings.FileNameGenerationBaseFileName,
                Path.GetFileName(filename))

            # Option to Increment, set to false will not increment
            experiment.SetValue(
                ExperimentSettings.FileNameGenerationAttachIncrement,
                True)

            # Option to add date
            experiment.SetValue(
                ExperimentSettings.FileNameGenerationAttachDate,
                True)

            # Option to add time
            experiment.SetValue(
                ExperimentSettings.FileNameGenerationAttachTime,
                True)
       
        def device_found():
            # Find connected device
            for device in experiment.ExperimentDevices:
                if (device.Type == DeviceType.Camera):
                    return True

            # If connected device is not a camera inform the user
            print("Camera not found. Please add a camera and try again.")
            return False  



        # Create the LightField Application (true for visible)
        # The 2nd parameter forces LF to load with no experiment 
        auto = Automation(True, List[String]())
        application= auto.LightFieldApplication
        experiment = auto.LightFieldApplication.Experiment
        file_manager=application.FileManager
        
    if begin=='adjust':
        def set_value(setting, value):    
        # Check for existence before setting
        # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    
#             print("Experiment Completed")    
            # Sets the state of the event to signaled,
            # allowing one or more waiting threads to proceed.
            acquireCompleted.Set()
       
        from flipper import mirror
        mirror('on')
        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,1000)
            #print("Please Enter the Number of Frames")
            #y=int(input())
            n=3
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,n)
            for k in range(1,2):
                if k==1:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,578.1351880026082)
                elif k==2:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,621.2340604418703)
               
                _file_name = "case"

                # Pass location of saved file
                save_file(_file_name)

                # Acquire image
                experiment.Acquire()
                time.sleep(5)
                #directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
                directory="C:\\Users\\UWAdmin\\Desktop\\AIM-Lab-Automation-master\\AIM-Lab-Automation-master\\spes"
                if( os.path.exists(directory)):        
#                         print("\nFound the .spe file...")        
                        print(" ")
                        # Returns all .spe files
                        files = glob.glob(directory +'/*.spe')

                        # Returns recently acquired .spe file
                        last_image_acquired = max(files, key=os.path.getctime)

                        try:
                            # Open file
                            file_name = file_manager.OpenFile(last_image_acquired, FileAccess.Read)

                            # Access image
                            file=file_name
                            imageData = file.GetFrame(0,0)
                            #here is a problem 11-18-2019
                            
                            intensity_frame=np.zeros((n,1340))
                            # Get image data
                            buffer = imageData.GetData()
                            #buffer=imageData.GetDataBuffer()
                            # Print first 10 pixel intensities
                            for i in range(0,n):
                                imageData=file.GetFrame(0,i)
                                buffer=imageData.GetData()
                                for pixel in range(0,1340):
                                    intensity_frame[i][pixel]=buffer[pixel]

                            file_name.Dispose()


                        except IOError:
                            print ("Error: can not find file or read data")

                else:
#                     print(".spe file not found...")
                    print(" ")

#                 print(String.Format("{0} {1}",
#                                     "Image saved to",
#                                     experiment.GetValue(
#                                         ExperimentSettings.
#                                         FileNameGenerationDirectory)))  

                mirror('off')
                wl= experiment.SystemColumnCalibration
                wavelength=np.zeros((1,1340))
                for i in range(1340):wavelength[0,i]=wl[i]
                #print(intensity_frame)
                intensity=np.zeros((1,1340))
                for i in range(1340):
                    x=0
                    for j in range(n):
                        x=x+intensity_frame[j][i]
                    x=x/n
                    intensity[0,i]=x
                    check_intensity=x

                w=[]
                inten=[]

                for x in range(1340):
                    wavelength[0,x]=1e7*(1/532 - 1/wavelength[0,x])
                    w.append(wavelength[0,x])
                    inten.append(intensity[0,x])
                import csv

                ix=np.max(inten)
                return ix
    if begin=="bg":
        def set_value(setting, value):    
        # Check for existence before setting
        # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    
#             print("Experiment Completed")    
            # Sets the state of the event to signaled,
            # allowing one or more waiting threads to proceed.
            acquireCompleted.Set()
       

        
        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,3000)
            #print("Please Enter the Number of Frames")
            #y=int(input())
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,10)
            for k in range(1,3):
                if k==1:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,578.1351880026082)
                elif k==2:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,621.2340604418703)
               
                _file_name = "case"

                # Pass location of saved file
                save_file(_file_name)

                # Acquire image
                experiment.Acquire()
                time.sleep(35)
                #directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
                directory="C:\\Users\\UWAdmin\\Desktop\\AIM-Lab-Automation-master\\AIM-Lab-Automation-master\\spes"
                if( os.path.exists(directory)):        
#                         print("\nFound the .spe file...")        
                        print(" ")
                        # Returns all .spe files
                        files = glob.glob(directory +'/*.spe')

                        # Returns recently acquired .spe file
                        last_image_acquired = max(files, key=os.path.getctime)

                        try:
                            # Open file
                            file_name = file_manager.OpenFile(
                                last_image_acquired, FileAccess.Read)

                            # Access image
                            file=file_name
                            imageData = file.GetFrame(0,0)
                            #here is a problem 11-18-2019
                            n=5
                            intensity_frame=np.zeros((n,1340))
                            # Get image data
                            buffer = imageData.GetData()
                            #buffer=imageData.GetDataBuffer()
                            # Print first 10 pixel intensities
                            for i in range(0,n):
                                imageData=file.GetFrame(0,i)
                                buffer=imageData.GetData()
                                for pixel in range(0,1340):
                                    intensity_frame[i][pixel]=buffer[pixel]

                            file_name.Dispose()


                        except IOError:
                            print ("Error: can not find file or read data")

                else:
#                     print(".spe file not found...")
                  print(" ")

#                 print(String.Format("{0} {1}",
#                                     "Image saved to",
#                                     experiment.GetValue(
#                                         ExperimentSettings.
#                                         FileNameGenerationDirectory)))  


                wl= experiment.SystemColumnCalibration
                wavelength=np.zeros((1,1340))
                for i in range(1340):wavelength[0,i]=wl[i]
                #print(intensity_frame)
                intensity=np.zeros((1,1340))
                for i in range(1340):
                    x=0
                    for j in range(n):
                        x=x+intensity_frame[j][i]
                    x=x/n
                    intensity[0,i]=x
                    check_intensity=x

                w=[]
                inten=[]

                for x in range(1340):
                    wavelength[0,x]=1e7*(1/532 - 1/wavelength[0,x])
                    w.append(wavelength[0,x])
                    inten.append(intensity[0,x])
                import csv
          
                m="background"+str(k)+"D.csv"
                with open(m, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["W", "I"])
                    writer.writerows(zip(w,inten))

        
    if begin=="on":
        def set_value(setting, value):    
        # Check for existence before setting
        # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    
#             print("Experiment Completed")    
            # Sets the state of the event to signaled,
            # allowing one or more waiting threads to proceed.
            acquireCompleted.Set()
       

        
        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,3000)
            #print("Please Enter the Number of Frames")
            #y=int(input())
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,10)
            for k in range(1,3):
                if k==1:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,578.1351880026082)
                elif k==2:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,621.2340604418703)
               
                _file_name = "case"

                # Pass location of saved file
                save_file(_file_name)

                # Acquire image
                experiment.Acquire()
                time.sleep(35)
                #directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
                directory="C:\\Users\\UWAdmin\\Desktop\\AIM-Lab-Automation-master\\AIM-Lab-Automation-master\\spes"
                if( os.path.exists(directory)): 
#                         print("\nFound the .spe file...")        
                        print(" ")
                        # Returns all .spe files
                        files = glob.glob(directory +'/*.spe')

                        # Returns recently acquired .spe file
                        last_image_acquired = max(files, key=os.path.getctime)

                        try:
                            # Open file
                            file_name = file_manager.OpenFile(
                                last_image_acquired, FileAccess.Read)

                            # Access image
                            file=file_name
                            imageData = file.GetFrame(0,0)
                            #here is a problem 11-18-2019
                            n=10
                            intensity_frame=np.zeros((n,1340))
                            # Get image data
                            buffer = imageData.GetData()
                            #buffer=imageData.GetDataBuffer()
                            # Print first 10 pixel intensities
                            for i in range(0,n):
                                imageData=file.GetFrame(0,i)
                                buffer=imageData.GetData()
                                for pixel in range(0,1340):
                                    intensity_frame[i][pixel]=buffer[pixel]

                            file_name.Dispose()


                        except IOError:
                            print ("Error: can not find file or read data")

                else:
#                     print(".spe file not found...")
                  print(" ")


                wl= experiment.SystemColumnCalibration
                wavelength=np.zeros((1,1340))
                for i in range(1340):wavelength[0,i]=wl[i]
                #print(intensity_frame)
                intensity=np.zeros((1,1340))
                for i in range(1340):
                    x=0
                    for j in range(n):
                        x=x+intensity_frame[j][i]
                    x=x/n
                    intensity[0,i]=x
                    check_intensity=x

                w=[]
                inten=[]

                for x in range(1340):
                    wavelength[0,x]=1e7*(1/532 - 1/wavelength[0,x])
                    w.append(wavelength[0,x])
                    inten.append(intensity[0,x])
                import csv
          
                m="line "+ str(line)+" Point "+str(exp_no)+" iteration "+str(iii)+" foreground"+str(k)+"D.csv"
                with open(m, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["W", "I"])
                    writer.writerows(zip(w,inten))

                 
        if check_intensity>=40e3:
            print("experiment: ",exp_no, ":Patterning not done")
        #,twoGD,twoD,G,WD,WG
        elif check_intensity<40e3:
            gdr=ration(1,2,exp_no,line,iii)
            return gdr
    if begin=="first":
        def set_value(setting, value):    
        # Check for existence before setting
        # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    

            acquireCompleted.Set()
       

        
        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,3000)
            #print("Please Enter the Number of Frames")
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,5)
            for k in range(1,3):
                if k==1:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,578.1351880026082)
                elif k==2:
                    experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,621.2340604418703)
                
                _file_name = "case"

                # Pass location of saved file
                save_file(_file_name)

                # Acquire image
                experiment.Acquire()
                time.sleep(25)
                #directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
                directory="C:\\Users\\UWAdmin\\Desktop\\AIM-Lab-Automation-master\\AIM-Lab-Automation-master\\spes"
                if( os.path.exists(directory)):        
#                         print("\nFound the .spe file...")        
                        print(" ")
                        # Returns all .spe files
                        files = glob.glob(directory +'/*.spe')

                        # Returns recently acquired .spe file
                        last_image_acquired = max(files, key=os.path.getctime)

                        try:
                            # Open file
                            file_name = file_manager.OpenFile(
                                last_image_acquired, FileAccess.Read)

                            # Access image
                            file=file_name
                            imageData = file.GetFrame(0,0)
                            #here is a problem 11-18-2019
                            n=5
                            intensity_frame=np.zeros((n,1340))
                            # Get image data
                            buffer = imageData.GetData()
                            #buffer=imageData.GetDataBuffer()
                            # Print first 10 pixel intensities
                            for i in range(0,n):
                                imageData=file.GetFrame(0,i)
                                buffer=imageData.GetData()
                                for pixel in range(0,1340):
                                    intensity_frame[i][pixel]=buffer[pixel]

                            file_name.Dispose()


                        except IOError:
                            print ("Error: can not find file or read data")

                else:
#                     print(".spe file not found...")
                  print(" ")


                wl= experiment.SystemColumnCalibration
                wavelength=np.zeros((1,1340))
                for i in range(1340):wavelength[0,i]=wl[i]
                #print(intensity_frame)
                intensity=np.zeros((1,1340))
                for i in range(1340):
                    x=0
                    for j in range(n):
                        x=x+intensity_frame[j][i]
                    x=x/n
                    intensity[0,i]=x
                    check_intensity=x

                w=[]
                inten=[]

                for x in range(1340):
                    wavelength[0,x]=1e7*(1/532 - 1/wavelength[0,x])
                    w.append(wavelength[0,x])
                    inten.append(intensity[0,x])
                import csv
                m="line "+ str(line)+" Before Point "+str(exp_no)+" iteration "+str(iii)+" foreground"+str(k)+"D.csv"
                with open(m, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["W", "I"])
                    writer.writerows(zip(w,inten))
        
                 
        gd=ration2(1,2,exp_no,line,iii)
   
        return gd
        
            

def ration(a,b,i,line,iii):
    
   
   
    """Plots LIG BEFORE PATTERN and get saves fits as fits.csv
    Plots currently saved manually.
    TO-DO: save each plot directly from this function
    d1: GD
    d2: 2D
    _d1: background GD
    _d2: background 2D
    """
  
   

    counter=i
    
    fit=[]

    d1 = pd.read_csv("line "+str(line)+" Point "+str(counter)+" iteration "+str(iii)+" foreground1D.csv")
    d2 = pd.read_csv("line "+str(line)+" Point "+str(counter)+" iteration "+str(iii)+" foreground2D.csv")
    _d1 = pd.read_csv("background1D.csv")
    _d2 = pd.read_csv("background2D.csv")
    

    
    # d1 = pd.read_csv(fn1)
    d1 = d1
    # d1_ = pd.read_csv(bg1)
    d1_= _d1
    d1['I'] = d1['I']-d1_['I']
    base1 = peakutils.baseline(d1['I'], 1)
    d1['I_base']= d1['I']-base1
    d1 = d1[(d1['W']>1220) & (d1['W']<1750)]

    # d2 = pd.read_csv(fn2)
    d2 = d2
    # d2_ = pd.read_csv(bg2)
    d2_= _d2
    d2['I'] = d2['I']-d2_['I']
    d2 = d2[(d2['W']>2550) & (d2['W']<2850)]
    d2= d2[(np.abs(stats.zscore(d2))<3).all(axis=1)]
    base2 = peakutils.baseline(d2['I'], 1)
    d2['I_base'] = d2['I']-base2
    

    def PseudoVoigtFunction(WavNr, Pos, Amp, GammaL, FracL):
        SigmaG = GammaL / np.sqrt(2*np.log(2)) # Calculate the sigma parameter  for the Gaussian distribution from GammaL (coupled in Pseudo-Voigt)
        LorentzPart = Amp * (GammaL**2 / ((WavNr - Pos)**2 + GammaL**2)) # Lorentzian distribution
        GaussPart = Amp * np.exp( -((WavNr - Pos)/SigmaG)**2) # Gaussian distribution
        Fit = FracL * LorentzPart + (1 - FracL) * GaussPart # Linear combination of the two parts (or distributions)
        return Fit

    def one_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a3 = pars['a3'].value
        c3 = pars['c3'].value
        s3 = pars['s3'].value
        f3 = pars['f3'].value

        peak1 = PseudoVoigtFunction(x.astype(float),c3, a3, s3, f3)

        model =  peak1  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated

    def three_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a1 = pars['a1'].value
        c1 = pars['c1'].value
        s1 = pars['s1'].value
        f1 = pars['f1'].value
        
        a4 = pars['a4'].value
        c4 = pars['c4'].value
        s4 = pars['s4'].value
        f4 = pars['f4'].value
        
        a2 = pars['a2'].value
        c2 = pars['c2'].value
        s2 = pars['s2'].value
        f2 = pars['f2'].value
        

        peak1 = PseudoVoigtFunction(x.astype(float), c1, a1, s1, f1)
        peak3 = PseudoVoigtFunction(x.astype(float), c4, a4, s4, f4)
        peak2 = PseudoVoigtFunction(x.astype(float), c2, a2, s2, f2)

        model =  peak1 + peak3 + peak2  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1, peak3, peak2
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated


    ps1 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps1.add_many(('a1',    1 ,   True,     0, None,  None),
                 ('c1',   1350,   True,  1330, 1370,  None),
                 ('s1',     20,   True,    10,   200,  None),  # 200 so that we get proper fit width of unpatterned peak 
                 ('f1',    0.5,   True,  0, 1,  None),
                 ('a4',    1 ,   True,     0, None,  None), # peak middle of GD
                 ('c4',   1500,   True,  1480, 1520,  None),
                 ('s4',     20,   True,    10,   200,  None),  
                 ('f4',    0.5,   True,  0, 1,  None),
                 ('a2',      1,   True,     0, None,  None),
                 ('c2',    1600,   True, 1560,  1640,  None),
                 ('s2',     20,   True,    10,   200,  None),
                 ('f2',    0.5,   True,  0, 1,  None))

    ps2 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps2.add_many(('a3',      1,   True,     0, None,  None),
                 ('c3',    2700,   True, 2650,  2750,  None),
                 ('s3',     20,   True,    10,   200,  None),
                 ('f3',    0.5,   True,  0, 1,  None))



    x = d1['W']
    y = d1['I_base']
    out = minimize(three_pv, ps1, method = 'leastsq', args=(x, y))

    x2 = d2['W']
    y2 = d2['I_base']
    out2 = minimize(one_pv, ps2, method = 'leastsq', args=(x2, y2))



    df1 = pd.DataFrame({key: [par.value] for key, par in out.params.items()})
    df2 = pd.DataFrame({key: [par.value] for key, par in out2.params.items()})

    df = pd.concat([df1,df2],axis=1)

    if df['s1'].values > 300:
        df[['a1','c1','s1','f1']] = 0

    if df['s2'].values > 120:
        df[['a2','c2','s2','f2']] = 0

    if df['s3'].values > 120:
        df[['a3','c3','s3','f3']] = 0
        
    df.columns= ['D','PD','WD','FD','D1','PD1','WD1','FD1','G','PG','WG','FG','2D','P2D','W2D','F2D']
   
    df['GD']=df['G']/df['D']
    df['2DG']=df['2D']/df['G']

#     df.to_csv('fits.csv',mode = 'a',index=False)
#     print (df)
    se=[df['D'].values[0],df['PD'].values[0],df['WD'].values[0],df['FD'].values[0],df['D1'].values[0],\
        df['PD1'].values[0],df['WD1'].values[0],df['FD1'].values[0],df['G'].values[0],\
       df['PG'].values[0],df['WG'].values[0],df['FG'].values[0],df['2D'].values[0],\
        df['P2D'].values[0],df['W2D'].values[0],df['F2D'].values[0]]
    

   
    if df['WD'].values>120:
        if (df['D'].values>.3*df['G'].values or df['D1'].values > df['D'].values):
            print("patterning not done")
    elif (df['WG'].values>120):
        print("patterning not done")
        df3=pd.read_csv('dataset.csv')
        df3['ratio'].replace(' ',np.nan, inplace=True)
        df4=df3.dropna(subset=["ratio"])
        a=df4['ratio'].shape
        df3.loc[a[0],'ratio']=0
        df3.to_csv('dataset.csv',index=False)
    
    
    elif np.mean(d1[d1['W']<1255]['I_base']) > 0.7*np.mean(d1[(d1['W']>1340) & (d1['W']<1350)]['I_base'])\
        or np.mean(d1[(d1['W']>1400) & (d1['W']<1550)]['I_base']) > 0.7*np.mean(d1[(d1['W']>1340) & (d1['W']<1350)]['I_base']):
        print("patterning not done")
    
    else:

        df3=pd.read_csv('dataset.csv')
        df3['ratio'].replace(' ',np.nan, inplace=True)
        df4=df3.dropna(subset=["ratio"])
        a=df4['ratio'].shape
        df3.loc[a[0],'ratio']=df['GD'].values[0]
        df3.to_csv('dataset.csv',index=False)
    return df['GD'].values[0] 

def ration2(m1,m2,counter,line,iii):
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().run_line_magic('pylab', 'inline')


    from matplotlib.ticker import MultipleLocator
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().run_line_magic('pylab', 'inline')
    import sys
    from lmfit import Parameters, minimize
    import pandas as pd # python data manipulation and analysis library
    import numpy as np #  Library with large collection of high-level mathematical functions to operate on arrays
    import matplotlib.pyplot as plt #python plotting library
    import peakutils #baselining library

    import os, glob, csv
 # Library with operating system dependent functionality. Example: Reading data from files on the computer
    bg1=pd.read_csv("background1D.csv")
    bg2=pd.read_csv("background2D.csv")

    d1=pd.read_csv("line "+ str(line)+" Before Point "+str(counter)+" iteration "+str(iii)+" foreground1D.csv")
    d2=pd.read_csv("line "+ str(line)+" Before Point "+str(counter)+" iteration "+str(iii)+" foreground2D.csv")
    _d1 = pd.read_csv("background1D.csv")
    _d2 = pd.read_csv("background2D.csv")
    
    
    
    d1 = d1
    # d1_ = pd.read_csv(bg1)
    d1_= _d1
    d1['I'] = d1['I']-d1_['I']
    base1 = peakutils.baseline(d1['I'], 1)
    d1['I_base']= d1['I']-base1
    d1 = d1[(d1['W']>1220) & (d1['W']<1750)]

    # d2 = pd.read_csv(fn2)
    d2 = d2
    # d2_ = pd.read_csv(bg2)
    d2_= _d2
    d2['I'] = d2['I']-d2_['I']
    d2 = d2[(d2['W']>2550) & (d2['W']<2850)]
    d2= d2[(np.abs(stats.zscore(d2))<3).all(axis=1)]
    base2 = peakutils.baseline(d2['I'], 1)
    d2['I_base'] = d2['I']-base2
    
    
    

    def PseudoVoigtFunction(WavNr, Pos, Amp, GammaL, FracL):
        SigmaG = GammaL / np.sqrt(2*np.log(2)) # Calculate the sigma parameter  for the Gaussian distribution from GammaL (coupled in Pseudo-Voigt)
        LorentzPart = Amp * (GammaL**2 / ((WavNr - Pos)**2 + GammaL**2)) # Lorentzian distribution
        GaussPart = Amp * np.exp( -((WavNr - Pos)/SigmaG)**2) # Gaussian distribution
        Fit = FracL * LorentzPart + (1 - FracL) * GaussPart # Linear combination of the two parts (or distributions)
        return Fit

    def one_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a3 = pars['a3'].value
        c3 = pars['c3'].value
        s3 = pars['s3'].value
        f3 = pars['f3'].value

        peak1 = PseudoVoigtFunction(x.astype(float),c3, a3, s3, f3)

        model =  peak1  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated

    def three_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a1 = pars['a1'].value
        c1 = pars['c1'].value
        s1 = pars['s1'].value
        f1 = pars['f1'].value
        
        a4 = pars['a4'].value
        c4 = pars['c4'].value
        s4 = pars['s4'].value
        f4 = pars['f4'].value
        
        a2 = pars['a2'].value
        c2 = pars['c2'].value
        s2 = pars['s2'].value
        f2 = pars['f2'].value
        

        peak1 = PseudoVoigtFunction(x.astype(float), c1, a1, s1, f1)
        peak3 = PseudoVoigtFunction(x.astype(float), c4, a4, s4, f4)
        peak2 = PseudoVoigtFunction(x.astype(float), c2, a2, s2, f2)

        model =  peak1 + peak3 + peak2  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1, peak3, peak2
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated


    ps1 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps1.add_many(('a1',    1 ,   True,     0, None,  None),
                 ('c1',   1350,   True,  1330, 1370,  None),
                 ('s1',     20,   True,    10,   200,  None),  # 200 so that we get proper fit width of unpatterned peak 
                 ('f1',    0.5,   True,  0, 1,  None),
                 ('a4',    1 ,   True,     0, None,  None), # peak middle of GD
                 ('c4',   1500,   True,  1480, 1520,  None),
                 ('s4',     20,   True,    10,   200,  None),  
                 ('f4',    0.5,   True,  0, 1,  None),
                 ('a2',      1,   True,     0, None,  None),
                 ('c2',    1600,   True, 1560,  1640,  None),
                 ('s2',     20,   True,    10,   200,  None),
                 ('f2',    0.5,   True,  0, 1,  None))

    ps2 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps2.add_many(('a3',      1,   True,     0, None,  None),
                 ('c3',    2700,   True, 2650,  2750,  None),
                 ('s3',     20,   True,    10,   200,  None),
                 ('f3',    0.5,   True,  0, 1,  None))



    x = d1['W']
    y = d1['I_base']
    out = minimize(three_pv, ps1, method = 'leastsq', args=(x, y))

    x2 = d2['W']
    y2 = d2['I_base']
    out2 = minimize(one_pv, ps2, method = 'leastsq', args=(x2, y2))



    df1 = pd.DataFrame({key: [par.value] for key, par in out.params.items()})
    df2 = pd.DataFrame({key: [par.value] for key, par in out2.params.items()})

    df = pd.concat([df1,df2],axis=1)

    if df['s1'].values > 300:
        df[['a1','c1','s1','f1']] = 0

    if df['s2'].values > 120:
        df[['a2','c2','s2','f2']] = 0

    if df['s3'].values > 120:
        df[['a3','c3','s3','f3']] = 0
        
    df.columns= ['D','PD','WD','FD','D1','PD1','WD1','FD1','G','PG','WG','FG','2D','P2D','W2D','F2D']
   
    df['GD']=df['G']/df['D']
    df['2DG']=df['2D']/df['G']


    se=[df['D'].values[0],df['PD'].values[0],df['WD'].values[0],df['FD'].values[0],df['D1'].values[0],\
        df['PD1'].values[0],df['WD1'].values[0],df['FD1'].values[0],df['G'].values[0],\
       df['PG'].values[0],df['WG'].values[0],df['FG'].values[0],df['2D'].values[0],\
        df['P2D'].values[0],df['W2D'].values[0],df['F2D'].values[0]]
    
  
    if df['WD'].values>120:
        if (df['D'].values>.3*df['G'].values or df['D1'].values > df['D'].values):
            print("patterning not done")
    elif (df['WG'].values>120):
        print("patterning not done")
        df3=pd.read_csv('dataset.csv')
        df3['ratio'].replace(' ',np.nan, inplace=True)
        df4=df3.dropna(subset=["ratio"])
        a=df4['ratio'].shape
        df3.loc[a[0],'ratio']=0
        df3.to_csv('dataset.csv',index=False)
    
    else:

    
        df3=pd.read_csv('dataset-pre.csv')
        df3['ratio'].replace(' ',np.nan, inplace=True)
        df4=df3.dropna(subset=["ratio"])
        a=df4['ratio'].shape
        df3.loc[a[0],'ratio']=df['GD'].values[0]
        df3.to_csv('dataset-pre.csv',index=False)
    return df['GD'].values[0] 

