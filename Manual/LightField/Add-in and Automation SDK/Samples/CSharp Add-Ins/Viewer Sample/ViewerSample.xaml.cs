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
using System.IO;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    /// <summary>
    /// Interaction logic for ViewerSample.xaml
    /// </summary>
    public partial class ViewerSample : UserControl
    {
        ILightFieldApplication application_;
        IDisplayViewerControl viewer_;

        public ViewerSample(ILightFieldApplication app)
        {
            application_ = app;
            InitializeComponent();

            // Create a LightField Style Display Viewer
            viewer_ =  application_.DisplayManager.CreateDisplayViewerControl();
            ViewerControl.Children.Add(viewer_.Control);

            // Setup some of the properties for the viewer control
            viewer_.IsDisplayTypeSelectable = true;
            viewer_.IsLiveDataAvailable     = true;
            viewer_.SourceAvailability      = ImageDataSourceAvailability.Selectable;        

            // Clear old and add live display
            viewer_.DisplayViewer.Clear();
            viewer_.DisplayViewer.Add(viewer_.DisplayViewer.LiveDisplaySource);
        }

        private void OpenFile_Click(object sender, RoutedEventArgs e)
        {            
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            dlg.FileName = "Document";                  // Default file name
            dlg.DefaultExt = ".spe";                    // Default file extension
            dlg.Filter = "SPE documents (.spe)|*.spe";  // Filter files by extension

            // Show open file dialog box
            Nullable<bool> result = dlg.ShowDialog();

            // Process open file dialog box results
            if (result == true)
            {                
                ShowFrame(dlg.FileName);
            }            
        }

        void ShowFrame(string fileName)
        {
            var filemgr = application_.FileManager;
            if (filemgr != null)
            {                
                IImageDataSet dataSet = filemgr.OpenFile(fileName, FileAccess.Read);                
                IImageData d = dataSet.GetFrame(0, 0);

                // Convert IImageData To Bitmap
                System.Drawing.Bitmap bmp = new System.Drawing.Bitmap(d.Width, d.Height);
                ushort[] data = new ushort[bmp.Width * bmp.Height];

                // convert them all to the smallest (simple example for now)
                var pixels = bmp.Width * bmp.Height;
                switch (d.Format)
                {
                    case ImageDataFormat.MonochromeFloating32:
                        {
                            float[] ptr = (float[])d.GetData();
                            for (int k = 0; k < pixels; k++)
                                data[k] = (ushort)ptr[k];
                        }
                        break;
                    case ImageDataFormat.MonochromeUnsigned16:
                        {
                            ushort[] ptr = (ushort[])d.GetData();
                            for (int k = 0; k < pixels; k++)
                                data[k] = (ushort)ptr[k];
                        }
                        break;
                    case ImageDataFormat.MonochromeUnsigned32:
                        {
                            uint[] ptr = (uint[])d.GetData();
                            for (int k = 0; k < pixels; k++)
                                data[k] = (ushort)ptr[k];
                        }
                        break;
                }

                short rgb_value = 0;
                int i = 0;
                for (int y = 0; y < bmp.Height; y++)
                {
                    for (int x = 0; x < bmp.Width; x++)
                    {
                        rgb_value = (short)((ushort)data[i] / (ushort)256);
                        bmp.SetPixel(x, y, System.Drawing.Color.FromArgb(rgb_value, rgb_value, rgb_value));
                        i++;
                    }
                }
                // Convert To WPF Bitmap
                System.Windows.Media.Imaging.BitmapSource bitmapSource = System.Windows.Interop.Imaging.CreateBitmapSourceFromHBitmap(bmp.GetHbitmap(), IntPtr.Zero, Int32Rect.Empty,
                System.Windows.Media.Imaging.BitmapSizeOptions.FromEmptyOptions());

                // Set the source
                image1.Source = bitmapSource;

                // Show the image in a new display viewer
                viewer_.DisplayViewer.Display("Sample Display", dataSet);
            }
        }
       
    }
}
