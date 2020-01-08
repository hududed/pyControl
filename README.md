## pyControl

### Abstract

The primary aim is to develop a program to allow the user design the experiment and the run the process independently. The program should be divided into four main parts:

1.	Setup surrogate model, initiate moving the XYZ stage
2.	Setting laser parameters for patterning
3.	Acquiring Raman Data
4.	Raman Data Analysis and export
5.  Update surrogate model, predict new point

## Instruments:
1. Newport ESP300 XYZ controller  
2. Thorlabs MFF101 Flip Mirror  
3. Lighthouse Photonics Sprout G12W Laser  
4. Princeton Instruments Isoplane SCT320 Raman

**Current Challenge**

1. Find the exact coordinates of GO(Graphene Oxide), Quartz, Kapton.
2. Calibrate the Laser power and monitor if patterning is done properly or not.
3. Run experiments on many points of a sample to monitor time-out issues from ESP 300 (motion controller) and solve them if it shows up.



## Completed Works
 ........................................................................................................................
## Details
### Part 0 (OK)
TO-DO:  
User should define parameter set i.e. how many parameters, type of parameters (continuous or discrete) and limits [F1].  
User should define size of initial dataset, and dataset is randomly sampled from parameter space [F1].  
Data written to ML-csv [F1].  
Build surrogate model using initial dataset R -> python code [F2].  
Move stage to set initial XYZ coordinate and run iterations subsequent dX or dY safe interval between spots/lines.  
F1: pyControl/Spectrometer Automation/initial experiment.py  
F2: pyControl/Spectrometer Automation/R2py_code.py  

### Part 1
Instrument: Newport ESP300 XYZ controller  
File: pyControl/site-packages/pymeasure/instruments/newport/ESP300.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: continuous stream reading  
Documentation: https://pymeasure.readthedocs.io/en/latest/api/instruments/newport/esp300.html  
               see also pyControl/Manual/

### Part 2 
Instrument: Thorlabs MFF101 Flip Mirror  
File: pyControl/site-packages/ftd2xx  
Lab:  
TO-DO: one-line ON/OFF function  
Documentation: https://github.com/qpit/thorlabs_apt/issues/3  

Instrument: Lighthouse Photonics Sprout G12W Laser (PRIORITY)  
File: pyControl/site-packages/pymeasure/instruments/lighthousephotonics/sprout.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: class function debugging in pymeasure instruments - overwriting problem, documentation for contribution   
Documentation: https://pymeasure.readthedocs.io/en/latest/tutorial/index.html  
               https://pymeasure.readthedocs.io/en/latest/dev/adding_instruments.html (proper contribution to pymeasure)  
               Contact also Lighthouse Photonics Service <service@lighthousephotonics.com>  

### Part 3 (PRIORITY)
TO-DO: extract raw data, spe files (DONE)  
       integrate flip mirror  
       integrate lasing controls  
       
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Spectrometer Automation/automation update 11-25-19.py  
Lab:  
Documentation: pyControl/Manual/LightField/Add-in and Automation SDK/  
               Contact LightField support recommended mailto:techsupport@princetoninstruments.com  

Instrument: Lighthouse Photonics Sprout G12W Laser  
File: pyControl/site-packages/pymeasure/instruments/lighthousephotonics/sprout.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: class function debugging in pymeasure instruments - overwriting problem  
Documentation: https://pymeasure.readthedocs.io/en/latest/tutorial/index.html  
               Contact also Lighthouse Photonics Service <service@lighthousephotonics.com>  

### Part 4
TO-DO: extract raw data, spe files (DONE)  
       fit data, export all as columns in a new line in ML-csv  
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Spectrometer Automation/automation update 11-25-19.py  
Fitting File: tba  
Lab:
Documentation: pyControl/Manual/LightField/Add-in and Automation SDK/  
               Contact LightField support recommended mailto:techsupport@princetoninstruments.com  

### Part 5
TO-DO: Export newline from ML-csv to update surrogate model  
       Export proposed configuration as newline to ML-csv  
       Read newline to control laser  
File: pyControl/Spectrometer Automation/R2py_code.py  
Docs: https://rpy2.readthedocs.io/en/version_2.8.x/  


## Model Files

Priority is given to Part 3 specfically reliable connection to Sprout Laser and Princeton Raman.
Model file is given in:

pyControl/codes/dash_flipper.py - example connection to Instruments 1-3
pyControl/codes/Table_test.py - example automation patterning matrix

The front-end GUI is using DashDAQ interface.
User Guide https://dash.plot.ly/dash-daq
Community Forum https://community.plot.ly/c/dash/dashdaq
