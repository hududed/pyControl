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
    [AddIn("File Sample (C#)", Version = "1.0.0", Publisher = "Teledyne Princeton Instruments", Description = "Shows how to generate SPE files from raw data")]
    [QualificationData("IsSample", "True")]
    public class FileSample : AddInBase, ILightFieldAddIn
    {
        bool? toolBarState_;
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.DataToolBar; } }
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
        public override string UIDataToolBarTitle { get { return "File Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIDataToolBarIsChecked
        {
            get { return toolBarState_; }

            // The Button In LightField Was Pushed
            set { GenerateFiles(); }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override string UIDataToolBarToolTip
        {
            get { return "Generate a multi-frame single region file and a multi region single frame file sample"; }
        }
        ///////////////////////////////////////////////////////////////////////        
        public override bool UIDataToolBarIsEnabled{ get { return true; } }
        ///////////////////////////////////////////////////////////////////////        
        public override void UIDataToolBarExecute()
        {
            GenerateFiles();
        }        
        ////////////////////////////////////////////////////////////////////////
        //  The following routine demonstrates how to create files using the 
        //  LightField Addin SDK. 
        //
        //  Create 1 File with 2 Frames and 1 Region  (TwoFrameOneRoi.Spe)
        //  Create 1 File with 1 Frames and 2 Regions (OneFrameTwoRoi.Spe)        
        ////////////////////////////////////////////////////////////////////////
        private void GenerateFiles()
        {
            // Get the addin file manager
            var filemgr = LightFieldApplication.FileManager;
            if (filemgr != null)
            {
                ///////////////////////////////////////////////////////////////
                // Part 1: Two Frames 1 Region
                ///////////////////////////////////////////////////////////////                
                int[] w1 = { 100 };
                int[] h1 = { 200 };

                // Pseudo Frame 1 Region 1, Frame 2 Region 1
                ushort[] frame1 = new ushort[100 * 200];
                ushort[] frame2 = new ushort[100 * 200];
                for (int pix = 0; pix < 100 * 200; pix++)
                {
                    frame1[pix] = (ushort)pix;
                    frame2[pix] = (ushort)(pix * 2);
                }

                // Folder Selector
                var dialog = new System.Windows.Forms.FolderBrowserDialog();
                dialog.Description = "Please choose folder for resulting SPE file(s).";
                System.Windows.Forms.DialogResult result = dialog.ShowDialog();

                // Something bad happened we don't want to write the files.
                if (result != System.Windows.Forms.DialogResult.OK)
                    return;

                // Local variable containing path 
                string path = dialog.SelectedPath;

                // Create a file with 2 frames and the proper width and height
                // The file is initially created as empty and the user must load data to it. 
                RegionOfInterest roi = new RegionOfInterest(0, 0, w1[0], h1[0], 1, 1);
                RegionOfInterest[] rois = { roi };
                IImageDataSet TwoFrameOneRoi = filemgr.CreateFile(path + "\\TwoFrameOneRoi.spe",
                                                          rois,
                                                          2,                  // Frames
                                                          ImageDataFormat.MonochromeUnsigned16);                

                // Put Data to frame 1
                IImageData data1 = TwoFrameOneRoi.GetFrame(0, 0);
                data1.SetData(frame1);

                // Put Data to frame 2
                IImageData data2 = TwoFrameOneRoi.GetFrame(0, 1);
                data2.SetData(frame2);
                
                // Finally close this file
                filemgr.CloseFile(TwoFrameOneRoi);

                ///////////////////////////////////////////////////////////////
                // Part 2: 1 Frame 2 Regions
                ///////////////////////////////////////////////////////////////                
                int[] w2 = { 300, 500 };
                int[] h2 = { 400, 600 };

                // Pseudo Frame 2 Region 1
                ushort[] frame1_roi1 = new ushort[300 * 400];
                for (int pix = 0; pix < 300 * 400; pix++)
                    frame1_roi1[pix] = (ushort)pix;

                // Pseudo Frame 2 Region 2
                ushort[] frame1_roi2 = new ushort[500 * 600];
                for (int pix = 0; pix < 500 * 600; pix++)
                    frame1_roi2[pix] = (ushort)pix;

                // Create a file, get the buffer and fill it in for each region
                // The file is initially created as empty and the user must load data to it. 
                // The regions can not overlap
                RegionOfInterest r1 = new RegionOfInterest(0, 0, w2[0], h2[0], 1, 1);
                RegionOfInterest r2 = new RegionOfInterest(w2[0]+1, h2[0]+1, w2[1], h2[1], 1, 1);
                RegionOfInterest[] rois2 = { r1,r2 };
                IImageDataSet OneFrameTwoRoi = filemgr.CreateFile(path + "\\OneFrameTwoRoi.spe",
                                                         rois2,
                                                          1,                  // Frames
                                                          ImageDataFormat.MonochromeUnsigned16);

                // Put Data To Region 1
                IImageData data2_roi1 = OneFrameTwoRoi.GetFrame(0, 0);
                data2_roi1.SetData(frame1_roi1);

                // Data To Region 2
                IImageData data2_roi2 = OneFrameTwoRoi.GetFrame(1, 0);
                data2_roi2.SetData(frame1_roi2);

                // Finally close this file
                filemgr.CloseFile(OneFrameTwoRoi);
            }
        }
    }
}
