using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples.Metadata_Sample
{
    /// <summary>
    /// Interaction logic for MetadataSample.xaml
    /// </summary>
    public partial class MetadataSample : UserControl
    {
        ILightFieldApplication app_;
        EventHandler<ExperimentCompletedEventArgs> acquireCompletedEventHandler_;
        ObservableCollection<StampData> stampCollection_ = new ObservableCollection<StampData>();

        public class StampData
        {
            public TimeSpan? ExposureStart  { get; set; }
            public TimeSpan? ExposureEnd    { get; set; }
            public long? Frame              { get; set; }
            public double? GateTrackingDelay{ get; set; }
            public double? GateTrackingWidth{ get; set; }
            public double? TrackingPhase    { get; set; }
        }
        public ObservableCollection<StampData> StampCollection
        { get { return stampCollection_; } }


        public MetadataSample(ILightFieldApplication application)
        {            
            app_ = application;
            InitializeComponent();
            textBoxFrames.Text = "5";
        }
        ///////////////////////////////////////////////////////////////////////
        bool ValidateAcquisition()
        {
            IDevice camera = null;
            foreach (IDevice device in app_.Experiment.ExperimentDevices)
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
            if (!app_.Experiment.IsReadyToRun)
            {
                MessageBox.Show("The system is not ready for acquisition, is there an error?");
                return false;
            }
            return true;
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire 5 Frames With Stamping On
        ///////////////////////////////////////////////////////////////////////
        private void button1_Click(object sender, RoutedEventArgs e)
        {
            // Are we in a state where we can acquire?
            if (!ValidateAcquisition())
                return;

            // Get the experiment object
            IExperiment experiment = app_.Experiment;
            if (experiment != null)
            {
                // Empty the time stamping collection
                stampCollection_.Clear();

                // Turn On Time Stamping
                experiment.SetValue(CameraSettings.AcquisitionTimeStampingStamps, TimeStamps.ExposureEnded | TimeStamps.ExposureStarted);

                // Turn On Frame Tracking
                experiment.SetValue(CameraSettings.AcquisitionFrameTrackingEnabled, true);

                // Don't Attach Date/Time
                experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, false);
                experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, false);

                // Save file as Specific.Spe to the default directory
                experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, "MetaDataSample");

                // Set the number of frames to 5
                experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, textBoxFrames.Text);

                // Connect Completion Event
                acquireCompletedEventHandler_ = new EventHandler<ExperimentCompletedEventArgs>(experiment_ExperimentCompleted);
                experiment.ExperimentCompleted += acquireCompletedEventHandler_;

                // Capture 5 Frames
                experiment.Acquire();
            }
        }
        ///////////////////////////////////////////////////////////////////////
        // Acquire Completed Handler        
        ///////////////////////////////////////////////////////////////////////
        void experiment_ExperimentCompleted(object sender, ExperimentCompletedEventArgs e)
        {
            ((IExperiment)sender).ExperimentCompleted -= acquireCompletedEventHandler_;

            IFileManager fileManager = app_.FileManager;
            if (fileManager != null)
            {
                // Get the recently acquired file list
                IList<string> files = fileManager.GetRecentlyAcquiredFileNames();

                // Open the last one if there is one
                if (files.Count != 0)
                {
                    // We can't update our observable collection here it must be done on this dispatcher not 
                    // from within this callback
                    Dispatcher.Invoke(
                        System.Windows.Threading.DispatcherPriority.Background,
                        new Action(delegate()
                        {
                            // Get the image dataset
                            IImageDataSet dataSet = fileManager.OpenFile(files[0], System.IO.FileAccess.Read);

                            // show the origin
                            origin.Text = dataSet.TimeStampOrigin.ToString();

                            // Display the Meta Data for each frame
                            for (int i = 0; i < dataSet.Frames; i++)
                            {
                                Metadata md = dataSet.GetFrameMetaData(i);

                                // by adding the meta data to the observable collection it appears in the listview
                                stampCollection_.Add(new StampData
                                {
                                    ExposureStart = md.ExposureStarted,
                                    ExposureEnd = md.ExposureEnded,
                                    Frame = md.FrameTrackingNumber,
                                    GateTrackingDelay = md.GateTrackingDelay,
                                    GateTrackingWidth = md.GateTrackingWidth,
                                    TrackingPhase = md.ModulationTrackingPhase
                                });
                            }
                        }));
                }
            }

        }   
    }
}
