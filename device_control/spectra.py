import numpy as np
import glob
import matplotlib.pyplot as plt
import clr
import sys
import os
from System.IO import *
from System import String
from System.Threading import AutoResetEvent
from System.Collections.Generic import List

# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import CameraSettings
from PrincetonInstruments.LightField.AddIns import ExperimentSettings
from PrincetonInstruments.LightField.AddIns import DeviceType
from PrincetonInstruments.LightField.AddIns import SpectrometerSettings

import time
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import peakutils 


class LightFieldControl:
    def __init__(self, laser_wavelength:int = 532)->None:
        self.laser_wavelength = laser_wavelength

        auto = Automation(True, List[String]())
        self.application = auto.LightFieldApplication
        self.experiment = auto.LightFieldApplication.Experiment
        self._file_manager = self.controller.application.FileManager

        self.data_manager = data_management()
        

    def save_raman_scan(self,file_name:str)->None:
        self.experiment.SetValue(
        ExperimentSettings.FileNameGenerationBaseFileName,
        Path.GetFileName(file_name))

    # Option to Increment, set to false will not increment
        self.experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachIncrement,
        True)

    # Option to add date
        self.experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachDate,
        True)

    # Option to add time
        self.experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachTime,
        True)
    
    def aquisition_frames(self, number:int)->None:
        self.aquisition_frames_count:int = number
        self._set_value(ExperimentSettings.AcquisitionFramesToStore,number)

    def _set_value(self, setting:CameraSettings|ExperimentSettings|SpectrometerSettings, value:float|int)->None:
        if self.experiment.Exists(setting):
            self.experiment.SetValue(setting, value)

    def collection_time(self, collection_time:int)->None:
        self._set_value(CameraSettings.ShutterTimingExposureTime,collection_time)

    def datapoint_count(self, number:int = 1340):
        self.datapoint_count:int = number

    def begin_scanning(self)->None:
        self.experiment.Acquire()

    def read_spectrum_file(self, spectrum_scan, number_of_datapoints:int, column_count:int = 5)->np.ndarray:
        try:
            file_dir = self.data_manager.new_file_dir()
            spectrum_scan = self._file_manager.OpenFile(file_dir, FileAccess.Read)
            image_data = spectrum_scan.GetFrame(0,0)
            buffer = image_data.GetData()

            intensity_frame:np.ndarray = np.zeros((column_count, self.controller.datapoint_count))

            for i in range(0, self.datapoint_count):
                image_data = spectrum_scan.GetFrame(0,i)
                buffer = spectrum_scan.GetData()
                for pixel in range(0, number_of_datapoints):
                    intensity_frame[i][pixel] = buffer[pixel]

            spectrum_scan.Dispose()

            return intensity_frame
        
        except IOError:
            print("Error: can not find file or read data")
        
    def get_calibration_frame(self, number_of_datapoints):
        
        w = []
        
        wavelength_calibration = self.experiment.SystemColumnCalibration
        calibration = np.zeros((1, number_of_datapoints))
        wavelength = calibration.copy()

        for i in range(number_of_datapoints):
            calibration[0,i] = wavelength_calibration[i]
            
        for i in range(len(number_of_datapoints)):
            #check this spot as a location for errors
            wavelength[0,i] = 1e7*(1/self.laser_wavelength - 1/calibration[0,i])
            w.append(wavelength[0,i])
        
        return w


    def get_intensity_frame(self, number_of_datapoints):
        intensity_frame:np.ndarray = self.read_spectrum_file(number_of_datapoints)
        intensity = np.zeros((1, number_of_datapoints))
        for i in range(number_of_datapoints):
            totalizer = 0
            for j in range(self.controller.aquisition_frames_count):
                totalizer += intensity_frame[j][i]

            avg_intensity:np.ndarray = totalizer/self.controller.aquisition_frames_count
            intensity[0,i] = avg_intensity

        return intensity
    



#data management
class data_management:

    def make_spectrum_directory(self, spectrum_directory:str = 'raw_spectrum')->None:
        check_folder = os.path.isdir(spectrum_directory)
        self.spectrum_directory = spectrum_directory
        if not check_folder:
            os.makedirs(spectrum_directory)
            print(f"created folder : {spectrum_directory}")

        else:
            print(f'{spectrum_directory} folder already exists.')

    def get_new_spe(self):
        all_spectrum_files = glob.glob(self.spectrum_directory +'/*.spe')
        file_dir = max(all_spectrum_files, key=os.path.getctime)
        return file_dir

def collect_gd_ratio(controller:LightFieldControl, collection_time:int):
    controller.collection_time(collection_time)
    controller.begin_scanning()
    time.sleep(35)

def capture_photo():
    pass

def check_connection():
    pass



def name_file():
    pass

