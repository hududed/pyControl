import math

from arcconverter import ArcConverter


def test_parse_cmd():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    ac.parse_cmd(gcode)
    assert ac.cmd == gcode
    assert ac.dir == 'cw'
    assert ac.end_xpos == 0
    assert ac.end_ypos == -0.5
    assert ac.center_xpos == 0
    assert ac.center_ypos == -0.25

def test_distance():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    assert math.isclose(ac.distance(5, 0, 0, -0.5), 5.024937810560445)
    assert math.isclose(ac.distance(0, 0, 0, -0.5), 0.5)
    assert math.isclose(ac.distance(5, 0, 0, 0), 5)

def test_distance_from_arc_point_to_arc_center():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    assert math.isclose(ac.distance_from_arc_point_to_arc_center(90, 0.25), 0.3535533905932738)
    assert math.isclose(ac.distance_from_arc_point_to_arc_center(180, 0.25), 0.5)
    assert math.isclose(ac.distance_from_arc_point_to_arc_center(45, 0.5), 0.3826834323650898)

def test_arc_angle():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    assert math.isclose(ac.arc_angle(5, 0, 0, -0.5, 0, -0.25), 92.8624272010275)
    assert math.isclose(ac.arc_angle(0, 0, 0, -0.5, 0, -0.25), 180)
    assert math.isclose(ac.arc_angle(5, 0, 0, 0, 0, -0.25), 87.1375727989725)

def test_rotate_point():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    assert ac.rotate_point(0, -0.25, 90) == [0.0, -0.25]
    assert ac.rotate_point(0, -0.25, 180) == [0.0, -0.25]
    assert ac.rotate_point(0, -0.25, 270) == [0.0, -0.25]

def test_arc_to_lines():
    gcode = 'G2 X0 Y-0.5 I0 J-0.25'
    ac = ArcConverter(gcode)
    ac.output_cmds = []
    ac.arc_to_lines_cw(0, 0, 0.0, -0.5, 180)
    assert ac.get_output_cmds() == ['G1 X0.095671 Y-0.019030', 'G1 X0.176777 Y-0.073223', 'G1 X0.230970 Y-0.154329', 'G1 X0.250000 Y-0.250000', 'G1 X0.230970 Y-0.345671', 'G1 X0.176777 Y-0.426777', 'G1 X0.095671 Y-0.480970', 'G1 X0.000000 Y-0.500000']
    
    ac.output_cmds = []
    ac.arc_to_lines_ccw(0, 0, 0.0, -0.5, 180)
    assert ac.get_output_cmds() == ['G1 X-0.095671 Y-0.019030', 'G1 X-0.176777 Y-0.073223', 'G1 X-0.230970 Y-0.154329', 'G1 X-0.250000 Y-0.250000', 'G1 X-0.230970 Y-0.345671', 'G1 X-0.176777 Y-0.426777', 'G1 X-0.095671 Y-0.480970', 'G1 X0.000000 Y-0.500000']
