# Import the .NET class library
import clr

# Import python sys module
import sys, os

# numpy import
import numpy as np
import pandas as pd

# Import saving and opening files
from System.IO import *

# Import c compatible List and String
from System import String
from System.Collections.Generic import List
from System.Runtime.InteropServices import GCHandle, GCHandleType

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
from PrincetonInstruments.LightField.Automation import *
from PrincetonInstruments.LightField.AddIns import *


def set_value(setting, value):
    # Check for existence before setting
    # gain, adc rate, or adc quality
    if experiment.Exists(setting):
        experiment.SetValue(setting, value)


def validate_camera():
    camera = None

    # Find connected device
    for device in _experiment.ExperimentDevices:
        if (device.Type == DeviceType.Camera & _experiment.IsReadyToRun):
            camera = device

    if (camera == None):
        print("This sample requires a camera.")
        return False

    if (not _experiment.IsReadyToRun):
        print("The system is not ready for acquisition, is there an error?")

    return True


# Create the LightField Application (true for visible)
# The 2nd parameter forces LF to load with no experiment
_auto = Automation(True, List[String]())

# Get LightField Application object
_application = _auto.LightFieldApplication

# Get experiment object
_experiment = _application.Experiment

# Validate camera state
if (validate_camera()):

    images = 1
    frames = 10

    # Set number of frames
    _experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, frames)

    # Set exposure time
    set_value(CameraSettings.ShutterTimingExposureTime, 3000.0)

    # Capture 1 image 10 frame
    imageset = _experiment.Capture(frames)

    # Stop processing if we do not have all frames
    if (imageset.Frames != frames):
        # Clean up the image data set
        imageset.Dispose();

        raise Exception("Frames are not equal.")

    img_data = imageset.GetDataBuffer()
    df = pd.DataFrame(img_data)
    y_all = df.iloc[::2].reset_index(drop=True)
    y0, y1, y2, y3, y4, y5, y6, y7, y8, y9 = y_all[:1340], \
                                             y_all[1340:2680].reset_index(drop=True), \
                                             y_all[2680:4020].reset_index(drop=True), \
                                             y_all[4020:5360].reset_index(drop=True), \
                                             y_all[5360:6700].reset_index(drop=True), \
                                             y_all[6700:8040].reset_index(drop=True), \
                                             y_all[8040:9380].reset_index(drop=True), \
                                             y_all[9380:10720].reset_index(drop=True), \
                                             y_all[10720:12060].reset_index(drop=True), \
                                             y_all[12060:].reset_index(drop=True)

    intensity = pd.concat([y0, y1, y2, y3, y4, y5, y6, y7, y8, y9], axis=1)
    intensity.columns = list('0123456789')
    intensity['mean'] = intensity.mean(axis=1)
    cal = _experiment.SystemColumnCalibration
    ncal = np.array([float(i) for i in cal])
    wavenumber = pd.DataFrame(1e7 * (1 / 532 - 1 / ncal))
    _df = pd.concat([wavenumber.round(2), intensity], axis=1)

    print(_df)

auto.Dispose()



