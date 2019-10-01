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

namespace LightFieldAddInSamples.Composite_Sample
{   
    ///////////////////////////////////////////////////////////////////////////
    //  This sample shows ad add-in that can dynamically change its appearance
    // and what light field zones it suports ui for. 
    //
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Composite Sample (C#)", 
            Version = "1.0.0",
            Publisher = "Teledyne Princeton Instruments",
            Description = "Shows how to support multiple user interfaces and dynamically change the appearance of an add-in")
    ]
    [QualificationData("IsSample", "True")]
    public class CompositeSample : AddInBase, ILightFieldAddIn
    {
        private ExperimentView control_;
        private Button control2_;

        public Component ExperimentSetting;
        public Component ExperimentView;
        public Component AppToolBar;
        public Component DataToolBar;
        public Component Menu;

        ///////////////////////////////////////////////////////////////////////
        // Fire The Event To The Application (Change all but the view!)
        ///////////////////////////////////////////////////////////////////////
        internal void DingEvent()
        {
            UISupport item = UISupport.DataToolBar | UISupport.ApplicationToolBar | UISupport.ExperimentSetting | UISupport.Menu;
            ChangeExperimentSetting();
            RequestUIRefresh(item);
        }        
        ///////////////////////////////////////////////////////////////////////
        // Dynamically Changes Support Based On Check Boxes
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport 
        { 
            get 
            {
                UISupport flags = UISupport.ExperimentView;

                if (ExperimentSetting != null)
                    if (ExperimentSetting.CanShow)
                        flags |= UISupport.ExperimentSetting;

                if (Menu != null)
                    if (Menu.CanShow)
                        flags |= UISupport.Menu;

                if (AppToolBar != null)
                    if (AppToolBar.CanShow)
                        flags |= UISupport.ApplicationToolBar;

                if (DataToolBar != null)
                    if (DataToolBar.CanShow)
                        flags |= UISupport.DataToolBar;

                return flags; 
            } 
        }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls
            control_ = new ExperimentView(this);            
            ExperimentViewElement = control_;

            // Simple button 
            control2_ = new Button();
            control2_.Content = "Push!";
            ExperimentSettingElement = control2_;
        }
        ///////////////////////////////////////////////////////////////////////
        // If we change one of the UI elements it must be recreated by the addin
        // or reference a different object. 
        public void ChangeExperimentSetting()
        {
            control2_ = new Button();
            control2_.Content = "Push!";
            ExperimentSettingElement = control2_;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }        
        ///////////////////////////////////////////////////////////////////////
        //                      EXPERIMENT VIEW
        ///////////////////////////////////////////////////////////////////////                        
        public override string UIExperimentViewTitle
        { get { return "Composite Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        //                      EXPERIMENT SETTING
        ///////////////////////////////////////////////////////////////////////                
        public override string UIExperimentSettingTitle 
        { get { return ExperimentSetting.Title; } }
        ///////////////////////////////////////////////////////////////////////
        //                      APPLICATION TOOLBAR
        ///////////////////////////////////////////////////////////////////////       
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarTitle 
        { get { return AppToolBar.Title; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIApplicationToolBarIsChecked
        {
            get { return AppToolBar.State;  }
            set { AppToolBar.State = (bool)value; }
        }        
        ///////////////////////////////////////////////////////////////////////
        public override bool UIApplicationToolBarIsEnabled 
        { get { return AppToolBar.IsEnabled; } }
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarToolTip
        {
            get { return AppToolBar.Tip; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override int? UIApplicationToolBarHelpTopicID 
        { get { return 1; } }
        ///////////////////////////////////////////////////////////////////////
        public override void UIApplicationToolBarExecute(){ ; }
        ///////////////////////////////////////////////////////////////////////
        //                      DATA TOOLBAR
        ///////////////////////////////////////////////////////////////////////       
        ///////////////////////////////////////////////////////////////////////
        public override string UIDataToolBarTitle 
        { get { return DataToolBar.Title; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIDataToolBarIsChecked
        {
            get { return DataToolBar.State; }
            set { DataToolBar.State = (bool)value; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override bool UIDataToolBarIsEnabled 
        { get { return DataToolBar.IsEnabled; } }
        ///////////////////////////////////////////////////////////////////////
        public override string UIDataToolBarToolTip
        {
            get { return DataToolBar.Tip; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override int? UIDataToolBarHelpTopicID { get { return 1; } }
        ///////////////////////////////////////////////////////////////////////
        public override void UIDataToolBarExecute() { ; }
        ///////////////////////////////////////////////////////////////////////
        //                  APPLICATION MENU
        ///////////////////////////////////////////////////////////////////////       
        ///////////////////////////////////////////////////////////////////////
        public override string UIMenuTitle { get { return Menu.Title; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool UIMenuIsEnabled { get { return Menu.IsEnabled; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIMenuIsChecked
        {
            get { return Menu.State; }
            set { Menu.State = (bool)value;}
        }
        ///////////////////////////////////////////////////////////////////////
        public override void UIMenuExecute()
        {
            ;
        }
    }

    ///////////////////////////////////////////////////////////////////////////
    // Helper class that ties things  together     
    ///////////////////////////////////////////////////////////////////////////
    public class Component
    {
        // Private Backing
        private string toolTip_;
        private string title_;
        private bool executable_;
        private bool? state_;
        private bool visiblity_;
        private UISupport type_;

        // Create With Settings
        public Component(string title, string tip, bool exec, bool? state, bool vis, UISupport type)
        {
            title_ = title;
            toolTip_ = tip;
            executable_ = exec;
            state_ = state;
            visiblity_ = vis;
            type_ = type;
        }

        // Public Gets
        public string Title { get { return title_; } }
        public string Tip { get { return toolTip_; } }
        public bool IsEnabled { get { return executable_; } }
        public bool CanShow { get { return visiblity_; } }
        public UISupport Type { get { return type_; } }
        public bool? State { get { return state_; } set { state_ = value; } }
    }
}
