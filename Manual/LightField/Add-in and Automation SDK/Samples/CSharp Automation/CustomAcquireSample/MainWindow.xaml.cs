using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows;
using PrincetonInstruments.LightField.AddIns;
using PrincetonInstruments.LightField.Automation;

namespace Custom_Acquire_Sample_Automation_
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private IExperiment experiment_;
        private Automation automation_;
        private ILightFieldApplication application_;

        public MainWindow()
        {
            Cameras = new List<CameraSetup>();
            OpenLightFields = new List<OpenLightField>();
            IncrementFileName = 0;

            // Open one invisible instance of LightField
            var openLightField = new OpenLightField(this, visibleLightField: false);

            // return its automation object
            automation_ = openLightField.Auto;

            // return its experiment object
            experiment_ = openLightField.Experiment;

            // return its application object
            application_ = openLightField.Application;

            IsVisibleChanged += MainWindow_IsVisibleChanged;
        }

        private void MainWindow_IsVisibleChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            // Update list box when the main window becomes visible
            if ((bool)e.NewValue == true)
                UpdateListBox();

            IsVisibleChanged -= MainWindow_IsVisibleChanged;
        }

        /// <summary>
        /// Collection of all open LightFields
        /// </summary>
        private List<OpenLightField> OpenLightFields { get; set; }

        /// <summary>
        /// Collection of all cameras
        /// </summary>
        private List<CameraSetup> Cameras { get; set; }

        /// <summary>
        /// Used for unique file naming
        /// </summary>
        internal int IncrementFileName { get; set; }

        private void StopButton_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            // Get all running cameras
            var runningExperiments = Cameras.FindAll(p => p.Experiment.IsRunning);

            // Stop acquisition for all running cameras
            foreach (var experiment in runningExperiments)
                experiment.EndAcquisition();
        }

        private void StartButton_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            // Get all idle cameras
            var experimentsNotRunning = Cameras.FindAll(p => !p.Experiment.IsRunning);

            foreach (var experiment in experimentsNotRunning)
                // Run worker asynchronously to start acquisition
                experiment.StartAcquisitionWorker.RunWorkerAsync();
        }


        private void LaunchButton_Click(object sender, RoutedEventArgs e)
        {
            // Disable button after first use
            LaunchButton.IsEnabled = false;

            // Add all available experiments
            AddAvailableCameras();
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            // Close application
            Close();
            
            // Unhook event handlers from each object
            Cameras.ForEach(p => p.UnHookEvents());
            OpenLightFields.ForEach(p => p.UnHookEvents());
        }

        private void HideLFCheckbox_Checked(object sender, RoutedEventArgs e)
        {
            // controls visibility of first LightField instance
            if (IsLoaded)
                automation_.IsApplicationVisible = false;
        }

        private void HideLFCheckbox_OnUnchecked(object sender, RoutedEventArgs e)
        {
            // controls visibility of first LightField instance
            if (IsLoaded)
                automation_.IsApplicationVisible = true;
        }

        private void SuppressPromptCheckBox_Checked(object sender, RoutedEventArgs e)
        {
            // control suppression of messages from the first LightField instance
            if (IsLoaded)
                application_.UserInteractionManager.SuppressUserInteraction = true;
        }

        private void SuppressPromptCheckBox_OnUnchecked(object sender, RoutedEventArgs e)
        {
            // control suppression of messages from the first LightField instance
            if (IsLoaded)
                application_.UserInteractionManager.SuppressUserInteraction = false;
        }

        /// <summary>
        /// Update list box with available cameras
        /// </summary>
        private void UpdateListBox()
        {
            string cameraName = string.Empty;

            // Add available camera to the list box
            foreach (var camera in experiment_.AvailableDevices)
                if (experiment_.AvailableDevices.Count > 0 &&
                    camera.Type == DeviceType.Camera)
                {
                    cameraName =
                        string.Format("Model: {0}, SN: {1}",
                        camera.Model, camera.SerialNumber);

                    // Add camera identity to user list if it is not present
                    if (!AvaiableCamerasListBox.Items.Contains(cameraName))
                        AvaiableCamerasListBox.Items.Add(cameraName);
                }
        }

        /// <summary>
        /// Associate available cameras with automation and setup class
        /// Connect camera to LightField
        /// </summary>
        /// <param name="experiment"></param>
        /// <returns></returns>
        private void AddAvailableCameras()
        {            
            // Add available camera
            foreach (var camera in experiment_.AvailableDevices)
                if (experiment_.AvailableDevices.Count > 0 &&
                    camera.Type == DeviceType.Camera)
                {
                    experiment_ = new OpenLightField(this, visibleLightField:true).Experiment;

                    // Connect camera to LightField
                    experiment_.Add(camera);

                    string cameraName =
                        string.Format("Model: {0}, SN: {1}",
                        camera.Model, camera.SerialNumber);                    

                    // Assign background worker, identity, etc..
                    // through camera setup class
                    CameraSetup cameraSetup =
                        new CameraSetup(experiment_, this, cameraName);

                    experiment_ = cameraSetup.Experiment;
                }
        }

        /// <summary>
        /// Encapsulation of individual LightField instances
        /// </summary>
        class OpenLightField
        {
            internal Automation Auto { get; set; }
            internal ILightFieldApplication Application { get; set; }
            internal IExperiment Experiment { get; set; }
            internal bool VisibleLightField { get; set; }

            private MainWindow mainWindow_;

            public OpenLightField(MainWindow mainWindow, bool visibleLightField)
            {
                VisibleLightField = visibleLightField;
                mainWindow_ = mainWindow;

                OpenSingleInstance();

                // Add this LightField to the List of open LightFields
                mainWindow_.OpenLightFields.Add(this);
            }

            /// <summary>
            /// Creates and opens a new instance of LightField
            /// </summary>
            /// <returns>experiment</returns>
            private void OpenSingleInstance()
            {
                Automation();

                AutoApplication();

                Experiment = Application.Experiment;
            }

            /// <summary>
            /// Create a new automation object
            /// Hook closing event handler
            /// Set LightField to visible or invisible
            /// </summary>
            private void Automation()
            {
                // Create a new automation object
                // Set LightField to visible or invisible
                Auto = new Automation(VisibleLightField, new List<string> { "/empty" });

                // Hook closing event handler
                Auto.LightFieldClosing += auto_LightFieldClosing;
            }

            /// <summary>
            /// Return ILightFieldApplication object
            /// </summary>
            private void AutoApplication()
            {
                Application = Auto.LightFieldApplication;
            }

            private void auto_LightFieldClosing(object sender, LightFieldClosingEventArgs e)
            {
                // Prevent closing of any LightField instance
                e.Cancel = true;
            }

            /// <summary>
            /// Removes event/event handler association 
            /// </summary>
            internal void UnHookEvents()
            {
                Auto.LightFieldClosing -= auto_LightFieldClosing;

                Auto.Dispose();
            }
        }

        /// <summary>
        /// Class binding of individual experiment associations
        /// </summary>
        class CameraSetup
        {
            internal IExperiment Experiment { get; set; }
            internal string ExperimentName { get; set; }
            internal BackgroundWorker StartAcquisitionWorker { get; private set; }

            internal MainWindow mainWindow_;

            /// <summary>
            /// Constructor
            /// </summary>
            /// <param name="experiment"></param>
            /// <param name="mainWindow"></param>
            public CameraSetup(IExperiment experiment, MainWindow mainWindow, string experimentName)
            {
                Experiment = experiment;
                mainWindow_ = mainWindow;
                ExperimentName = experimentName;

                CreateAcquisitionBGW();
                SaveFileOptions();

                // Add camera setup to List
                mainWindow_.Cameras.Add(this);
            }

            /// <summary>
            /// Instantiate a new background worker for every experiment's start acquisition
            /// </summary>
            private void CreateAcquisitionBGW()
            {
                StartAcquisitionWorker = new BackgroundWorker();
                StartAcquisitionWorker.WorkerReportsProgress = false;
                StartAcquisitionWorker.WorkerSupportsCancellation = false;
                StartAcquisitionWorker.DoWork += startAcquisitionWorker__DoWork;
            }

            private void startAcquisitionWorker__DoWork(object sender, DoWorkEventArgs e)
            {
                // Acquire from passed in experiment/associated LightField
                if (Experiment.IsReadyToRun && !Experiment.IsUpdating && !Experiment.IsRunning)
                    Experiment.Acquire();
            }

            internal void EndAcquisition()
            {
                // End acquisition of passed in experiment/associated LightField
                Experiment.Stop();
            }

            /// <summary>
            /// Set file options for each LightField instance
            /// </summary>
            /// <param name="experiment"></param>
            private void SaveFileOptions()
            {
                // Option to Increment, set to false will not increment
                Experiment.SetValue(
                    ExperimentSettings.FileNameGenerationAttachIncrement,
                    true);

                // Increment on each file name
                Experiment.SetValue(
                    ExperimentSettings.FileNameGenerationIncrementNumber,
                    mainWindow_.IncrementFileName++);

                // Option to add date
                Experiment.SetValue(
                    ExperimentSettings.FileNameGenerationAttachDate,
                    true);

                // Option to add time
                Experiment.SetValue(
                    ExperimentSettings.FileNameGenerationAttachTime,
                    true);
            }

            /// <summary>
            /// Removes event/event handler association 
            /// </summary>
            internal void UnHookEvents()
            {
                StartAcquisitionWorker.DoWork -= startAcquisitionWorker__DoWork;
            }

            public override string ToString()
            {
                return ExperimentName;
            }
        }
    }
}
