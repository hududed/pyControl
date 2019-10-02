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


### Part 1
Instrument: Newport ESP300 XYZ controller  
File: pyControl/site-packages/pymeasure/instruments/newport/ESP300.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: continuous stream reading  

### Part 2
Instrument: Thorlabs MFF101 Flip Mirror  
File: pyControl/site-packages/ftd2xx  
Lab:  
TO-DO: one-line ON/OFF function  

Instrument: Lighthouse Photonics Sprout G12W Laser
File: pyControl/site-packages/pymeasure/instruments/lighthousephotonics/sprout.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab: 
TO-DO: class function debugging in pymeasure instruments - overwriting problem

### Part 3
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Examples/Python Automation/synhcronous_acquisition  
Lab:  
TO-DO: extract raw data  

Instrument: Lighthouse Photonics Sprout G12W Laser  
File: pyControl/site-packages/pymeasure/instruments/lighthousephotonics/sprout.py  
Calls class: pyControl/site-packages/pymeasure/instruments/instrument.py  
Lab:  
TO-DO: class function debugging in pymeasure instruments - overwriting problem  

### Part 4 (soon)
Instrument: Princeton Instruments Isoplane SCT320 Raman  
File: pyControl/Examples/Python Automation/synhcronous_acquisition  
Fitting File: tba  
Lab:  
TO-DO: extract raw data  

