from config import GCODE_INPUT, TRJ_OUTPUT
from gcodeconverter import GcodeConverter as new_gc
from old_gcodeconverter import GcodeConverter as old_gc


def test_revised_gcode():
    new = new_gc(f"{GCODE_INPUT}", f"{TRJ_OUTPUT}")
    old = old_gc(f"{GCODE_INPUT}", f"{TRJ_OUTPUT}")
    assert old.revised_gcode == new.revised_gcode