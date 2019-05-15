# Import the .NET class library
import clr

# Import python sys module
import sys, os

# Import saving and opening files
from System.IO import *

# Import c compatible List and String
from System import String
from System.Collections.Generic import List

# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT'] + "\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')
clr.AddReference('System.IO')
clr.AddReference('System.Collections')

# PI imports
import PrincetonInstruments.LightField.AddIns as AddIns
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import CameraSettings, DeviceType


def set_value(setting, value):
    # Check for existence before setting
    # gain, adc rate, or adc quality
    if experiment.Exists(setting):
        experiment.SetValue(setting, value)


def device_found():
    # Find connected device
    for device in experiment.ExperimentDevices:
        if (device.Type == DeviceType.Camera):
            return True
    # If connected device is not a camera inform the user
    print("Cmaera not found. Please add camera and try again")
    return False


# Create the LF app (true for visible)
# The 2nd parameter forces LF to load with no exp
auto = Automation(True, List[String]())

# Get exp obj
experiment = auto.LightFieldApplication.Experiment

if (device_found()==True):
    # Set exposure time
    set_value(CameraSettings.ShutterTimingExposureTime, 20.0)

    # Acquire image
    experiment.Acquire()

# for device in experiment.ExperimentDevices:
#     print(device)
