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

namespace LightFieldAddInSamples.Regions_Of_Interest_Sample
{
    /// <summary>
    /// Interaction logic for RegionControl.xaml
    /// </summary>
    public partial class RegionControl : UserControl
    {
       ILightFieldApplication application_;
       IExperiment experiment_;
       int xbin_, ybin_;
       int rowsbinned_;
       int x_, y_, w_, h_, xb_, yb_;

       bool controlsInitialized_;

       bool CameraExist
       {
           get            
           { 
               bool exist = experiment_.Exists(CameraSettings.AcquisitionFrameRate);

               if (exist && !controlsInitialized_)
               {
                   controlsInitialized_ = true;

                   // Get The Full Size
                   RegionOfInterest full = experiment_.FullSensorRegion;

                   // Full Sensor Binned
                   RegionOfInterest binned = experiment_.BinnedSensorRegion;
                   xbin_ = binned.XBinning;
                   ybin_ = binned.YBinning;
                   FullSensorBinW.Text = xbin_.ToString();
                   FullSensorBinH.Text = ybin_.ToString();

                   // Line Sensor
                   RegionOfInterest line = experiment_.LineSensorRegion;
                   rowsbinned_ = line.YBinning;
                   RowsBinnedH.Text = rowsbinned_.ToString();

                   // Custom Region
                   RegionOfInterest[] custom = experiment_.CustomRegions;
                   x_ = custom[0].X;
                   RegionX.Text = x_.ToString();

                   w_ = custom[0].Width;
                   RegionWidth.Text = w_.ToString();

                   xb_ = custom[0].XBinning;
                   XBin.Text = xb_.ToString();

                   y_ = custom[0].Y;
                   RegionY.Text = y_.ToString();

                   h_ = custom[0].Height;
                   RegionHeight.Text = h_.ToString();

                   yb_ = custom[0].YBinning;
                   YBin.Text = yb_.ToString();                   
               }               
               
               return exist;
           }           
       }
       public RegionControl(ILightFieldApplication app)
       {
            application_ = app;
            InitializeComponent();

            // nab the experiment since we need it for everything
            experiment_ = application_.Experiment;

            bool bExist = CameraExist;
            
            // Set Full Chip
            FullChip.IsChecked = true;
        }

        private void radioButton1_Checked(object sender, RoutedEventArgs e)
        {
            if (CameraExist)
                experiment_.SetFullSensorRegion();            
        }

        private void FullSensorBinned_Checked(object sender, RoutedEventArgs e)
        {
            if (CameraExist)
                experiment_.SetBinnedSensorRegion(xbin_, ybin_);
        }

        private void RowsBinned_Checked(object sender, RoutedEventArgs e)
        {
            if (CameraExist)
                experiment_.SetLineSensorRegion(rowsbinned_);
        }

        private void CustomRegion_Checked(object sender, RoutedEventArgs e)
        {
            RegionOfInterest roi = new RegionOfInterest(x_, y_, w_, h_, xb_, yb_);
            RegionOfInterest[] regions = { roi };
            if (CameraExist)
                experiment_.SetCustomRegions(regions);
        }

        private void FullSensorBinW_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (FullSensorBinW.Text != string.Empty)
            {
                xbin_ = Convert.ToInt32(FullSensorBinW.Text);
                if (CameraExist)
                    experiment_.SetBinnedSensorRegion(xbin_, ybin_);
            }
        }

        private void FullSensorBinH_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (FullSensorBinH.Text != string.Empty)
            {
                ybin_ = Convert.ToInt32(FullSensorBinH.Text);
                if (CameraExist)
                    experiment_.SetBinnedSensorRegion(xbin_, ybin_);
            }
        }

        private void RowsBinnedH_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (RowsBinnedH.Text != string.Empty)
            {
                rowsbinned_ = Convert.ToInt32(RowsBinnedH.Text);
                if (CameraExist)
                    experiment_.SetLineSensorRegion(rowsbinned_);
            }
        }

        private void RegionX_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (RegionX.Text != string.Empty)
            {
                x_ = Convert.ToInt32(RegionX.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
        }

        private void RegionY_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (RegionY.Text != string.Empty)
            {
                y_ = Convert.ToInt32(RegionY.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
        }

        private void RegionWidth_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (RegionWidth.Text != string.Empty)
            {
                w_ = Convert.ToInt32(RegionWidth.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
        }

        private void RegionHeight_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (RegionHeight.Text != string.Empty)
            {
                h_ = Convert.ToInt32(RegionHeight.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
        }

        private void XBin_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (XBin.Text != string.Empty)
            {
                xb_ = Convert.ToInt32(XBin.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
        }

        private void YBin_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (YBin.Text != string.Empty)
            {
                yb_ = Convert.ToInt32(YBin.Text);
                CustomRegion_Checked(this, new RoutedEventArgs());
            }
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
        private void button1_Click(object sender, RoutedEventArgs e)
        {
            // Can we acquire?
            if (!ValidateAcquisition())
                return;

            // Snap an image
            if (CameraExist)
                experiment_.Acquire();
        }
       
    }
}
