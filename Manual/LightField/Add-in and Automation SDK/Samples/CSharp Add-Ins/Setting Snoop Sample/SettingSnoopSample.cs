using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.AddIn;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Windows;
using System.AddIn.Pipeline;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Setting Snoop Sample (C#)", 
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments", 
    Description="Demonstrates an add-in with no user interface that registers for setting changed events and logs them")]
    [QualificationData("IsSample", "True")]
    public class AddinSettingSnoopSample : AddInBase, ILightFieldAddIn
    {
        // Since we need to hook / unhook the filter keep a single reference
        // instead of getting it each time.
        IExperiment theExperiment_;
        string fullName_;

        ///////////////////////////////////////////////////////////////////////
        // Get All The Setting Names of A Given Type
        ///////////////////////////////////////////////////////////////////////
        public IEnumerable<string> GetAllNames(Type type)
        {
            FieldInfo[] fieldInfos = type.GetFields(BindingFlags.Public | BindingFlags.Static);
            return fieldInfos.Where(fi => fi.IsLiteral && !fi.IsInitOnly)
                .Select(fi => fi.GetValue(null).ToString());
        }
        ///////////////////////////////////////////////////////////////////////
        // Return We Don't Support a User Interface
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.None; } }
        ///////////////////////////////////////////////////////////////////////
        // Make a list of settings and set the filter to them as well
        // as hook the changed event.
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Set the add-ins discovery root directory to be the current directory
            string addinRoot = AppDomain.CurrentDomain.BaseDirectory;
            fullName_ = Path.Combine(addinRoot, "SettingSnoopSample.txt");

            theExperiment_ = app.Experiment;

            // Generate a filter with only the valid settings 
            List<string> filteredSettings = new List<string>();

            // Load Up The Setting Strings
            IEnumerable<string> CameraSettings       = GetAllNames(typeof(CameraSettings));
            IEnumerable<string> ExperimentSettings   = GetAllNames(typeof(ExperimentSettings));
            IEnumerable<string> FilterSettings       = GetAllNames(typeof(FilterWheelSettings));
            IEnumerable<string> SpectrometerSettings = GetAllNames(typeof(SpectrometerSettings));
           
            // put them all into the filter    
            // camera
            foreach (string str in CameraSettings)
                filteredSettings.Add(str);
            // experiment
            foreach (string str in ExperimentSettings)          
                filteredSettings.Add(str);
            // filterWheel
            foreach (string str in FilterSettings)
                filteredSettings.Add(str);
            // spectrometer
            foreach (string str in SpectrometerSettings)            
                filteredSettings.Add(str);

            // Connect the setting change handler
            theExperiment_.SettingChanged += new EventHandler<SettingChangedEventArgs>(Experiment_SettingChanged);

            // Apply the filter
            theExperiment_.FilterSettingChanged(filteredSettings);

            // Also Monitor System building events
            theExperiment_.ExperimentUpdating += Experiment_ExperimentUpdating;
            theExperiment_.ExperimentUpdated += Experiment_ExperimentUpdated;
        }

        ///////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////
        void Experiment_ExperimentUpdated(object sender, ExperimentUpdatedEventArgs e)
        {            
            // Time Stamp
            DateTimeOffset dateTimeOffset = DateTimeOffset.Now;

            // Stream Writer Set to append if the file is there
            using (StreamWriter fs = new StreamWriter(fullName_, true))
            {
                if (fs != null)
                    fs.WriteLine(dateTimeOffset.ToString() + " ExperimentUpdated Event");
            }         
        }
        ///////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////
        void Experiment_ExperimentUpdating(object sender, ExperimentUpdatingEventArgs e)
        {            
            // Time Stamp
            DateTimeOffset dateTimeOffset = DateTimeOffset.Now;

            // Stream Writer Set to append if the file is there
            using (StreamWriter fs = new StreamWriter(fullName_, true))
            {
                if (fs != null)
                    fs.WriteLine(dateTimeOffset.ToString() + " ExperimentUpdating Event");
            }         
        }
        ///////////////////////////////////////////////////////////////////////
        // Disconnect the event handler from the event.
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() 
        {            
            theExperiment_.SettingChanged       -= Experiment_SettingChanged;            
            theExperiment_.ExperimentUpdating   -= Experiment_ExperimentUpdating;
            theExperiment_.ExperimentUpdated    -= Experiment_ExperimentUpdated;
        }
        ///////////////////////////////////////////////////////////////////////
        // When a setting in the filter list changes this will get called by
        // the application.
        ///////////////////////////////////////////////////////////////////////
        void Experiment_SettingChanged(object sender, SettingChangedEventArgs e)
        {            
            // Setting name
            string settingName  = ":  Setting:" + e.Setting;

            // Setting value
            string settingValue = " Value: " + theExperiment_.GetValue(e.Setting).ToString();
            
            // Time Stamp
            DateTimeOffset dateTimeOffset = DateTimeOffset.Now;
            
            // Stream Writer Set to append if the file is there
            using (StreamWriter fs = new StreamWriter(fullName_,true))
            {
                if (fs != null)
                    fs.WriteLine(dateTimeOffset.ToString() + settingName + settingValue);
            }                        
        }

    }
}

