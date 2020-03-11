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

1. Add Raman measurements pre-patterning to determine poorly deposited areas.

2. Update notebooks to python files.

3. Velocity control for line patterning.

## HOW-TO  
1. Git clone this repo to your local machine.  
2. Create a new virtual environment, activate it and install requirements.  
3. Run notebook `pyControl/Updated Codes/initial experiment.ipynb`,  
   and define number of training data and parameter set.  
   --> Parameters will be written randomly as `results/dataset.csv`. (TO-DO: fixed paths)  
4. Run notebook `pyControl/Updated Codes/main program.ipynb`  
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
