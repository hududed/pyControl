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

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    /// <summary>
    /// Interaction logic for SystemBuildingSampleControl.xaml
    /// </summary>
    public partial class SystemBuildingSampleControl : Window
    {
        ILightFieldApplication application_;
        IExperiment experiment_;

        //////////////////////////////////////////////////////////////////////////////        
        // Modal Dialog Constructor
        //////////////////////////////////////////////////////////////////////////////        
        public SystemBuildingSampleControl(ILightFieldApplication app)
        {
            application_ = app;
            experiment_ = app.Experiment;

            InitializeComponent();

            // Initial Update
            RefreshListBoxes();

            // Connect to device changed event
            experiment_.AvailableDevicesChanged += Experiment_DeviceChanged;
            experiment_.ExperimentDevicesChanged += Experiment_DeviceChanged;

            // When the window gets closed
            Closed += SystemBuildingSampleControl_Closed;
        }
        //////////////////////////////////////////////////////////////////////////////        
        // Unregister from listening when the window closes
        //////////////////////////////////////////////////////////////////////////////        
        void SystemBuildingSampleControl_Closed(object sender, EventArgs e)
        {
            // Connect to device changed event
            experiment_.AvailableDevicesChanged -= Experiment_DeviceChanged;
            experiment_.ExperimentDevicesChanged -= Experiment_DeviceChanged;
        }
        //////////////////////////////////////////////////////////////////////////////        
        // If we got a device changed lets update our list boxes to reflect the 
        // new current state.
        //////////////////////////////////////////////////////////////////////////////
        void Experiment_DeviceChanged(object sender, DevicesChangedEventArgs e)
        {
            RefreshListBoxes();
        }
        //////////////////////////////////////////////////////////////////////////////        
        // Update List Box From Application
        //////////////////////////////////////////////////////////////////////////////
        private void RefreshListBoxes()
        {
            // Available List
            IList<IDevice> avail = application_.Experiment.AvailableDevices;
            AvailableList.Items.Clear();
            foreach (IDevice device in avail)
            {
                string s = string.Format("{0} {1} {2}", device.Model, device.SerialNumber, device.Type.ToString());
                AvailableList.Items.Add(s);
            }
            // Experiment List
            IList<IDevice> exper = application_.Experiment.ExperimentDevices;
            ExperimentList.Items.Clear();
            foreach (IDevice device in exper)
            {
                string s = string.Format("{0} {1} {2}", device.Model, device.SerialNumber, device.Type.ToString());
                ExperimentList.Items.Add(s);
            }
        }
        //////////////////////////////////////////////////////////////////////////////        
        // Add From Available To Experiment
        //////////////////////////////////////////////////////////////////////////////
        private void Add_Click(object sender, RoutedEventArgs e)
        {
            int idx   = AvailableList.SelectedIndex;
            int count = application_.Experiment.AvailableDevices.Count;

            // Validate index
            if ((idx >= 0) && (idx < count))
            {
                application_.Experiment.Add(application_.Experiment.AvailableDevices[idx]);
                RefreshListBoxes();
            }
        }
        //////////////////////////////////////////////////////////////////////////////        
        // Remove From Experiment
        //////////////////////////////////////////////////////////////////////////////
        private void Remove_Click(object sender, RoutedEventArgs e)
        {
            int idx   = ExperimentList.SelectedIndex;
            int count = application_.Experiment.ExperimentDevices.Count;

            // Validate index
            if ((idx >= 0) && (idx < count))
            {
                application_.Experiment.Remove(application_.Experiment.ExperimentDevices[idx]);
                RefreshListBoxes();
            }
        }
        //////////////////////////////////////////////////////////////////////////////        
        // Clear All Experiment
        //////////////////////////////////////////////////////////////////////////////
        private void ClearAll_Click(object sender, RoutedEventArgs e)
        {
            application_.Experiment.Clear();
            RefreshListBoxes();
        }
        
    }
}
