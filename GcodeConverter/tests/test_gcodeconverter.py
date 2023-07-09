import filecmp

from config import ALT_GCODE_INPUT, GCODE_INPUT, OLD_TRJ_OUTPUT, TRJ_OUTPUT
from gcodeconverter import GcodeConverter as new_gc
from old_gcodeconverter import GcodeConverter as old_gc


def test_revised_gcode():
    new = new_gc(f"{GCODE_INPUT}", f"{TRJ_OUTPUT}")
    old = old_gc(f"{GCODE_INPUT}", f"{OLD_TRJ_OUTPUT}")
    assert old.revised_gcode == new.revised_gcode

def test_trajectory_file():
    new = new_gc(f"{GCODE_INPUT}", f"{TRJ_OUTPUT}")
    old = old_gc(f"{GCODE_INPUT}", f"{OLD_TRJ_OUTPUT}")
    new.init_conversion()
    old.init_conversion()
    with open(f"{TRJ_OUTPUT}", "r") as new_file, open(f"{OLD_TRJ_OUTPUT}", "r") as old_file:
        new_lines = new_file.readlines()
        old_lines = old_file.readlines()
        assert len(new_lines) == len(old_lines)
        for i in range(len(new_lines)):
            assert new_lines[i] == old_lines[i]
        
