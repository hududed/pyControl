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
    [AddIn("Export Sample (C#)",
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments",
            Description = "Shows how to export SPE files to other formats")]
    [QualificationData("IsSample", "True")]
    public class AddinExportSample : AddInBase, ILightFieldAddIn
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
        public override string UIApplicationToolBarTitle { get { return "Export Sample"; } }
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
            ExportSample wnd = new ExportSample(LightFieldApplication);

            // Show the dialog
            wnd.Title = "Export Sample";
            Show(wnd);
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Shows how to export SPE files to other formats"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }
    }
}
