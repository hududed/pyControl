using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using PrincetonInstruments.LightField.AddIns;
using System.IO;

namespace LightFieldAddInSamples.Acquire_Async_Sample
{
    /// <summary>
    /// Interaction logic for AsynAcquireSample.xaml
    /// </summary>
    public partial class AsynAcquireSample : UserControl
    {
        ILightFieldApplication application_;
        IExperiment experiment_;
        int totalAcquisitions_, acquisitionsCompleted_, frames_;
        IFileManager fileManager_;
        ///////////////////////////////////////////////////////////////////////
        // Constructor (Pull the experiment out of the app and store it for 
        // use)
        ///////////////////////////////////////////////////////////////////////
        public AsynAcquireSample(ILightFieldApplication app)
        {
            InitializeComponent();
            application_ = app;
            experiment_ = application_.Experiment;
            fileManager_ = application_.FileManager;
        }
        ///////////////////////////////////////////////////////////////////////
        bool ValidateAcquisition()
        {
            IDevice camera = null;
            foreach (IDevice device in experiment_.ExperimentDevices)
            {
                if (device.Type == DeviceType.Camera)
                    camera = device;
            }
            ///////////////////////////////////////////////////////////////////////
            if (camera == null)
            {
                MessageBox.Show("This sample requires a camera!");
                return false;
            }
            ///////////////////////////////////////////////////////////////////////
            if (!experiment_.IsReadyToRun)
            {
                MessageBox.Show("The system is not ready for acquisition, is there an error?");
                return false;
            }
            return true;
        }
        ///////////////////////////////////////////////////////////////////////
        //  Acquire Full Chip Asynchronously
        ///////////////////////////////////////////////////////////////////////
        private void AcquireAsync_Click(object sender, RoutedEventArgs e)
        {
            // Can we do this?
            if (!ValidateAcquisition())
                return;

            // In case a previous run was not completed make sure we start out not listening
            experiment_.ExperimentStarted -= exp_AcquisitionStarted;
            experiment_.ExperimentCompleted -= exp_AcquisitionComplete;

            acquisitionsCompleted_ = 0;
            totalAcquisitions_ = 3;
            frames_ = 1;

            // We want unique file names for this
            experiment_.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, true);

            // Set number of frames
            experiment_.SetValue(ExperimentSettings.AcquisitionFramesToStore, frames_);

            // Connect Completion Event
            experiment_.ExperimentStarted += exp_AcquisitionStarted;

            // Begin the acquisition (Note: current exposure, frames, filename etc will be used)
            experiment_.Acquire();
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire Completed Handler
        // This just fires a message saying that the data is acquired.
        ///////////////////////////////////////////////////////////////////////
        void exp_AcquisitionComplete(object sender, ExperimentCompletedEventArgs e)
        {
            // We can not call acquire in the completed handler, it must be deferred because 
            // the current acquisition will not be considered complete until this handler has
            // returned.
            Dispatcher.BeginInvoke(DispatcherPriority.Background, (Action)(() =>
            {
                acquisitionsCompleted_++;
                ShowImageDataFromLastAcquire();

                // Disconnect from the completed as the start event will reconnect
                experiment_.ExperimentCompleted -= exp_AcquisitionComplete;

                // Start the next one
                if (acquisitionsCompleted_ < totalAcquisitions_)
                    experiment_.Acquire();

                // Or no starts and disconnect starting as the next button click
                // will reconnect started.
                else
                    experiment_.ExperimentStarted -= exp_AcquisitionStarted;
            }));
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire Started Handler this connects up the completed handler    
        ///////////////////////////////////////////////////////////////////////
        void exp_AcquisitionStarted(object sender, ExperimentStartedEventArgs e)
        {
            experiment_.ExperimentCompleted += exp_AcquisitionComplete;
        }
        ///////////////////////////////////////////////////////////////////////
        // The first index of the filemanager's GetRecentlyAcquireFileNames is
        // always the last file acquired..
        ///////////////////////////////////////////////////////////////////////
        void ShowImageDataFromLastAcquire()
        {
            // Expected resulting file name
            string resultName
                = (string)experiment_.GetValue(ExperimentSettings.AcquisitionOutputFilesResult);

            // Open the last acquired file
            IList<string> files
                = fileManager_.GetRecentlyAcquiredFileNames();

            // Is our result in the acquired
            if (files.Contains(resultName))
            {
                //  Open file
                IImageDataSet dataSet
                    = fileManager_.OpenFile(resultName, FileAccess.Read);

                // Stop processing if we do not have all frames
                if (dataSet.Frames != frames_)
                {
                    // Close the file
                    fileManager_.CloseFile(dataSet);

                    throw new ArgumentException("Frames are not equal");
                }

                //  Cache image data
                Array imageData
                    = dataSet.GetFrame(0, frames_ - 1).GetData();

                //  Cache the frame
                IImageData imageFrame
                    = dataSet.GetFrame(0, frames_ - 1);

                //  Print some of the cached data
                PrintData(imageData, imageFrame);

                // Close the file
                fileManager_.CloseFile(dataSet);
            }
        }
        ///////////////////////////////////////////////////////////////////////
        private void PrintData(Array imageData, IImageData imageFrame)
        {
            //  Calculate center
            int centerPixel = ((imageFrame.Height / 2 - 1) * imageFrame.Width) + imageFrame.Width / 2;

            //  Last Pixel
            int lastPixel = (imageFrame.Width * imageFrame.Height) - 1;

            //  First Pixel
            string pixel1 = string.Format("\nFirst Pixel Intensity: {0}",
                imageData.GetValue(0));

            //  Center Pixel, zero based
            string pixel2 =
                string.Format("\nCenter Pixel Intensity: {0}",
                imageData.GetValue(centerPixel));

            //  Last Pixel
            string pixel3 =
                string.Format("\nLast Pixel Intensity: {0}",
                imageData.GetValue(lastPixel));

            //  Create message
            string message =
                string.Format("Acquire {0} of {1} Completed {2} {3} {4}",
                acquisitionsCompleted_, totalAcquisitions_, pixel1, pixel2, pixel3);

            MessageBox.Show(message);
        }
        ///////////////////////////////////////////////////////////////////////
    }
}
