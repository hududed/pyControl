using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.AddIn;
using System.AddIn.Pipeline;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Xml;
using System.Xml.XPath;
using System.Xml.Linq;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{    
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////
    [AddIn("Spectroscopy Sample (C#)",
    Version = "1.0.0",
    Publisher = "Teledyne Princeton Instruments",
    Description= "Shows how to work with wavelength calibrated data")]
    [QualificationData("IsSample", "True")]
    public class AddinSpectroscopySample : AddInBase, ILightFieldAddIn
    {        
        bool? toolBarState_;
        EventHandler<ExperimentCompletedEventArgs> acquireCompletedEventHandler_;

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
        public override string UIApplicationToolBarTitle { get { return "Spectroscopy Sample"; } }
        ///////////////////////////////////////////////////////////////////////
        public override bool? UIApplicationToolBarIsChecked
        {
            get { return toolBarState_; }
            set { toolBarState_ = value; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override void UIApplicationToolBarExecute()
        {
            IExperiment experiment = LightFieldApplication.Experiment;

            // 1.) Acquire image with calibration(You have to know you have it the sample
            //     can not help you with that.
            //------------------------------------------------------------------------------            
            acquireCompletedEventHandler_ = new EventHandler<ExperimentCompletedEventArgs>(experiment_ExperimentCompleted);
            experiment.ExperimentCompleted += acquireCompletedEventHandler_;

            // Take data now
            experiment.Acquire();
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire Completed Handler        
        ///////////////////////////////////////////////////////////////////////
        void experiment_ExperimentCompleted(object sender, ExperimentCompletedEventArgs e)
        {
            ((IExperiment)sender).ExperimentCompleted -= acquireCompletedEventHandler_;

            IFileManager fileManager = LightFieldApplication.FileManager;
            if (fileManager != null)
            {
                // 2.) Find the image ----------------------------------------------------------
                //------------------------------------------------------------------------------            
                // Get the recently acquired file list
                IList<string> files = fileManager.GetRecentlyAcquiredFileNames();                
                if (files.Count != 0)
                {
                    double[] waveLengths;
                    double[] errors;

                    // 3.) Get the xml out of the image and from that pull the calibration/error---
                    //-----------------------------------------------------------------------------            
                    // Get the image dataset
                    IImageDataSet dataSet = fileManager.OpenFile(files[0], System.IO.FileAccess.Read);
                    GetCalibrationAndError(dataSet, out waveLengths, out errors);
                                                            
                    // 4.) Create a new file of user data
                    //------------------------------------------------------------------------------ '
                    CreateCalibratedFile(waveLengths, errors);                                               
                }
            }
        }
       
        ///////////////////////////////////////////////////////////////////////
        public override bool UIApplicationToolBarIsEnabled { get { return true; } }
        ///////////////////////////////////////////////////////////////////////
        public override string UIApplicationToolBarToolTip
        {
            get { return "Get/Set the calibration data on a file to show an example of how to work with wavelength calibrated data"; }
        }
        ///////////////////////////////////////////////////////////////////////
        public override int? UIApplicationToolBarHelpTopicID { get { return 1; } }

        ///////////////////////////////////////////////////////////////////////
        private void CreateCalibratedFile(double [] calibration, double [] errors)
        {
            // No Calibration So Make Something up
            if (calibration == null)
            {
                calibration = new double[720];
                for (int i = 0; i < 720; i++)
                    calibration[i] = i * 3.0;
            }

            // Size of data passed in
            ushort[] cosine = new ushort[calibration.Length];

            // Generate Curves (Amplitude 100)
            for (int pix = 0; pix < calibration.Length; pix++)
            {
                // Convert To Angle
                double angle = Math.PI * ((double)pix - 360) / 180.0;
                // Compute Points
                cosine[pix] = (ushort)((double)100 * (Math.Cos(angle) + (double)1));
            }

            // Mkae a region of interest (Single Strip)
            RegionOfInterest roi = new RegionOfInterest(0, 0, calibration.Length, 1, 1, 1);
            
            // Get the file manager
            var filemgr = LightFieldApplication.FileManager;
            if (filemgr != null)
            {
                RegionOfInterest[] rois = { roi };
                string root = (string)LightFieldApplication.Experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory);
                IImageDataSet calSampleData =  filemgr.CreateFile(root + "\\CalibrationSample.Spe", rois, 1, ImageDataFormat.MonochromeUnsigned16);

                // Put Data to frame 1
                IImageData data1 = calSampleData.GetFrame(0, 0);
                data1.SetData(cosine);

                // Update The XML for the new document
                SetCalibrationAndError(calSampleData, calibration, errors);

                // Close the file
                filemgr.CloseFile(calSampleData);
            }            
        }
        ///////////////////////////////////////////////////////////////////////
        public void GetCalibrationAndError( IImageDataSet dataSet, 
                                            out double[] waveLengths, 
                                            out double[] errors)
        {
            // Start off empty
            errors = null;
            waveLengths = null;

            string xmlText = LightFieldApplication.FileManager.GetXml(dataSet);
            // Create a new XML Document
            XmlDocument xDoc = new XmlDocument();

            // Convert to proper encoding buffer
            byte[] byteArray = new byte[xmlText.Length];
            var encoding = Encoding.UTF8;
            byteArray = encoding.GetBytes(xmlText);

            // Convert to Memory Stream
            MemoryStream memoryStream = new MemoryStream(byteArray);
            memoryStream.Seek(0, SeekOrigin.Begin);

            // Load The XmlDocument
            xDoc.Load(memoryStream);

            // Create an XmlNamespaceManager to resolve the default namespace.
            XmlNamespaceManager nsmgr = new XmlNamespaceManager(xDoc.NameTable);
            nsmgr.AddNamespace("pi", @"http://www.princetoninstruments.com/spe/2009");

            // Find Calibrations
            XmlNode calRoot = xDoc.SelectSingleNode("//pi:Calibrations", nsmgr);
            if (calRoot != null)
            {
                // Get WavelengthMapping
                XmlNode waveMapping = calRoot.SelectSingleNode("//pi:WavelengthMapping", nsmgr);
                if (waveMapping != null)
                {
                    // Get Wavelength Errors (wave0,error0 wave1,error1 wave2,error2 ....
                    //--------------------------------------------------------------------------
                    XmlNode waveErrors = waveMapping.SelectSingleNode("//pi:WavelengthError", nsmgr);
                    if (waveErrors != null)
                    {
                        string[] pairs = waveErrors.InnerText.Split(' ');

                        waveLengths = new double[pairs.Count()];
                        errors = new double[pairs.Count()];

                        if ((pairs != null) && (pairs.Count() > 0))
                        {
                            for (int i = 0; i < pairs.Count(); i++)
                            {
                                string[] temp = pairs[i].Split(',');

                                waveLengths[i] = XmlConvert.ToDouble(temp[0]);
                                errors[i] = XmlConvert.ToDouble(temp[1]); 
                            }
                        }
                    }
                    // No Errors
                    //--------------------------------------------------------------------------
                    else
                    {
                        XmlNode waves = waveMapping.SelectSingleNode("//pi:Wavelength", nsmgr);
                        if (waves != null)
                        {
                            // Readin values into array
                            string[] split = waves.InnerText.Split(',');
                            waveLengths = new double[split.Length];

                            // Convert to doubles
                            for (int i = 0; i < split.Length; i++)
                                waveLengths[i] = XmlConvert.ToDouble(split[i]); 
                        }
                    }
                }
            }
        }
        ///////////////////////////////////////////////////////////////////////
        public void SetCalibrationAndError(IImageDataSet dataSet, double[] waveLengths, double[] errors)
        {
            // Get the text file
            string xmlText = LightFieldApplication.FileManager.GetXml(dataSet);

            // Create a new XML Document
            XmlDocument xDoc = new XmlDocument();

            // Convert to proper encoding buffer
            byte[] byteArray = new byte[xmlText.Length];
            var encoding = Encoding.UTF8;
            byteArray = encoding.GetBytes(xmlText);

            // Convert to Memory Stream
            MemoryStream memoryStream = new MemoryStream(byteArray);
            memoryStream.Seek(0, SeekOrigin.Begin);

            // Load The XmlDocument
            xDoc.Load(memoryStream);

            // Create an XmlNamespaceManager to resolve the default namespace.
            XmlNamespaceManager nsmgr = new XmlNamespaceManager(xDoc.NameTable);
            nsmgr.AddNamespace("pi", @"http://www.princetoninstruments.com/spe/2009");
            
            // Find Calibrations
            XmlNode calRoot = xDoc.SelectSingleNode("//pi:Calibrations", nsmgr);
            if (calRoot != null)
            {
                // Get WavelengthMapping
                XmlNode waveMapping = calRoot.SelectSingleNode("//pi:WavelengthMapping", nsmgr);

                // Create if it is non existing
                if (waveMapping == null)
                {
                    waveMapping = xDoc.CreateNode(XmlNodeType.Element, "WavelengthMapping", @"http://www.princetoninstruments.com/spe/2009");
                    calRoot.AppendChild(waveMapping);
                }
                if (waveMapping != null)
                {
                    // Set Wavelength Errors (wave0,error0 wave1,error1 wave2,error2 ....
                    //--------------------------------------------------------------------------
                    if (errors != null)
                    {
                        // Get Wavelength Errors
                        XmlNode waveErrors = waveMapping.SelectSingleNode("//pi:WavelengthError", nsmgr);

                        // Create if it is non existing and needed
                        if (waveErrors == null)
                        {
                            waveErrors = xDoc.CreateNode(XmlNodeType.Element, "WavelengthError", @"http://www.princetoninstruments.com/spe/2009");
                            waveMapping.AppendChild(waveErrors);
                        }

                        if (waveErrors != null)
                        {
                            string errorString = string.Empty;                            
                            for (int i = 0; i < errors.Length; i++)
                            {
                                errorString += waveLengths[i].ToString() + ',' + errors[i].ToString();

                                // Space for next pair if not last one
                                if (i != errors.Length - 1)
                                    errorString += ' ';
                            }
                            waveErrors.InnerText = errorString;
                        }
                    }
                    //--------------------------------------------------------------------------
                    else
                    {
                        XmlNode waves = waveMapping.SelectSingleNode("//pi:Wavelength", nsmgr);

                        // Create if it is non existing
                        if (waves == null)
                        {
                            waves = xDoc.CreateNode(XmlNodeType.Element, "Wavelength", @"http://www.princetoninstruments.com/spe/2009");
                            waveMapping.AppendChild(waves);
                        }
                        if (waves != null)
                        {
                            string waveString = string.Empty;                            
                            for (int i = 0; i < waveLengths.Length; i++)
                            {
                                waveString += waveLengths[i].ToString();
                                if (i != waveLengths.Length - 1)
                                    waveString += ',';
                            }
                            waves.InnerText = waveString;
                        }
                    }
                }                
            }
            // Finally Update the document with the new xml
            LightFieldApplication.FileManager.SetXml(dataSet, xDoc.InnerXml);

        }
    }
}
