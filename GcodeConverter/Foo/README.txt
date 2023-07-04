gcodeconverter (v1.0)
author: Austin Barner
email: abarner@uwyo.edu
alt email: abarner99@gmail.com

***v1.0 notes***

- convert a .gcode file into a .trj file

- the program starts by converting all non-G1 movement commands (i.e. G2/G3 arc commands) into a list of "revised gcode" commands

	- all movement commands in the "revised gcode" are G1 commands (linear movement)

- the program allows for the modification of the target speed, the acceleration/deceleration rates, the start x position,
the start y position, the mode (either "abs" or "rel", for v1.0 only use "abs" which is the default), and the arc step (This value
determines the length, in mm, of each line when an arc is segmented.  The actual size will be <= the declared arc step length.)

- this will change in future versions, but for now, the program assumes that the first G1 command and the last G1 command in the 
revised gcode are a sufficient length to acceleration to the target speed and decelerate to 0.  Do not start or end gcode with arc
commands or extremely short g1 commands!

- the program will give the option to output the "revised gcode" either to the terminal or to a file.  I strongly recommend reviewing
the "revised gcode" with this website (https://nraynaud.github.io/webgcode/) or some other gcode viewer.  I think my math is correct,
but it is possible that mistakes exist.

- currently, it is assumed that all arcs are 180 degrees (specifically for the purposed of meandering patterns).  I will likely change
this in the future to allow for other arc angles.  If you input a command where the arc angle is NOT 180 degrees, the program will likely
crash or give an undesired output.

- if any errors are found, please email me at abarner@uwyo.edu - any and all relavent screenshots/notes/error messages/etc. will be 
greatly appreciated.  At a bare minimum, please include the input gcode that caused the error(s).   



***TODO***

- make the code involving the initial acceleration/deceleration more robust/flexible as described above

- allow for the user in input the input/output files in the console (currently, the files are declared at the very bottom of gcodeconverter.py 
when creating an instance of GcodeConverter()

- implement F command functionality (allows for the target speed to be changed in the gcode)

- integrate with mecode (https://github.com/jminardi/mecode) and newportxps (https://github.com/pyepics/newportxps)
    
    - currently, I have a modified version of mecode which can be used to create the meandering arc gcode.  See the file "mecode_modified/test1.py"

- implement a front-end  ¯\_(ツ)_/¯