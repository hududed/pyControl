import math
import os
from os.path import exists
from typing import Callable, List, Tuple

import arcconverter
from config import GCODE_INPUT, TRJ_OUTPUT


def process_gcode_command(cmd: str, x: float, y: float, revised_gcode: List[str], arcstep: float, command_func: Callable[[str, float, float, float, float], Tuple[float, float]]) -> Tuple[float, float]:
    revised_gcode.append(cmd.rstrip())
    x, y = command_func(cmd, x, y, arcstep, revised_gcode)
    return x, y

def process_move_command(cmd: str, x: float, y: float, arcstep: float, revised_gcode: List[str]) -> Tuple[float, float]:
    for arg in cmd.split(" "):
        if arg[0] == 'X':
            x = float(arg[1:])
        elif arg[0] == 'Y':
            y = float(arg[1:])
    return x, y

def process_arc_command(cmd: str, x: float, y: float, arcstep: float, revised_gcode: List[str]) -> Tuple[float, float]:
    arc = arcconverter.ArcConverter(cmd, start_xpos=x, start_ypos=y, step_size=arcstep, mode='abs')
    for arc_cmd in arc.get_output_cmds():
        revised_gcode.append(arc_cmd.rstrip())
    for arg in cmd.split(" "):
        if arg[0] == 'X':
            x = float(arg[1:])
        elif arg[0] == 'Y':
            y = float(arg[1:])
    return x, y


class GCodeCommand:
    def __init__(self, cmd):
        self.cmd = cmd
        self.split_cmd = cmd.split(" ")
        self.cmd_type = self.split_cmd[0]
    
    def __str__(self):
        return self.cmd

    def is_move_command(self):
        return self.cmd_type in ['G0', 'G1', 'G2', 'G3']

    def is_arc_command(self):
        return self.cmd_type in ['G2', 'G3']

    def is_absolute_mode_command(self):
        return self.cmd_type.rstrip() == 'G90'

    def is_relative_mode_command(self):
        return self.cmd_type.rstrip() == 'G91'

    def get_move_params(self):
        x, y, i, j = 0, 0, 0, 0
        for arg in self.split_cmd:
            if arg[0] == 'X':
                x = float(arg[1:])
            elif arg[0] == 'Y':
                y = float(arg[1:])
            elif arg[0] == 'I':
                i = float(arg[1:])
            elif arg[0] == 'J':
                j = float(arg[1:])
        return x, y, i, j

    def to_abs_command(self, x, y, i, j):
        if self.is_arc_command():
            return '{0} X{1:0.6f} Y{2:0.6f} I{3:0.6f} J{4:0.6f}'.format(self.cmd_type, x, y, i, j)
        else:
            return '{0} X{1:0.6f} Y{2:0.6f}'.format(self.cmd_type, x, y)

class GcodeConverter:

    '''
    input:
        gcode_file: the directory of the .gcode file being read in
        trj_file: the directory of the .trj file being written to
        speed: (mm/sec) the target constant speed that the motors need to be 
            moving at after acceleration and before deceleration
        accel: (mm/sec^2) the rate of acceleraction/deceleration
        posx: (mm) the absolute position for the x-axis
        posy: (mm) the absolute position for the y-axis
        mode: indicates if the mode is absolute (abs) or relative (rel)
        arcstep: (mm) the target length of each step along the x-axis when drawing an arc
    
    variables:
        acceltime: the time needed to accelerate to the constant speed or
            decelerate to 0
        acceldist: the acceleration distance needed to travel before the constant speed 
            is reached and the deceleration distance needed to travel before reaching a 
            speed of 0
        currspeed: the current speed, this is used for acceleration/deceleration
            
    '''
    def __init__(self, gcode_file, trj_file, speed=5, accel=10, posx=0, posy=0, mode='abs', arcstep=0.05):
    
        self.gcode_file = gcode_file
        self.trj_file = trj_file
        self.speed = speed
        self.accel = accel
        
        self.gcode_cmds = self.read()
        self.posx = posx
        self.posy = posy
        
        if mode != 'rel' or mode != 'abs':
            self.mode = 'abs'
        else:
            self.mode = mode
        
        self.arcstep = arcstep
        
        self.acceltime = speed/accel
        self.acceldist = 0.5 * accel * math.pow(self.acceltime, 2)
        self.currspeed = 0
        
        self.revised_gcode = []

        self.convert_rel_to_abs(start_x=self.posx, start_y=self.posy)
        
        self.init_revised_gcode()
        

    '''
    append data to self.trj_file
    if the file does not exist, it is created
    '''
    def write(self, data):
    
        if data == 'null':
            return
        
        exists = os.path.exists(self.trj_file)
        
        if not exists:
            
            f = open(self.trj_file, "x")
            f.write(data + "\n")
            f.close()
        
        else:
        
            f = open(self.trj_file, "a")
            f.write(data + "\n")
            f.close()
    
    
    '''
    read the data from self.gcode_file
    '''
    def read(self):
        
        raw_cmds = []
        
        f = open(self.gcode_file, "r")
        
        for line in f:
            raw_cmds.append(line)
        
        return raw_cmds
    



    '''
    convert all gcode commands to g1 commands
    '''
    def init_revised_gcode(self):

        x = 0
        y = 0
        for cmd in self.gcode_cmds:
            split_cmd = cmd.split(" ")
            if split_cmd[0] == 'G1':
                command_func = process_move_command
            elif split_cmd[0] == 'G2' or split_cmd[0] == 'G3':
                command_func = process_arc_command
            else:
                self.revised_gcode.append(cmd.rstrip())
                continue
            x, y = process_gcode_command(cmd, x, y, self.revised_gcode, self.arcstep, command_func)
    
    def convert_rel_to_abs(self, start_x=0, start_y=0):
        curr_x = start_x
        curr_y = start_y
        index = 0
        is_rel = False
        for cmd in self.gcode_cmds:
            gcode_cmd = GCodeCommand(cmd)
            if gcode_cmd.is_move_command():
                x, y, i, j = gcode_cmd.get_move_params()
                if is_rel:
                    x += curr_x
                    y += curr_y
                self.gcode_cmds[index] = gcode_cmd.to_abs_command(x, y, i, j)
                curr_x = x
                curr_y = y
            elif gcode_cmd.is_absolute_mode_command():
                is_rel = False
            elif gcode_cmd.is_relative_mode_command():
                is_rel = True
                self.gcode_cmds[index] = GCodeCommand('G90').__str__()
            index += 1
                
    '''
    print out all revised gcode commands
    '''
    def print_revised_gcode(self):
        
        for cmd in self.revised_gcode:
            print(cmd)
        
        
    def init_conversion(self):
    
        #clear the contents of the .trj file
        f = open(self.trj_file, "w").close()
        
        firstmovementindex = -1
        lastmovementindex = -1
        count = 0
        for cmd in self.revised_gcode:
        
            if firstmovementindex == -1 and self.retrieve_cmd_code(cmd) == 'G1':
                firstmovementindex = count
            
            if self.retrieve_cmd_code(cmd) == 'G1':
                lastmovementindex = count
            count += 1
        
        if firstmovementindex == -1 or lastmovementindex == -1:
            print('No G1 command found, the first and last movements must be G1 commands for acceleration/deceleration')
            return
            
        if self.length_of_cmd(self.revised_gcode[firstmovementindex]) < self.acceldist:
            print('The length of the first G1 command must be >= the acceleration distance of: ', self.acceldist)
            return
            
        if self.length_of_cmd(self.revised_gcode[lastmovementindex]) < self.acceldist:
            print('The length of the last G1 command must be >= the acceleration distance of: ', self.acceldist)
            return
            
            
        #convert/execute all commands called before the first G1 command
        for i in range(firstmovementindex):
            self.interpret_cmd(self.revised_gcode[i])
        
        
        #convert the first G1 command
        totallength_0 = self.length_of_cmd(self.revised_gcode[firstmovementindex])
        endpos_0 = self.retrieve_g1_finalpos(self.revised_gcode[firstmovementindex])    #x = endpos[0], y = endpos[1]
        
        t_0 = self.acceldist/totallength_0
        
        x_t0 = (1 - t_0) * (self.posx) + (t_0 * endpos_0[0])
        y_t0 = (1 - t_0) * (self.posy) + (t_0 * endpos_0[1])
        
        changex_0 = x_t0 - self.posx
        changey_0 = y_t0 - self.posy

        velx_0 = (changex_0/self.acceldist)* self.acceltime * self.accel
        vely_0 = (changey_0/self.acceldist) * self.acceltime * self.accel
        
        self.write('{0:0.6f} {1:0.6f} {2:0.6f} {3:0.6f} {4:0.6f} {5:0.6f} {6:0.6f}'.format(self.acceltime, x_t0, velx_0, y_t0, vely_0, 0, 0))
        self.posx = x_t0
        self.posy = y_t0
        
        #if there is a remaining portion of the line after the acceleration, write the remainder at the constant speed
        if t_0 != 1:
            
            self.write(self.lineAtConstSpeed(self.posx, self.posy, endpos_0[0], endpos_0[1]))
            
            self.posx = endpos_0[0]
            self.posy = endpos_0[1]
        
        
        #convert/execute all commands called after the first G1 command, but before the final G1 command
        
        #return if all commands have been executed
        if len(self.revised_gcode) == firstmovementindex + 1:
            return
            
        for i in range(firstmovementindex + 1, lastmovementindex):
            self.interpret_cmd(self.revised_gcode[i])
        
        
        #convert the last G1 command
        totallength_1 = self.length_of_cmd(self.revised_gcode[lastmovementindex])
        endpos_1 = self.retrieve_g1_finalpos(self.revised_gcode[lastmovementindex])
        
        t_1 = self.acceldist/totallength_1
        
        x_t1 = (1 - t_1) * (self.posx) + (t_1 * endpos_1[0])
        y_t1 = (1 - t_1) * (self.posy) + (t_1 * endpos_1[1])
        
        
        if t_1 != 1:
            
            self.write(self.lineAtConstSpeed(self.posx, self.posy, x_t1, y_t1))
            
            self.posx = x_t1
            self.posy = y_t1
        
        self.write('{0:0.6f} {1:0.6f} {2:0.6f} {3:0.6f} {4:0.6f} {5:0.6f} {6:0.6f}'.format(self.acceltime, endpos_1[0], 0, endpos_1[1], 0, 0, 0))
        
        self.posx = endpos_1[0]
        self.posy = endpos_1[1]
        
        
        #convert/execute any commands called after the last G1 command
        
        #return if all commands have been executed
        if len(self.revised_gcode) == lastmovementindex + 1:
            return
            
        for i in range(lastmovementindex + 1, len(self.revised_gcode)):
            self.interpret_cmd(self.revised_gcode[i])
        
        
        #TODO implement the case where firstmovementindex == lastmovementindex and the command needs to be split into 3 commands instead of 2
    
    
    '''
    returns the total travel length of the gcode commands 
    '''
    def total_length(self):
        
        sum = 0
        
        for cmd in self.revised_gcode:
            sum = sum + float(self.length_of_cmd(cmd))
        
        return sum
    
    
    '''
    returns the travel length of a given gcode command
    '''    
    def length_of_cmd(self, cmd):
        
        cmd_s = cmd.split(" ")
        
        if cmd_s[0] == 'G0':#return 0, because a rapid linear motion shouldn't be counted towards the acceleration/deceleration
            return 0
            
        elif cmd_s[0] == 'G1':
            x = 0
            y = 0
        
            for arg in cmd_s:
            
                if arg[0] == 'X':
                    x = float(arg[1:])
                elif arg[0] == 'Y':
                    y = float(arg[1:])
            
            return self.distance(self.posx, self.posy, x, y)
            
        elif cmd_s[0] == 'G2':#clockwise arc
            return self.arc_length(float(cmd_s[1][1:]), float(cmd_s[2][1:]), float(cmd_s[3][1:]), float(cmd_s[4][1:]))
            
        elif cmd_s[0] == 'G3':#counter-clockwise arc
            return self.arc_length(float(cmd_s[1][1:]), float(cmd_s[2][1:]), float(cmd_s[3][1:]), float(cmd_s[4][1:]), dir='ccw')
            
        elif cmd_s[0] == 'G28':
            return self.distance(self.posx, self.posy, 0, 0)
            
        elif cmd_s[0] == 'G90':
            return 0
            
        elif cmd_s[0] == 'G91':
            return 0
            
        else:
            print('Invalid gcode command!  Cannot interpret: ' + cmd)
            return 0
        
            
    '''
    returns the length of an arc
    '''
    def arc_length(self, x0, y0, centerx, centery, dir='cw'):
        
        a = self.distance(x0, y0, centerx, centery)
        b = self.distance(self.posx, self.posy, centerx, centery)
        c = self.distance(x0, y0, self.posx, self.posy)
        
        num = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
        den = 2 * a * b
        if den == 0:
            return 0
        div = num / den
        div *= -1
        
        rad = math.acos(div)
        if dir == 'cw':
            rad = (2 * math.pi) - rad
        
        return a * rad
    
    
    #valid_cmds = ['G0', 'G1', 'G2', 'G3', 'G28', 'G90', 'G91']
    def interpret_cmd(self, cmd):
        
        cmd_s = cmd.split(" ")
        
        if cmd_s[0] == 'G0':
            print('G0')
            
        elif cmd_s[0] == 'G1':
            self.cmd_g1(cmd_s)
            
        elif cmd_s[0] == 'G90':
            self.cmd_g90();
            
        elif cmd_s[0] == 'G91':
            self.cmd_g91();
            
        else:
            print('Invalid gcode command!  Cannot interpret: ' + cmd)
    
    
    '''
    returns the gcode command (i.e. G0, G1, G2, etc)
    '''
    def retrieve_cmd_code(self, cmd):
        
        cmd_s = cmd.split(" ")
        return cmd_s[0]
    
    
    '''
    returns the final position of a G1 command execution without converting/writing it
    '''
    def retrieve_g1_finalpos(self, cmd):
    
        cmd_s = cmd.split(" ")
        
        if cmd_s[0] != 'G1':
            rtrn = [self.posx, self.posy]
            return rtrn
        
        x = 0
        y = 0
        
        for arg in cmd_s:
            
            if arg[0] == 'X':
                x = float(arg[1:])
            elif arg[0] == 'Y':
                y = float(arg[1:])
        
        #rtrn = [self.posx + x, self.posy + y]
        rtrn = [x, y]
        return rtrn
        
        
    def cmd_g1(self, args):    
        #TODO: implement abs movement, first/last movement acceleration/decceleration
        x = ""
        y = ""
        
        for arg in args:
            
            if arg[0] == 'X':
                x = arg[1:]
            elif arg[0] == 'Y':
                y = arg[1:]
        
        self.write(self.lineAtConstSpeed(self.posx, self.posy, float(x), float(y)))
        
        self.posx = float(x)
        self.posy = float(y)
    
    def cmd_g90(self):
        self.mode = 'abs'
    
    
    def cmd_g91(self):
        self.mode = 'rel'
    
    
    def distance(self, x1, y1, x2, y2):
        xdist = math.pow((x2 - x1), 2)
        ydist = math.pow((y2 - y1), 2)
        return math.sqrt(xdist + ydist)
    
    
    '''
    outputs the pvt command for a line which is already moving at a constant speed
    the command mantains the constant speed, however the x/y velocities vary depending
    on their bearing and the total distance being traveled
    '''
    def lineAtConstSpeed(self, startx, starty, endx, endy):
        changex = endx - startx
        changey = endy - starty
        
        #print(self.posx, "   ", endx)
        
        totalDist = self.distance(startx, starty, endx, endy)
        if totalDist == 0:
            print('LINE SKIPPED')
            return 'null'
        
        velx = (changex/totalDist) * self.speed
        vely = (changey/totalDist) * self.speed
        
        time = totalDist/self.speed
        
        #return ('{0:0.6f} {1:0.6f} {2:0.6f} {3:0.6f} {4:0.6f} {5:0.6f} {6:0.6f}'.format(time, changex, velx, changey, vely, 0, 0))
        return ('{0:0.6f} {1:0.6f} {2:0.6f} {3:0.6f} {4:0.6f} {5:0.6f} {6:0.6f}'.format(time, endx, velx, endy, vely, 0, 0))


gc = GcodeConverter(f"{GCODE_INPUT}", f"{TRJ_OUTPUT}")#type in the directory for the input .gcode file and the output .trj file 
gc.print_revised_gcode()#comment out this line if you don't want the revised gcode printed to the console
# gc.init_conversion()#call this command to start the .gcode -> .trj conversion




    