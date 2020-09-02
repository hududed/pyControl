## pyControl

### Abstract

The primary aim is to develop a program to allow the user design the experiment and the run the process independently. The program works in following fashion:
1.	Setting laser parameters for patterning,
2.	Setup surrogate model, initiate moving the XYZ stage,
3. Auto adjust z axis of motion controller for each spot,
4.	Start patterning,
5. Acquiring Raman Data,
6.	Raman Data Analysis and export,
7. Update surrogate model, predict new candidates,
8. Repeat process 2-7 until all the spots are patterned,
9. Save the Optimizer model for post-analysis.

## Instruments:
1. Newport ESP300 XYZ controller  
2. Thorlabs MFF101 Flip Mirror  
3. Lighthouse Photonics Sprout G12W Laser  
4. Princeton Instruments Isoplane SCT320 Raman

**Current Challenge**

1. Update notebooks to python files.

2. Velocity control for line patterning.

## HOW-TO  
1. Git clone this repo to your local machine.  
2. Create a new virtual environment, activate it and install requirements.  
3.  Run notebook `pyControl/Updated Codes/main program.ipynb`. 
   (https://github.com/hududed/pyControl/blob/master/codes/main%20program.ipynb)
   -->Inside current directory, a new folder will be created as "Campaign " + "Current Date" . In this folder 
      experimental data will be recorded.
   --> Parameters will be written at `directory/campaign_current_date/dataset.csv`. (TO-DO: fixed paths)  
4. Imports pressure, IsoPlane Spectrometer, Motion Controller, Flipper Mirror and Laser files. 
5. Run main program.  
6. Set start `(x1,y1)`, end coordinates `(x2,y2)` and intervals `(dx,dy)`.  
7. Following outputs are written to `results`: (TO-DO: fixed paths)  
    - Background1D and Background2D csv files are created. The center wavelengths are 1500 and 2700. 
    - Two Raw Raman spectrum files `foreground1D.csv` and `foreground2D.csv` for each pattern.   
    - One updated file for MBO `dataset.csv` with each pattern as newline,  
    - the optimizer model opt.state.rds are saved at `directory/campaign_current_date/'
    - All the csv files for foreground and background 1D, 2D are saved at `directory/campaign_current_date/'.
     
