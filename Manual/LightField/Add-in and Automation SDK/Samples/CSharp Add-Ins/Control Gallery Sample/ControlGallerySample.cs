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
    //  This sample is nothing more than a container to show off the default 
    // look and feel of controls from lightfield. It makes a view type of add-in
    // and sticks a bunch of controls in it. 
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Control Gallery Sample (C#)",
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments",
            Description = "Shows the look and feel of .NET controls when inheriting the LightField styles")]
    [QualificationData("IsSample", "True")]
    public class AddinGallerySample : AddInBase, ILightFieldAddIn
    {
        private Control_Gallery_Sample.ControlGallerySample control_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentView; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            ScrollViewer sv = new ScrollViewer();            
            // Build your controls
            control_ = new Control_Gallery_Sample.ControlGallerySample();

            sv.Content = control_;
            ExperimentViewElement = sv;//control_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }        
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentViewTitle { get { return "Control Gallery Sample"; } }
        
    }
}
