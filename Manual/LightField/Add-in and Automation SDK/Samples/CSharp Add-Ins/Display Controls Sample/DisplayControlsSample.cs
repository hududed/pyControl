using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.AddIn;
using System.AddIn.Pipeline;

using PrincetonInstruments.LightField.AddIns;

using LightFieldAddInSamples;

namespace LightFieldAddInSamples
{
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Display Controls Sample (C#)",
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments",
    Description = "Shows how to use controls to affect the graph/image viewer")]
    [QualificationData("IsSample", "True")]
    public class AddinDisplayControlsSample : AddInBase, ILightFieldAddIn
    {        
        ///////////////////////////////////////////////////////////////////////
        bool? toolBarState_;
        
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ApplicationToolBar; } }
                
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Button Style
            toolBarState_ = null;            
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////        
        public override void UIApplicationToolBarExecute()
        {
            // Build your controls
            DisplayControlsSample wnd = new DisplayControlsSample(LightFieldApplication);
            
            // Call the base class
            wnd.Title = "Display Controls Sample";

            Show(wnd);
        }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIApplicationToolBarIsChecked
        {
            get { return toolBarState_; }

            // The Button In LightField Was Pushed
            set { toolBarState_ = value; }
        }
        ///////////////////////////////////////////////////////////////////////    
        public override string UIApplicationToolBarTitle { get { return "Display Controls Sample"; } }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Shows how to use controls to affect the graph/image viewer"; }
        }
    }
}
