using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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
    [AddIn("Data Sample (C#)", Version = "1.0.0", Publisher = "Teledyne Princeton Instruments", Description = "Shows how to create, modify, and display data")]
    [QualificationData("IsSample", "True")]
    public class AddinDataSample : AddInBase, ILightFieldAddIn
    {
        bool? toolBarState_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.ApplicationToolBar; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication = app;
            toolBarState_ = null; // Forces it to be a button, true or false
                                  // would make it a checkbox
        }
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() { }
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarTitle { get { return "Data Sample"; } }
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
            GenerateRamps(); 
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIApplicationToolBarToolTip
        {
            get { return "Generate Linear Ramps frames of data and display them as an example of how to create, modify, and display data"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIApplicationToolBarIsEnabled{ get { return true; } }
        ///////////////////////////////////////////////////////////////////////        
        //  Make a linear ramp of data and display it.         
        ///////////////////////////////////////////////////////////////////////
        private void GenerateRamps()
        {
            // Make A Frame 200x400 pixels
            ushort[] frame1 = new ushort[200 * 400];
            for (int pix = 0; pix < 200 * 400; pix++)
                frame1[pix] = (ushort)(pix % 400);

            // Make A Frame 300x500 pixels with a 1k bias
            ushort[] frame2 = new ushort[300 * 500];
            for (int pix = 0; pix < 300 * 500; pix++)
                frame2[pix] = (ushort)((pix % 500) + 1000);

            // Get the addin file manager
            var datamgr = LightFieldApplication.DataManager;
            if (datamgr != null)
            {
                RegionOfInterest roi  = new RegionOfInterest(0, 0, 400, 200, 1, 1);
                RegionOfInterest roi2 = new RegionOfInterest(0, 0, 500, 300, 1, 1);

                // Simple Single Region
                IImageDataSet imageData = datamgr.CreateImageDataSet(frame1, roi, ImageDataFormat.MonochromeUnsigned16);

                RegionOfInterest[] rois = { roi, roi2 };
                
                List<Array> buffers = new List<Array>();
                buffers.Add(frame1);
                buffers.Add(frame2);

                // Complex Set Containing Two Regions
                IImageDataSet imageDataSets = datamgr.CreateImageDataSet(buffers, rois, ImageDataFormat.MonochromeUnsigned16);

                IDisplay display = LightFieldApplication.DisplayManager;
                if (display != null)
                {
                    // Select Data File Compare Mode & 3 Vertical Windows 
                    display.ShowDisplay(DisplayLocation.ExperimentWorkspace, DisplayLayout.TwoHorizontal);
                    IDisplayViewer view = null;

                    // Modify the underlying data a little bit before displaying it.
                    ModifyDataExample(imageData, 0);

                    // Put the simple data in window 0
                    view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, 0);
                    view.Display("SimpleRamp", imageData);

                    // Modify the underlying data a little bit before displaying it.
                    ModifyDataExample(imageDataSets, 1);

                    // Put the complex data in window 1
                    view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, 1);
                    view.Display("ComplexRamp", imageDataSets);                    
                }                
            }           
        }
        ///////////////////////////////////////////////////////////////////////
        //  Change some of the values in the underlying IImageDataSet
        ///////////////////////////////////////////////////////////////////////
        void ModifyDataExample(IImageDataSet imageData, int roiIdx)
        {
            // Demostrate how to access the data and change it                
            var rois = imageData.Regions;

            // Get the width & the height
            int h = rois[roiIdx].Height;
            int w = rois[roiIdx].Width;

            // Get sub image arrays from the data set 
            IImageData row = imageData.GetRow(roiIdx, 0, h / 2);
            IImageData col = imageData.GetColumn(roiIdx, 0, w / 2);
            IImageData pix = imageData.GetPixel(roiIdx, 0, h / 2, w / 2);

            // Create new arrays to replace data
            ushort[] rowData = new ushort[w];
            ushort[] colData = new ushort[h];
            ushort[] pixData = new ushort[1];

            // Build up new data with values
            for (int x = 0; x < w; x++)
                rowData[x] = (ushort)(5000 + x);
            for (int y = 0; y < h; y++)
                colData[y] = (ushort)(10000 + y);

            // bright pixel
            pixData[0] = 65535;

            // Push back to original buffer
            row.SetData(rowData);
            col.SetData(colData);
            pix.SetData(pixData);        
        }
    }
}
