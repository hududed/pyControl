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
    ////////////  MODAL DIALOG SAMPLE  ////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////    
    [AddIn("Modal Dialog Sample (C#)", 
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments", 
            Description = "Shows an example of a modal dialog window")
    ]
    [QualificationData("IsSample", "True")]
    public class ModalDialogSample : AddInBase, ILightFieldAddIn
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
        public override string UIApplicationToolBarTitle { get { return "Modal Dialog Sample"; } }
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
            DialogSampleWindow wnd = new DialogSampleWindow();

            // Show the dialog
            wnd.Title = "Modal Dialog Example";            
            ShowDialog(wnd);
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Open a modal dialog window that inherits its styles from LightField"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }    
    }

    ///////////////////////////////////////////////////////////////////////////    
    ////////  MODELESS DIALOG SAMPLE  /////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Modeless Dialog Sample (C#)",
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments",
            Description = "Shows an example of a modeless dialog window")
    ]
    [QualificationData("IsSample", "True")]
    public class ModelessDialogSample : AddInBase, ILightFieldAddIn
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
        public override string UIApplicationToolBarTitle { get { return "Modeless Dialog Sample"; } }
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
            DialogSampleWindow wnd = new DialogSampleWindow();

            // Call the base class
            wnd.Title = "Modeless Dialog Example";
            Show(wnd);
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Open a modal dialog window that inherits its styles from LightField"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }
    }
}

