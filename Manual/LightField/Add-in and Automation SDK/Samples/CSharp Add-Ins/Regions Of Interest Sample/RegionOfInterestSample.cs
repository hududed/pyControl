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
    // This sample is intended to be activated and used only when you have a 
    // a camera in the system, if no camera is in the system this will simply
    // fail to initialize and unload itself.
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Regions Of Interest Sample (C#)", Version = "1.0.0", Publisher = "Teledyne Princeton Instruments", Description = "Shows how to work with the region of interest settings")]
    [QualificationData("IsSample", "True")]
    public class AddinRegionsOfInterestSample : AddInBase, ILightFieldAddIn
    {
        private LightFieldAddInSamples.Regions_Of_Interest_Sample.RegionControl control_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentSetting; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new LightFieldAddInSamples.Regions_Of_Interest_Sample.RegionControl(LightFieldApplication);            
            ExperimentSettingElement = control_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }                
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentSettingTitle { get { return "Regions Of Interest Sample"; } }
    }
}
