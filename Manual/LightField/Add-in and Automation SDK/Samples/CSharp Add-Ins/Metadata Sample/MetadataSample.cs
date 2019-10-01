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
    //  Acquire multiple frames and show the meta data for each frame    
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Metadata Sample (C#)",
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments", 
    Description="Demonstrates metadata tagging and how to access the timestamps on the data after acquisition on a frame by frame basis")]
    [QualificationData("IsSample", "True")]
    public class AddinMetaDataSample : AddInBase, ILightFieldAddIn
    {
        private LightFieldAddInSamples.Metadata_Sample.MetadataSample control_;
        
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ExperimentSetting; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;

            // Build your controls            
            control_ = new LightFieldAddInSamples.Metadata_Sample.MetadataSample(LightFieldApplication);
            ExperimentSettingElement = control_;
        }                        
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////
        public override string UIExperimentSettingTitle { get { return "Metadata Sample"; } }
    }
}


