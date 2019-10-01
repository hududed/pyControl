using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Markup;
using System.AddIn;
using System.IO;
using System.AddIn.Pipeline;

using PrincetonInstruments.LightField.AddIns;

using LightFieldAddInSamples;

namespace LightFieldAddInSamples
{   
    ///////////////////////////////////////////////////////////////////////////
    // This sample is intended to show how to acquire data(to the default name
    // and location) and demonstrate how to hook into the acquisition started
    // and acquisition completed events.
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Acquire Asynchronous Sample (C#)", 
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments", 
            Description = "Shows an example of asynchronous acquisition and how to use events")]
    [QualificationData("IsSample", "True")]
    public class AddinAcquireAsyncSample : AddInBase, ILightFieldAddIn
    {
        private Acquire_Async_Sample.AsynAcquireSample control_;

        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentSetting; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new Acquire_Async_Sample.AsynAcquireSample(LightFieldApplication);
            ExperimentSettingElement = control_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////        
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentSettingTitle { get { return "Acquire Asynchronous Sample"; } }       
    }
}
