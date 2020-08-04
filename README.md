## pyControl

### Abstract

The primary aim is to develop a program to allow the user design the experiment and the run the process independently. The program works in following fashion:
1.	Setting laser parameters for patterning
2.	Setup surrogate model, initiate moving the XYZ stage
3. Auto adjust z axis of motion controller for each spot.
4.	Start patterning.
5. Acquiring Raman Data.
6.	Raman Data Analysis and export.
7. Update surrogate model, predict new candidates.
8. Repeat process 2-7 until all the spots are patterned.
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
3. Run notebook `pyControl/Updated Codes/initial experiment.ipynb`, 
   (https://github.com/hududed/pyControl/blob/master/codes/initial%20experiment.ipynb) 
   and insert the parameters and their range.  
   --> Parameters will be written randomly as `results/dataset.csv`. (TO-DO: fixed paths)  
4. Run notebook `pyControl/Updated Codes/main program.ipynb`. 
   (https://github.com/hududed/pyControl/blob/master/codes/main%20program.ipynb)
5. Initialize IsoPlane Spectrometer. (TO-DO: Catch error so that main program doesn't run without this init)
6. Define `capture_photo` [Raman] and `ration` [fit code] (TO-DO: make as imports!)  
7. Update `path/to/dataset.csv` and parameter set for MBO in `rpy2objects.robjects` in main program cell.  
   (TO-DO: fixed folders and paths using example dataset)  
8. Run main program.  
9. Set start `(x1,y1)`, end coordinates `(x2,y2)` and intervals `(dx,dy)`.  
10. Following outputs are written to `results`: (TO-DO: fixed paths)  
    - Two Raw Raman spectrum files `foreground1D.csv` and `foreground2D.csv` for each pattern.  
    - One fit results `fit.csv` with each pattern as newline.  
    - One updated file for MBO `dataset.csv` with each pattern as newline,  
      containing `estimated` and `estimatedUpper` when MBO starts predictions.
