using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.AddIn;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.AddIn.Pipeline;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Plot Sample (C#)", 
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments", 
    Description="Demonstrates making data in memory and then plotting it as graphs\nThis also demonstrates adding multiple graph sources to the same window")]
    [QualificationData("IsSample", "True")]
    public class AddinPlotSample : AddInBase, ILightFieldAddIn
    {
        bool? toolBarState_;

        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ApplicationToolBar; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;
            toolBarState_ = null;
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarTitle { get { return "Plot Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIApplicationToolBarIsChecked
        {
            get { return toolBarState_;  }
            set { toolBarState_ = value; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override void UIApplicationToolBarExecute()
        {
            PlotSinAndCos(); 
        }
        ///////////////////////////////////////////////////////////////////////
        public override bool UIApplicationToolBarIsEnabled{ get { return true; }}
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarToolTip
        {
            get { return "Generate Cos & Sin Curves and display results in four windows to demonstrate making data in memory and plotting graphs"; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override int? UIApplicationToolBarHelpTopicID{ get { return 1;}}
        ///////////////////////////////////////////////////////////////////////
        public override Bitmap UIApplicationToolBarBitmap
        {
            get 
            {
                Assembly executingAssembly  = Assembly.GetExecutingAssembly();                
                Stream resourceStream       = executingAssembly.GetManifestResourceStream("LightFieldCSharpAddInSamples.Plot_Sample.PlotSample.bmp");                
                Bitmap image                = new Bitmap(resourceStream);
                return image;   
            }
        }
        ///////////////////////////////////////////////////////////////////////
        // Show 4 Plots of Cos vs Sine in Quad Display
        // 1.) Generates Raw Data
        // 2.) Builds IImageData(s) with the raw data from the DataManager. 
        // 3.) Gets 4 Displays and Puts 2 Waveforms in each display.        
        ///////////////////////////////////////////////////////////////////////
        private void PlotSinAndCos()
        {
            // Make two curves (720 = 2*PI so its a full cycle)
            ushort[] cosine = new ushort[720];
            ushort[] sine = new ushort[720];

            // Generate Curves (Amplitude 100)
            for (int pix = 0; pix < 720; pix++)
            {
                // Convert To Angle
                double angle = Math.PI * ((double)pix - 360) / 180.0;

                // Compute Points
                cosine[pix] = (ushort)((double)100 * (Math.Cos(angle) + (double)1));
                sine[pix] = (ushort)((double)100 * (Math.Sin(angle) + (double)1));
            }

            // Get the data manager
            var datamgr = LightFieldApplication.DataManager;
            if (datamgr != null)
            {
                RegionOfInterest roi = new RegionOfInterest(0,0,720,1,1,1);
                // Create Blobs
                IImageDataSet cosData = datamgr.CreateImageDataSet(cosine, roi, ImageDataFormat.MonochromeUnsigned16);
                IImageDataSet sineData = datamgr.CreateImageDataSet(sine,  roi, ImageDataFormat.MonochromeUnsigned16);

                // Get The Display Object
                IDisplay display = LightFieldApplication.DisplayManager;
                if (display != null)
                {
                    // Select Data File Compare Mode & 4 Even Windows
                    display.ShowDisplay(DisplayLocation.ExperimentWorkspace, DisplayLayout.FourEven);
                    IDisplayViewer view = null;

                    // Put the data in all 4 windows
                    for (int i = 0; i <= 3; i++)
                    {
                        view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, i);
                        view.Display("Cosine", cosData);
                        IDisplaySource sinSource = display.Create("Sine", sineData);
                        view.Add(sinSource);
                    }
                }
            }
        }
    }
}
