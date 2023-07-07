import math

import numpy as np


class ArcConverter:
    
    
    def __init__(self, cmd: str, start_xpos: int=0, start_ypos: int=0, step_size: float=0.1, mode: str='abs') -> None:
        
        self.cmd = cmd
        self.step_size = step_size
        self.mode = mode
        
        if mode == 'rel':
            self.start_xpos = 0
            self.start_ypos = 0
        
        else:
            self.start_xpos = start_xpos
            self.start_ypos = start_ypos
            
        self.output_cmds: list[str] = []
        
        #parse cmd
        args = self.cmd.split(" ")
        
        if args[0] == 'G02' or args[0] == 'G2': #clockwise arc
            #print('clockwise')
            self.dir: str = 'cw'
            
        elif args[0] == 'G03' or args[0] == 'G3': #counter-clockwise arc
            #print('counter-clockwise')
            self.dir: str = 'ccw'
        
        else:
            #print('invalid arc command provided, defaulting to a clockwise (G2) arc')
            self.dir: str = 'cw'
            
        self.xoffset: float = 0
        self.yoffset: float = 0
        
        self.end_xpos: float = 0
        self.end_ypos: float = 0
        self.center_xpos: float = 0
        self.center_ypos: float = 0
        
        for arg in args:
            
            if arg[0] == 'X':
                self.end_xpos = float(arg[1:])
                
            elif arg[0] == 'Y':
                self.end_ypos = float(arg[1:])
                
            elif arg[0] == 'I':
                self.center_xpos = float(arg[1:])
                
            elif arg[0] == 'J':
                self.center_ypos = float(arg[1:])

        #self.radius = self.distance(0, 0, self.center_xpos, self.center_ypos)#OG
        self.radius = self.distance(self.start_xpos, self.start_ypos, self.end_xpos, self.end_ypos)/2
       
        #self.angle = self.arc_angle(self.start_xpos, self.start_ypos, self.end_xpos, self.end_ypos, self.center_xpos, self.center_ypos)#OG
        self.angle = 180
        #self.angle = self.arc_angle(0, 0, self.end_xpos, self.end_ypos, self.center_xpos, self.center_ypos)
        
        #self.arc_to_lines(self.start_xpos, self.start_ypos, self.end_xpos, self.end_ypos, self.angle)#OG
        if self.dir == 'cw':
            self.arc_to_lines_cw(self.start_xpos, self.start_ypos, self.end_xpos, self.end_ypos, self.angle)#OG
        elif self.dir == 'ccw':
            self.arc_to_lines_ccw(self.start_xpos, self.start_ypos, self.end_xpos, self.end_ypos, self.angle)#OG


    '''
    returns the length of an arc
    '''
    def arc_length(self, x_start: float, y_start: float, x_end: float, y_end: float, x_center: float, y_center: float) -> float:
        
        a = self.distance(x_end, y_end, x_center, y_center)
        b = self.distance(x_start, y_start, x_center, y_center)
        c = self.distance(x_end, y_end, x_start, y_start)

        num = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
        den = 2 * a * b
        if den == 0:
            return 0
        div = num / den
        div *= -1
        
        rad = math.acos(div)
        if self.dir == 'ccw':
            rad = (2 * math.pi) - rad
        
        #print('arc length', (a * rad))
        return a * rad
    
    
    '''
    returns the angle of an arc
    '''
    def arc_angle(self, x_start: float, y_start: float, x_end: float, y_end: float, x_center: float, y_center: float) -> float:
        a = self.distance(x_end, y_end, x_center, y_center)
        b = self.distance(x_start, y_start, x_center, y_center)
        c = self.distance(x_end, y_end, x_start, y_start)

        num = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
        den = 2 * a * b
        if den == 0:
            return math.degrees(math.acos(np.round(0, 6)))
        div = num / den
        div *= -1

        rad = math.acos(np.round(div, 6))

        # For now, I am assuming all angles are <= 180 degrees, so I am only using the calculation for the minor angle. This may change later.
        return math.degrees(rad)


    def distance_from_arc_point_to_arc_center(self, arc_angle: float, arc_radius: float) -> float:
        angle = arc_angle/2
        return math.sin(math.radians(angle)) * arc_radius * 2


    def distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.hypot(x2 - x1, y2 - y1)
    
    def rotate_point(self, x_pos: float, y_pos: float, degree: float) -> list[float]:
        x_new = math.cos(degree) * (x_pos - self.center_xpos) - math.sin(degree) * (y_pos - self.center_ypos) + self.center_xpos
        y_new = math.sin(degree) * (x_pos - self.center_xpos) + math.cos(degree) * (y_pos - self.center_ypos) + self.center_ypos
        return [x_new, y_new]

    def arc_to_lines_cw(self, x_start: float, y_start: float, x_end: float, y_end: float, angle: float) -> None:
        self.arc_to_lines(x_start, y_start, x_end, y_end, angle, True)

    def arc_to_lines_ccw(self, x_start: float, y_start: float, x_end: float, y_end: float, angle: float) -> None:
        self.arc_to_lines(x_start, y_start, x_end, y_end, angle, False)

    def arc_to_lines(self, x_start: float, y_start: float, x_end: float, y_end: float, angle: float, cw: str) -> None:
        if self.distance(x_start, y_start, x_end, y_end) <= self.step_size:
            rtrn = 'G1 X{0:0.6f} Y{1:0.6f}'.format(x_end, y_end)
            self.output_cmds.append(rtrn)
            return

        dist_to_center = self.distance_from_arc_point_to_arc_center(angle/2, self.radius)
        dist_between_points = self.distance(x_start, y_start, x_end, y_end)

        # find the x coordinate of the center point
        pt1_x = (x_start + x_end)/2 if cw else (x_end + x_start)/2
        pt2_x = (y_start - y_end)/2 if cw else (y_end - y_start)/2
        pt3 = (2 * dist_to_center)/dist_between_points
        pt3 = math.pow(pt3, 2)
        pt3 = pt3 - 1
        pt3 = math.sqrt(pt3)
        x = pt1_x + (pt2_x * pt3)

        # find the y coordinate of the center point
        pt1_y = (y_start + y_end)/2 if cw else (y_end + y_start)/2
        pt2_y = (x_start - x_end)/2 if cw else (x_end - x_start)/2
        y = pt1_y - (pt2_y * pt3)

        self.arc_to_lines(x_start, y_start, x, y, angle/2, cw)
        self.arc_to_lines(x, y, x_end, y_end, angle/2, cw)

    def get_output_cmds(self) -> list[str]:
        return self.output_cmds




