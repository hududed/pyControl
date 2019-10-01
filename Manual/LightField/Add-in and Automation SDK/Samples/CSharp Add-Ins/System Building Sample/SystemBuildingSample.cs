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
    [AddIn("System Building Sample (C#)",
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments",
            Description = "Demonstrates how to build a system from components")]
    [QualificationData("IsSample", "True")]
    public class AddinSystemBuildingSample : AddInBase, ILightFieldAddIn
    {
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

        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarTitle { get { return "System Building Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIApplicationToolBarIsChecked
        {
            get { return toolBarState_; }

            // The Button In LightField Was Pushed
            set { toolBarState_ = value; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override void UIApplicationToolBarExecute()
        {
            // Bring up a wpf dialog and 
            SystemBuildingSampleControl wnd = new SystemBuildingSampleControl(LightFieldApplication);

            // Show the dialog
            wnd.Title = "System Building Sample";
            ShowDialog(wnd);
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Demonstrates how to build a system from components"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }    
    }
}
