## pyControl

### Abstract

The primary aim is to develop a program to allow the user design the experiment and the run the process independently. The program should be divided into four main parts:

1.	Moving the XYZ stage
2.	Setting laser parameters for patterning
3.	Acquiring Raman Data
4.	Raman Data Analysis and export

## Instruments:
1. Newport ESP300 XYZ controller  
2. Thorlabs MFF101 Flip Mirror  
3. Lighthouse Photonics Sprout G12W Laser  
4. Princeton Instruments Isoplane SCT320 Raman

## Completed Works
 ............................................
## Details
### Part 0
Edit user input table to automatically create patterning matrix coordinates.
Replace individual XYZ coordinate inputs with starting a single XYZ coordinate and subsequent dX or dY safe interval between spots.  
File: pyControl/codes/Table_test.py  
Documentation: https://dash.plot.ly/datatable

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
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Examples/Python Automation/synhcronous_acquisition  
Lab:  
TO-DO: extract raw data  
Documentation: pyControl/Manual/LightField/Add-in and Automation SDK/  
               Contact LightField support recommended mailto:techsupport@princetoninstruments.com


Instrument: Lighthouse Photonics Sprout G12W Laser  
File: pyControl/site-packages/pymeasure/instruments/lighthousephotonics/sprout.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: class function debugging in pymeasure instruments - overwriting problem  
Documentation: https://pymeasure.readthedocs.io/en/latest/tutorial/index.html  
               Contact also Lighthouse Photonics Service <service@lighthousephotonics.com>  

### Part 4 (soon)
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Examples/Python Automation/synhcronous_acquisition  
Fitting File: tba  
Lab:  
TO-DO: extract raw data  
Documentation: pyControl/Manual/LightField/Add-in and Automation SDK/  
               Contact LightField support recommended mailto:techsupport@princetoninstruments.com  


## Model Files

Priority is given to Part 3 specfically reliable connection to Sprout Laser and Princeton Raman.
Model file is given in:

pyControl/codes/dash_flipper.py - example connection to Instruments 1-3
pyControl/codes/Table_test.py - example automation patterning matrix

The front-end GUI is using DashDAQ interface.
User Guide https://dash.plot.ly/dash-daq
Community Forum https://community.plot.ly/c/dash/dashdaq
