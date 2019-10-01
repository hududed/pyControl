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
    // This sample acquires a single frame of data synchronously and when the 
    // data is returned it pops it into a window (experiment view 1) for the 
    // user to look at.
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Acquire Synchronous Sample (C#)", 
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments",
    Description = "Shows an example of synchronous acquisition")]
    [QualificationData("IsSample", "True")]
    public class AddinAcquireSyncSample : AddInBase, ILightFieldAddIn
    {
        private Acquire_Sync_Sample.AcquireSyncSample control_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentSetting; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new Acquire_Sync_Sample.AcquireSyncSample(app);            
            ExperimentSettingElement = control_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIExperimentSettingTitle { get { return "Acquire Synchronous Sample"; } }
    }
}
