#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[52]:


import numpy as np
import glob



    
import matplotlib.pyplot as plt
# Import the .NET class library
import clr

# Import python sys module
import sys

# Import os module
import os

# Import System.IO for saving and opening files
from System.IO import *

# Import c compatible List and String
from System import String
from System.Threading import AutoResetEvent
from System.Collections.Generic import List
# from PrincetonInstruments.LightField.AddIns import CameraSettings

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


# In[ ]:


application= auto.LightFieldApplication
experiment = auto.LightFieldApplication.Experiment
file_manager=application.FileManager

def spectrometer(k):
    import csv
    import sys
    import pandas as pd
    if k==5:
#         import pandas as pd
     
       
#         import peakutils 

#         from scipy.optimize import curve_fit
        
       

#         def lorentzian_fcn(x, I, x0, gamma):
#             return I*((gamma**2)/(((x-x0)**2)+gamma**2))

#         def two_lorentzian(x, I1, x1, gamma1, I2, x2, gamma2, y0):
#             return lorentzian_fcn(x, I1, x1, gamma1) + lorentzian_fcn(x, I2, x2, gamma2) + y0
#         data = pd.read_csv("foreground 1D.csv")
#         bgr = pd.read_csv("background 1D.csv")
#         #print(data)
#         data_proc = (data.I.values - bgr.I.values)
#         #data_proc = (bgr.I.values)
#         data_index = data.index.values
#         data_proc = pd.DataFrame({'I': data_proc}, index = data_index)
#         data_proc = data_proc[1275:1750]

#         plt.plot(data_proc)
#         data_index = data_proc.index.values
#         lowval, hival = data_proc[data_proc.index.min():data_proc.index.min() + 50].values.mean(), data_proc[data_proc.index.max() - 50:data_proc.index.max()].values.mean()
#         low, hi = data_proc[data_proc.index.min():data_proc.index.min() + 50].index.values.mean(), data_proc[data_proc.index.max() - 50:data_proc.index.max()].index.values.mean()

#         y = [lowval, hival]
#         x = [low, hi]
#         m, b = np.polyfit(x, y, 1)

#         data_index = data_proc.index.values
#         data_proc = data_proc.I.values - (data_proc.index.values * m + b)
#         data_proc = pd.DataFrame({'I': data_proc}, index = data_index)

#         plt.plot(data_proc)
#         prms = [1000, 1345, 50, 3000, 1582, 25, 2000]   #prms = [I1, x1, gamma1, I2, x2, gamma2, y0]

#         #Optimal values for the prms are returned in array form via popt after lorentzian curve_fit 
#         popt, pcov = curve_fit(two_lorentzian, data_proc.index.values, data_proc.I.values, p0 = prms)

#         #Fit data is computed by passing optimal prms and x-values to two_lorentzian function
#         data_proc['fit'] = two_lorentzian(data_proc.index, *popt)

#         I_D = popt[0]
#         I_G = popt[3]
#         G = popt[4]
#         D = popt[1]
#         W_D = popt[2]
#         W_G = popt[5]

#         G_D_ratio = I_G/I_D
#         print("The G/D ratio is", G_D_ratio)
#         plt.plot(data_proc)
#         plt.plot(data_proc.fit)
#         plt.pause(0.001)
        def update_GD_ratio(p,G_D_ratio):
            df = pd.read_csv("2.csv")
            df.set_value(p, "Ratio", G_D_ratio)
            df.to_csv("2.csv", index=False)
            sys.exit()
        
        
        G_D_ratio =3.66
        print(G_D_ratio,"\n")
        print("It's experiment no.:")
        p=int(input())
        update_GD_ratio(p+1,G_D_ratio)
#         print("The G/D ratio is", G_D_ratio)
        
    else:
        if k==1:inn="background 1D"
        elif k==2:inn='background 2D'
        elif k==3:inn='foreground 1D'
        elif k==4:inn='foreground 2D'
        m=inn+ '.csv'
        application= auto.LightFieldApplication
        experiment = auto.LightFieldApplication.Experiment
        file_manager=application.FileManager
        def set_value(setting, value):    
            # Check for existence before setting
            # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    
            print("Experiment Completed")    
            # Sets the state of the event to signaled,
            # allowing one or more waiting threads to proceed.
            acquireCompleted.Set()

        import time

        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,3000)
            #print("Please Enter the Number of Frames")
            #y=int(input())
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,5)
            if k==1 or k==2:
                experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,550)
            elif k==3 or k==4:
                experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,350)
            _file_name = "case"

            # Pass location of saved file
            save_file(_file_name)

            # Acquire image
            experiment.Acquire()
            time.sleep(35)
            directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
            if( os.path.exists(directory)):        
                    print("\nFound the .spe file...")        

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
                print(".spe file not found...")

            print(String.Format("{0} {1}",
                                "Image saved to",
                                experiment.GetValue(
                                    ExperimentSettings.
                                    FileNameGenerationDirectory)))  


            wl= experiment.SystemColumnCalibration
            wavelength=np.zeros((1,1340))
            for i in range(1340):wavelength[0,i]=wl[i]
            print(intensity_frame)
            intensity=np.zeros((1,1340))
            for i in range(1340):
                x=0
                for j in range(n):
                    x=x+intensity_frame[j][i]
                x=x/n
                intensity[0,i]=x
            #print(intensity)
#             plt.plot(wavelength[0,:],intensity[0,:])
#             plt.xlabel("Wavelength")
#             plt.ylabel("Intensity")
#             plt.show()
            w=[]
            inten=[]
        
            for x in range(1340):
                w.append(wavelength[0,x])
                inten.append(intensity[0,x])
            import csv
            m=str(k)+ '.csv'

            with open(m, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["W", "I"])
                writer.writerows(zip(w,inten))

            acquireCompleted = AutoResetEvent(True)
            experiment.ExperimentCompleted -= experiment_completed

        if k==1:inn="background 1D"
        elif k==2:inn='background 2D'
        elif k==3:inn='foreground 1D'
        elif k==4:inn='foreground 2D'
        m=inn+ '.csv'
        
        with open(m, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["W", "I"])
            writer.writerows(zip(w,inten))
        k=int(input())
        return spectrometer(k)
spectrometer(1) 


# In[ ]:





# In[ ]:


application= auto.LightFieldApplication
experiment = auto.LightFieldApplication.Experiment
file_manager=application.FileManager
os.chdir("C:\\Users\\labuser")




import pandas as pd
#import numpy as np
#import sys
#import csv
#import os
def spectrometer(k,p):
    if k==5:
        m1="Experiment No."+str(p)+"Background 2D"+".csv"
        value=2.33
        datt1=pd.read_csv(m1)
        datt2=pd.read_csv(m1)
        datt3=pd.read_csv(m1)
        datt4=pd.read_csv(m1)
        os.chdir("C:\\Users\\labuser")
        df = pd.read_csv("2.csv")
        df.set_value(p+21, "Ratio", value)
        df.to_csv("ml-dataset.csv", index=False)
        print("Run More Experiments?\nType Yes to continue or No to terminate\n")
        scan=str(input())
        if scan=="Yes" or scan=="yes":
            print("Experiment",p+1," started\n")
            spectrometer(1,p+1)
        else:
            
            sys.exit() 
    else:
        
        
        if k==1:
            m="Experiment No."+ str(p)+"Background 1D"
            p1="Experiment" + str(p)
            os.makedirs(p1)
            os.chdir(p1)
        if k==2:
            m="Experiment No."+str(p)+"Background 2D"
            
        if k==3:
            m="Experiment No."+str(p)+"Foreground 1D"
        if k==4:
            m="Experiment No."+str(p)+"Foreground 2D"
        m=m+'.csv'
#         application= auto.LightFieldApplication
#         experiment = auto.LightFieldApplication.Experiment
#         file_manager=application.FileManager
        def set_value(setting, value):    
            # Check for existence before setting
            # gain, adc rate, or adc quality
            if experiment.Exists(setting):
                experiment.SetValue(setting, value)

        def experiment_completed(sender, event_args):    
            print("Experiment Completed")    
            # Sets the state of the event to signaled,
            # allowing one or more waiting threads to proceed.
            acquireCompleted.Set()

        import time

        # Check for device and inform user if one is needed
        if (device_found()==True): 
            experiment.ExperimentCompleted += experiment_completed 
            # Check this location for saved spe after running
            #print("Please Enter the Exposure Time:\n")
            #x=int(input())
            set_value(CameraSettings.ShutterTimingExposureTime,3000)
            #print("Please Enter the Number of Frames")
            #y=int(input())
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,5)
            if k==1 or k==2:
                experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,550)
            elif k==3 or k==4:
                experiment.SetValue(SpectrometerSettings.GratingCenterWavelength,350)
            _file_name = "case"

            # Pass location of saved file
            save_file(_file_name)

            # Acquire image
            experiment.Acquire()
            time.sleep(35)
            directory="C:\\Users\\labuser\\Desktop\\data\\Raman\\Vivek\\2019-10-08"
            if( os.path.exists(directory)):        
                    print("\nFound the .spe file...")        

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
                print(".spe file not found...")

            print(String.Format("{0} {1}",
                                "Image saved to",
                                experiment.GetValue(
                                    ExperimentSettings.
                                    FileNameGenerationDirectory)))  


            wl= experiment.SystemColumnCalibration
            wavelength=np.zeros((1,1340))
            for i in range(1340):wavelength[0,i]=wl[i]
            print(intensity_frame)
            intensity=np.zeros((1,1340))
            for i in range(1340):
                x=0
                for j in range(n):
                    x=x+intensity_frame[j][i]
                x=x/n
                intensity[0,i]=x
            #print(intensity)
#             plt.plot(wavelength[0,:],intensity[0,:])
#             plt.xlabel("Wavelength")
#             plt.ylabel("Intensity")
#             plt.show()
            w=[]
            inten=[]
        
            for x in range(1340):
                w.append(wavelength[0,x])
                inten.append(intensity[0,x])
            import csv
#         row=["A","B"]
#         with open(m, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(row)
#             writer.writerows(zip(w,inten))
            with open(m, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["W", "I"])
                writer.writerows(zip(w,inten))
#             k=int(input())
#             return spectrometer(k)
            print("Enter 2:Background 2D\nEnter 3:Foreground 1D\nEnter 4:Foreground 2D\nEnter 5: Exit or Start New Experiment")
            k=int(input())
            print("\n")
            return spectrometer(k,p)
print("Enter The Experiment Number:\n")
p=int(input())
spectrometer(1,p)


# In[ ]:


auto = Automation(True, List[String]())
application= auto.LightFieldApplication
experiment = auto.LightFieldApplication.Experiment
file_manager=application.FileManager


# In[ ]:




