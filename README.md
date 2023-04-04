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

The LRPC_Implementations folder is for rapid testing of different design panterns and parametric settings, which is it's distinction above pycontol. The LRPC Revisions are to be used for their 