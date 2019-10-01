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
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Viewer Sample (C#)", 
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments", 
            Description = "Shows how to create your own view of data, a report, or any custom view from within LightField \nThis example allows you to open a file through LightField and then converts it to a bitmap and displays it")]
    [QualificationData("IsSample", "True")]
    public class AddinViewerSample : AddInBase, ILightFieldAddIn
    {
        private ViewerSample control_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentView; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new ViewerSample(LightFieldApplication);
            ExperimentViewElement = control_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }                
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentViewTitle { get { return "Viewer Sample"; } }
    }
}
