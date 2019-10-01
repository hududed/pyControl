using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples.Acquire_Sync_Sample
{
    /// <summary>
    /// Interaction logic for AcquireSyncSample.xaml
    /// </summary>
    public partial class AcquireSyncSample : UserControl
    {
        ILightFieldApplication application_;

        public AcquireSyncSample(ILightFieldApplication app)
        {
            InitializeComponent();
            application_ = app;
        }
        ///////////////////////////////////////////////////////////////////////
        bool ValidateAcquisition()
        {
            IDevice camera = null;
            foreach (IDevice device in application_.Experiment.ExperimentDevices)
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
            if (!application_.Experiment.IsReadyToRun)
            {
                MessageBox.Show("The system is not ready for acquisition, is there an error?");
                return false;
            }
            return true;
        }
        ///////////////////////////////////////////////////////////////////////
        // Synchronous Full Frame Acquire      
        ///////////////////////////////////////////////////////////////////////
        private void AcquireFullFrameSync(object sender, RoutedEventArgs e)
        {
            // Are we in a state we can do this?
            if (!ValidateAcquisition())
                return;

            // Get the experiment object
            IExperiment experiment = application_.Experiment;

            // Full Frame
            experiment.SetFullSensorRegion();

            int images = 3;
            int frames = 1;

            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, frames);

            for (int i = 1; i <= images; i++)
            {
                // Capture 1 Frame
                IImageDataSet set = experiment.Capture(frames);

                // Stop processing if we do not have all frames
                if (set.Frames != frames)
                {
                    // Clean up the image data set                    
                    set.Dispose();

                    throw new ArgumentException("Frames are not equal");
                }

                // Get the data from the current frame
                Array imageData = set.GetFrame(0, frames - 1).GetData();

                //  Cache the frame
                IImageData imageFrame = set.GetFrame(0, frames - 1);

                PrintData(imageData, imageFrame, i, images);
            }
        }
        ///////////////////////////////////////////////////////////////////////
        private void PrintData(Array imageData, IImageData imageFrame,
            int iteration, int acquisitions)
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
                iteration, acquisitions, pixel1, pixel2, pixel3);

            MessageBox.Show(message);
        }
        ///////////////////////////////////////////////////////////////////////
    }
}
