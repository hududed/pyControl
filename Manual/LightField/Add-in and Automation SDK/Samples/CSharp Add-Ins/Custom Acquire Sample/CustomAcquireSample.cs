using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.AddIn;
using System.AddIn.Pipeline;

using PrincetonInstruments.LightField.AddIns;


namespace LightFieldAddInSamples
{
    ///////////////////////////////////////////////////////////////////////////
    //  This sample sets an exposure time, disables date and time as part of the 
    // file name and sets a specific name. Note pressing the button multiple times
    // will continually overwrite the file. (This sample also overrides the file
    // already exists dialog)
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Custom Acquire Sample (C#)", 
    Version = "1.0.0",
    Publisher= "Teledyne Princeton Instruments",
    Description= "Shows how to change some settings and acquire data using the customized values")]
    [QualificationData("IsSample", "True")]
    public class AddinCustomAcquireSample : AddInBase, ILightFieldAddIn
    {
        EventHandler<ExperimentCompletedEventArgs> acquireCompletedEventHandler_;
        
        private Button control_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentSetting; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new Button();
            control_.Content = "Acquire";
            control_.Click += new RoutedEventHandler(control__Click);
            ExperimentSettingElement = control_;
        }
        ///////////////////////////////////////////////////////////////////////
        bool ValidateAcquisition()
        {
            IDevice camera = null;
            foreach (IDevice device in LightFieldApplication.Experiment.ExperimentDevices)
            {
                if (device.Type == DeviceType.Camera)
                    camera = device;
            }
            ///////////////////////////////////////////////////////////////////////
            if (camera == null)
            {
                MessageBox.Show("This sample requires a camera!");
                return false;
            }
            ///////////////////////////////////////////////////////////////////////
            if (!LightFieldApplication.Experiment.IsReadyToRun)
            {
                MessageBox.Show("The system is not ready for acquisition, is there an error?");
                return false;
            }
            return true;
        }
        ///////////////////////////////////////////////////////////////////////
        // Override some typical settings and acquire an spe file with a 
        // specific name. 
        ///////////////////////////////////////////////////////////////////////
        private void control__Click(object sender, RoutedEventArgs e)
        {
            // Are we in a state where we can do this?
            if (!ValidateAcquisition())
                return; 

            // Get the experiment object
            IExperiment experiment = LightFieldApplication.Experiment;
            if (experiment != null)
            {                                
                // Not All Systems Have an Exposure Setting, if they do get the minimum and set it
                if (experiment.Exists(CameraSettings.ShutterTimingExposureTime))
                {
                    ISettingRange currentRange = experiment.GetCurrentRange(CameraSettings.ShutterTimingExposureTime);                    
                    experiment.SetValue(CameraSettings.ShutterTimingExposureTime, currentRange.Minimum);              
                }               

                // Don't Attach Date/Time
                experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, false);
                experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, false);
                
                // Save file as Specific.Spe to the default directory
                experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, "Specific");

                // Connnect the event handler
                acquireCompletedEventHandler_ = new EventHandler<ExperimentCompletedEventArgs>(exp_AcquisitionComplete);
                experiment.ExperimentCompleted += acquireCompletedEventHandler_;

                // Begin the acquisition 
                experiment.Acquire();
            }
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire Completed Handler
        // This just fires a message saying that the data is acquired.
        ///////////////////////////////////////////////////////////////////////
        void exp_AcquisitionComplete(object sender, ExperimentCompletedEventArgs e)
        {
            ((IExperiment)sender).ExperimentCompleted -= acquireCompletedEventHandler_;
            MessageBox.Show("Acquire Completed");
        }               
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }                
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentSettingTitle { get { return "Custom Acquire Sample"; } }
    }

}
                
