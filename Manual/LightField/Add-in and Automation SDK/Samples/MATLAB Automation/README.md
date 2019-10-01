# LightField-in-MATLAB
---
A simple library for automating Lightfield from Princeton Instruments using MATLAB.

## Usage

Setup_LightField_Environment.m is a script to prepare the environment with all of the proper .NET assemblies for automation. lfm.m contains the lfm class which handles automation of LightField. Multiple instances of LightField are allowed.

```
lfm class:
	Properties (public):
		automation;
        	addinbase;
        	application;
        	experiment;
	Methods:
		lfm(visible); 			The constructor of the class. Set visible to true or false if you want LightField visible.
		close();				Closes the instance of LightField.
		get(setting);			Gets the current value of 'setting' from LightField.
		set(setting, value); 	Sets 'setting' to value 'value'.
		load_experiment(value);	Loads an experiment.
		set_exposure(value);	Sets the exposure time in msec.
		set_frames(value);		Sets the number of frames.
		acquire();				Equivalent of pressing the acquire button in LightField. Return type depends on how many ROIs are configured.*
```		
*If there is more than one ROI configured, then MATLAB will return a cell array corresponding to each ROI. If not, then it will simply return a 3-dimensional array (x,y,f).

See the LightField automation manual for a list of possible settings.

A simple example, wherein the instance of the LightField-in-MATLAB automation class, lfm, is named lfi:		
```
Setup_LightField_Environment();       	Loads .NET automation assemblies
lfi = lfm(true);						Starts LightField and sets objects as properties
data = lfi.acquire();					Acquires and sends data to MATLAB
pcolor(data); shading interp;			Plots image data
lfi.close();							Closes LightField
```
## Revision History	
#### 3/1/2015
- Initial release of proof of concept library. 
- IExperiment set/get support implemented 
- Parsing of ImageDataSet object provided in acquire method.
