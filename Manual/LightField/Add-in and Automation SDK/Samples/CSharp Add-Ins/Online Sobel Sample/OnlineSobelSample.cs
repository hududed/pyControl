using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.AddIn;
using System.AddIn.Pipeline;
using System.Windows;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    ///////////////////////////////////////////////////////////////////////////
    //  This sample hooks into the data stream when data is being acquired or 
    // displayed and modifies the data by performing a sobel edge detection on 
    // the buffer(s). This is a menu driven addin and sets up a check box menu 
    // item as its source of control.
    //
    //  Notes: It will only sobel transform the first region of interest.
    //         It must be connected before acquiring or focusing, turning it
    //         on after the acquisition is started will do nothing.    
    //
    //  This sample shows how to inject your code into the LightField data 
    //  stream and modify the data.
    //
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Online Sobel Sample (C#)", 
            Version     = "1.0.0",
            Publisher   = "Teledyne Princeton Instruments",
            Description = "Shows how to patch into the data stream and modify data as it passes through the add-in\nThis simply does a Sobel process on the data")]
    [QualificationData("IsSample", "True")]
    public class AddinMenuSobel : AddInBase, ILightFieldAddIn
    {
        bool? processEnabled_;
        bool menuEnabled_;
        RemotingSobelTransformation sobelTransformer_;        
        IExperiment experiment_;
        
        ///////////////////////////////////////////////////////////////////////
        public UISupport UISupport { get { return UISupport.Menu; } }
        ///////////////////////////////////////////////////////////////////////
        public void Activate(ILightFieldApplication app)
        {
            // Capture Interface
            LightFieldApplication   = app;
            experiment_             = app.Experiment;
            menuEnabled_            = CheckSystem();
            processEnabled_         = false; 
            
            // Create transformation object if we have a camera (via menu enabled)
            if (menuEnabled_)
                CreateTransformationObject();

            // Listen to region of interest result changed and re-compute the buffers to match the 
            // region
            List<string> settings = new List<string>();
            settings.Add(CameraSettings.ReadoutControlRegionsOfInterestResult);
            experiment_.FilterSettingChanged(settings);
            experiment_.SettingChanged += experiment__SettingChanged;

            // Connect to experiment device changed (when camera is added this add-in is active, and 
            // if a camera is removed then this add-in is disabled.
            experiment_.ExperimentUpdated += experiment__ExperimentUpdated;

            // Connect to the data received event
            experiment_.ImageDataSetReceived += experimentDataReady;
        }
        ///////////////////////////////////////////////////////////////////////
        void experiment__ExperimentUpdated(object sender, ExperimentUpdatedEventArgs e)
        {
            bool hasCamera = CheckSystem();

            // Update on change only
            if (menuEnabled_ != hasCamera)
            {
                menuEnabled_ = hasCamera;
                RequestUIRefresh(UISupport.Menu);
            }
            // Building a system can change the sensor dimensions 
            if (hasCamera)
                CreateTransformationObject();
        }
        ///////////////////////////////////////////////////////////////////////
        void experiment__SettingChanged(object sender, SettingChangedEventArgs e)
        {            
            if (CheckSystem())
                CreateTransformationObject();            
        }       
        ///////////////////////////////////////////////////////////////////////
        public void Deactivate() 
        { 
            // Stop listening to device changes
            experiment_.ExperimentUpdated -= experiment__ExperimentUpdated;

            // Stop snooping settings
            experiment_.FilterSettingChanged(new List<string>());
            experiment_.SettingChanged -= experiment__SettingChanged;

            // Disconnect Data Event            
            experiment_.ImageDataSetReceived -= experimentDataReady;
        }
        ///////////////////////////////////////////////////////////////////////
        public override string UIMenuTitle { get { return "Online Sobel Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool UIMenuIsEnabled { get { return menuEnabled_; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIMenuIsChecked
        {
            get { return processEnabled_;  }
            set { processEnabled_ = value; }
        }        
        ///////////////////////////////////////////////////////////////////////        
        internal bool CheckSystem()
        {
            foreach (IDevice device in LightFieldApplication.Experiment.ExperimentDevices)
            {
                if (device.Type == DeviceType.Camera)
                    return true;
            }
            // No Camera return false
            return false;            
        }
        ///////////////////////////////////////////////////////////////////////        
        //  With all of the data in the block, transform it all        
        ///////////////////////////////////////////////////////////////////////
        void experimentDataReady(object sender, ImageDataSetReceivedEventArgs e)
        {
            if (processEnabled_ == true) // NO-OP if its off on this event
            {                
                // Are we transforming the data? Transform all frames in the package           
                for (int i = 0; i < (int)e.ImageDataSet.Frames; i++)
                    for (int roi = 0; roi < e.ImageDataSet.Regions.Length; roi++)
                        sobelTransformer_.Transform(e.ImageDataSet.GetFrame(roi, i), roi);

            }
        }
        ///////////////////////////////////////////////////////////////////
        private void CreateTransformationObject()
        {
            // Initialize Online Process and create transformation class
            RegionOfInterest[] rois = experiment_.SelectedRegions;
            sobelTransformer_ = new RemotingSobelTransformation(rois);
        }
    }
    ///////////////////////////////////////////////////////////////////////
    //
    //  Perform a Sobel Transformation on all regions
    //
    ///////////////////////////////////////////////////////////////////////
    public class RemotingSobelTransformation
    {
        static int[][,,] indexBuffers_;
        static ushort[][] retDataUs_;
        static uint[][] retDataI_;
        static float[][] retDataF_;
        
        // Matrices
        ///////////////////////////////////////////////////////////////////////
        double[] gy = new double[]  { -1, -2, -1,  0, 0, 0,  1, 2, 1 };
        double[] gx = new double[]  { -1,  0,  1, -2, 0, 2, -1, 0, 1 };
        int[] xs    = new int[]     { -1,  0,  1, -1, 0, 1, -1, 0, 1 };
        int[] ys    = new int[]     { -1, -1, -1,  0, 0, 0,  1, 1, 1 };
        ///////////////////////////////////////////////////////////////////////
        // Build Buffers of Indexes On Construction For Speed
        ///////////////////////////////////////////////////////////////////////
        public RemotingSobelTransformation(RegionOfInterest[] rois)
        {
            // Allocate outer buffers
            indexBuffers_ = new int[rois.Length][,,];
            retDataUs_    = new ushort[rois.Length][];
            retDataI_     = new uint[rois.Length][];
            retDataF_     = new float[rois.Length][];

            for (int roiIndex = 0; roiIndex < rois.Length; roiIndex++)
            {
                int dW = rois[roiIndex].Width / rois[roiIndex].XBinning;
                int dH = rois[roiIndex].Height / rois[roiIndex].YBinning;

                // Static Computed Once Upon Starting or roi changing
                // Compute all of the indexes ahead of time, this makes the 
                // code to do the process 10 times faster or more.
                if ((indexBuffers_[roiIndex] == null) || (indexBuffers_[roiIndex].Length != dW * dH * 9))
                {
                    indexBuffers_[roiIndex] = new int[dW, dH, 9];
                    for (int xx = 2; xx < dW - 2; xx++)
                    {
                        for (int yy = 2; yy < dH - 2; yy++)
                        {
                            for (int i = 0; i < 9; i++)
                            {
                                int index = (xx + xs[i]) + (yy + ys[i]) * dW;
                                indexBuffers_[roiIndex][xx, yy, i] = index;
                            }
                        }
                    }                   
                }
                // Output Data Buffers
                retDataUs_[roiIndex] = new ushort[dW * dH];
                retDataI_[roiIndex]  = new uint[dW * dH];
                retDataF_[roiIndex]  = new float[dW * dH];
            }            
        }
        ///////////////////////////////////////////////////////////////////////
        // Perform the actual transformation
        ///////////////////////////////////////////////////////////////////////
        public void Transform(IImageData data, int roi)
        {
            // Hint use locals (accessing on Interface forces boundary crossing)
            // that will be unbearably slow.
            int dW = data.Width;    // Boundary Crossing
            int dH = data.Height;   // Boundary Crossing

            switch (data.Format)
            {
                case ImageDataFormat.MonochromeUnsigned16:
                    {
                        ushort[] ptr = (ushort[])data.GetData();     // Input Data

                        // Loop Width & Height(Quick and Dirty Padding Of 2) 
                        // This Avoids a lot of boundary checking or reflection and increases speed
                        for (int xx = 2; xx < dW - 2; xx++)
                        {
                            for (int yy = 2; yy < dH - 2; yy++)
                            {
                                double GY = 0, GX = 0;
                                // Compute the X and Y Components
                                for (int i = 0; i < 9; i++)
                                {
                                    int idx = indexBuffers_[roi][xx, yy, i];
                                    GY += ptr[idx] * gy[i];
                                    GX += ptr[idx] * gx[i];
                                }
                                // Magnitude
                                double G = Math.Sqrt(GX * GX + GY * GY);

                                // Put the Magnitude into the output buffer
                                retDataUs_[roi][yy * dW + xx] = (ushort)G;
                            }
                        }
                        // Write the output buffer to the IImageData
                        // Boundary Crossing
                        data.SetData(retDataUs_[roi]);
                    }
                    break;

                case ImageDataFormat.MonochromeUnsigned32:
                    {
                        uint[] ptr = (uint[])data.GetData();     // Input Data

                        // Loop Width & Height(Quick and Dirty Padding Of 2) 
                        // This Avoids a lot of boundary checking or reflection and increases speed
                        for (int xx = 2; xx < dW - 2; xx++)
                        {
                            for (int yy = 2; yy < dH - 2; yy++)
                            {
                                double GY = 0, GX = 0;
                                // Compute the X and Y Components
                                for (int i = 0; i < 9; i++)
                                {
                                    int idx = indexBuffers_[roi][xx, yy, i];
                                    GY += ptr[idx] * gy[i];
                                    GX += ptr[idx] * gx[i];
                                }
                                // Magnitude
                                double G = Math.Sqrt(GX * GX + GY * GY);

                                // Put the Magnitude into the output buffer
                                retDataI_[roi][yy * dW + xx] = (uint)G;
                            }
                        }
                        // Write the output buffer to the IImageData
                        // Boundary Crossing
                        data.SetData(retDataI_[roi]);
                    }
                    break;

                case ImageDataFormat.MonochromeFloating32:
                    {
                        float[] ptr = (float[])data.GetData();     // Input Data

                        // Loop Width & Height(Quick and Dirty Padding Of 2) 
                        // This Avoids a lot of boundary checking or reflection and increases speed
                        for (int xx = 2; xx < dW - 2; xx++)
                        {
                            for (int yy = 2; yy < dH - 2; yy++)
                            {
                                double GY = 0, GX = 0;
                                // Compute the X and Y Components
                                for (int i = 0; i < 9; i++)
                                {
                                    int idx = indexBuffers_[roi][xx, yy, i];
                                    GY += ptr[idx] * gy[i];
                                    GX += ptr[idx] * gx[i];
                                }
                                // Magnitude
                                double G = Math.Sqrt(GX * GX + GY * GY);

                                // Put the Magnitude into the output buffer
                                retDataF_[roi][yy * dW + xx] = (float)G;
                            }
                        }
                        // Write the output buffer to the IImageData
                        // Boundary Crossing
                        data.SetData(retDataF_[roi]);
                    }
                    break;
            }
        }        
    }   
}

