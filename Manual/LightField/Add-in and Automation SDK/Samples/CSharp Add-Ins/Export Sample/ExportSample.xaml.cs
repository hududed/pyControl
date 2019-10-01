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
using System.Diagnostics;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    /// <summary>
    /// Interaction logic for ExportSample.xaml
    /// </summary>
    public partial class ExportSample : Window
    {
        ILightFieldApplication application_;

        string customPath_        = string.Empty;
        ExportOutputPathOption options_ = ExportOutputPathOption.InputPath;
        IExportSettings baseSettings_ = null;

        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        public ExportSample(ILightFieldApplication application)
        {
            // Store the application for future reference
            application_ = application;

            // Initialize the window
            InitializeComponent();            
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void AddFile_Click(object sender, RoutedEventArgs e)
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            dlg.FileName = "Document";                  // Default file name
            dlg.DefaultExt = ".spe";                    // Default file extension
            dlg.Filter = "SPE documents (.spe)|*.spe";  // Filter files by extension

            // Show open file dialog box
            Nullable<bool> result = dlg.ShowDialog();

            // Process open file dialog box results
            if (result == true)
                FilesListBox.Items.Add(dlg.FileName);
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void RemoveFile_Click(object sender, RoutedEventArgs e)
        {
            if (FilesListBox.SelectedIndex != -1)
                FilesListBox.Items.RemoveAt(FilesListBox.SelectedIndex);
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void AddFolder_Click(object sender, RoutedEventArgs e)
        {
            // Folder Selector
            var dialog = new System.Windows.Forms.FolderBrowserDialog();
            dialog.Description = "Please choose folder containing SPE file(s).";
            System.Windows.Forms.DialogResult result = dialog.ShowDialog();

            // Something bad happened or we cancelled so we don't want to export the files.
            if (result != System.Windows.Forms.DialogResult.OK)
                return;
            
            // Add this path
            FilesListBox.Items.Add(dialog.SelectedPath);
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void RemoveFolder_Click(object sender, RoutedEventArgs e)
        {
            if (FilesListBox.SelectedIndex != -1)
                FilesListBox.Items.RemoveAt(FilesListBox.SelectedIndex);
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void ExportButton_Click(object sender, RoutedEventArgs e)
        {
            // Get the file manager
            IFileManager fm = application_.FileManager;

            // Block User Pop Ups
            application_.UserInteractionManager.SuppressUserInteraction = true;

            try
            {
                // clear out prior errors
                ErrorTextBox.Clear();

                // Add Files
                List<string> itemsForExport = new List<string>();
                itemsForExport.AddRange(FilesListBox.Items.Cast<string>());
             
                IList<IExportSelectionError> selectedErrors
                    = new List<IExportSelectionError>();                                

                switch (OutputFormat.SelectedIndex)
                {
                    /////////////////////////////////////////////
                    // Tagged image file format
                    /////////////////////////////////////////////
                    case 0:
                        ITiffExportSettings tifSettings = (ITiffExportSettings)fm.CreateExportSettings(ExportFileType.Tiff);

                        // Specifics
                        tifSettings.IncludeAllExperimentInformation = true;

                        baseSettings_ = tifSettings;
                        break;
                    /////////////////////////////////////////////
                    // Comma Seperated Values
                    /////////////////////////////////////////////
                    case 1:
                        ICsvExportSettings csvSettings = (ICsvExportSettings)fm.CreateExportSettings(ExportFileType.Csv);

                        List<CsvTableFormat> list = new List<CsvTableFormat>();
                        list.Add(CsvTableFormat.Frame);
                        list.Add(CsvTableFormat.Region);
                        list.Add(CsvTableFormat.Wavelength);
                        list.Add(CsvTableFormat.Column);
                        list.Add(CsvTableFormat.Intensity);
                        list.Add(CsvTableFormat.Row);

                        // Specifics
                        csvSettings.TableFormat          = list;
                        csvSettings.HeaderType           = CsvExportHeader.Long;
                        csvSettings.IncludeFormatMarkers = true;
                        csvSettings.Layout               = CsvLayout.Matrix;

                        // Set culture to regional with the default separator
                        csvSettings.FieldSeparator = CsvFieldSeparator.Auto;
                        csvSettings.NumberFormat = CsvNumberFormat.Regional;
                                                
                        baseSettings_ = csvSettings;
                        break;
                    /////////////////////////////////////////////
                    // Galactic SPC spectroscopy file type
                    /////////////////////////////////////////////
                    case 2:
                        ISpcExportSettings spcSettings = (ISpcExportSettings)fm.CreateExportSettings(ExportFileType.Spc);                        

                        // Specifics
                        spcSettings.GlobalTimeUnit = TimeUnit.Milliseconds;

                        baseSettings_ = spcSettings;
                        break;
                    /////////////////////////////////////////////
                    // Grams Fits file format
                    /////////////////////////////////////////////
                    case 3:
                        IFitsExportSettings fitsSettings = (IFitsExportSettings)fm.CreateExportSettings(ExportFileType.Fits);
                        
                        // Specifics
                        fitsSettings.IncludeAllExperimentInformation = true;

                        baseSettings_ = fitsSettings;
                        break;
                    /////////////////////////////////////////////
                    // AVI file format
                    /////////////////////////////////////////////
                    case 4:
                        IAviExportSettings aviSettings = (IAviExportSettings)fm.CreateExportSettings(ExportFileType.Avi);
                        
                        // Specifics
                        aviSettings.FrameRate  = 30.0;
                        aviSettings.Compressed = false;
                        aviSettings.AlwaysAutoScale = true;

                        baseSettings_ = aviSettings;
                        break;
                }
                // Common Settings for all types
                baseSettings_.CustomOutputPath  = customPath_;
                baseSettings_.OutputPathOption  = options_;
                baseSettings_.OutputMode        = (ExportOutputMode)Enum.Parse(typeof(ExportOutputMode), ModeCombo.Text);

                selectedErrors = baseSettings_.Validate(itemsForExport);

                // Show any errors
                UpdateSelectedErrorTextBox(selectedErrors);

                // Async Mode
                if (AsyncCheckBox.IsChecked == true)
                {
                    fm.ExportCompleted += new EventHandler<ExportCompletedEventArgs>(fm_ExportCompleted);

                    application_.UserInteractionManager.ApplicationBusyStatus = ApplicationBusyStatus.Busy;
                    fm.ExportAsync(baseSettings_, itemsForExport);

                    // Enable cancel
                    CancelButton.IsEnabled = true;
                    ExportButton.IsEnabled = false;
                }
                // Sync Mode
                else
                {
                    ExportButton.IsEnabled = false;

                    // Busy cursor during write
                    using (new AddInStatusHelper(application_, ApplicationBusyStatus.Busy))
                    {
                        fm.Export(baseSettings_, itemsForExport);
                    }
                    ExportButton.IsEnabled = true;
                }
            }
            finally
            {
                application_.UserInteractionManager.SuppressUserInteraction = false;
            }
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        void fm_ExportCompleted(object sender, ExportCompletedEventArgs e)
        {
            application_.UserInteractionManager.ApplicationBusyStatus = ApplicationBusyStatus.NotBusy;
            ((IFileManager)sender).ExportCompleted -= fm_ExportCompleted;
            CancelButton.IsEnabled = false;
            ExportButton.IsEnabled = true;
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        string FolderOrFile(string path)
        {
            bool isDirectory = System.IO.Directory.Exists(path) && !System.IO.File.Exists(path);
            if (isDirectory)
                return "Folder";
            else
                return "File";
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void UpdateSelectedErrorTextBox(IList<IExportSelectionError> selectedErrors)
        {
            if (selectedErrors.Count() == 0)
                return;
            // iterate through each file 
            foreach (IExportSelectionError error in selectedErrors)
            {
                string sourceType = FolderOrFile(error.InputPath) + ": ";
                
                // spin through our error list and update the ui per file or folder
                foreach ( ExportItemSelectionError e in error.Errors)
                {
                    ErrorTextBox.AppendText(sourceType + e.ToString() + " " + error.InputPath + "\n");
                }
            }
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void OutputPathButton_Click(object sender, RoutedEventArgs e)
        {
            // Folder Selector
            var dialog = new System.Windows.Forms.FolderBrowserDialog();
            dialog.Description = "Please choose folder containing SPE file(s).";
            System.Windows.Forms.DialogResult result = dialog.ShowDialog();

            // Something bad happened or we cancelled so we don't want to export the files.
            if (result != System.Windows.Forms.DialogResult.OK)
                return;

            // Add this path
            customPath_             = dialog.SelectedPath;
            CustomPathLabel.Content = customPath_;
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void SourceLocationRadio_Checked(object sender, RoutedEventArgs e)
        {
            options_ = ExportOutputPathOption.InputPath;
        }
        ///////////////////////////////////////////////////////////////////////////
        //
        ///////////////////////////////////////////////////////////////////////////
        private void OtherDirectoryRadio_Checked(object sender, RoutedEventArgs e)
        {
            options_ = ExportOutputPathOption.CustomPath;
        }
        ///////////////////////////////////////////////////////////////////////////
        //  When the file out type is changed only show the supported modes for that
        // output file type.
        ///////////////////////////////////////////////////////////////////////////
        private void OutputFormat_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (!IsLoaded)
                return;

            // Clear Old Items When Format Changes
            ModeCombo.Items.Clear();

            switch (OutputFormat.SelectedIndex)
            {
                /////////////////////////////////////////////
                // Common Cases
                /////////////////////////////////////////////                
                case 0:// Tagged image file format 
                case 2:// Galactic SPC spectroscopy file type 
                case 3:// Grams Fits file format 
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi);
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoiPerFrame);
                    ModeCombo.SelectedIndex = 0;
                    break;
                /////////////////////////////////////////////
                // Comma Seperated Values
                /////////////////////////////////////////////
                case 1:
                    ModeCombo.Items.Add(ExportOutputMode.OneFile);
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerFrame);
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi);
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoiPerFrame);
                    ModeCombo.SelectedIndex = 0;
                    break;                
                /////////////////////////////////////////////
                // AVI file format
                /////////////////////////////////////////////
                case 4:        
                    ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi);                    
                    ModeCombo.SelectedIndex = 0;
                    break;
            }
        }
        ///////////////////////////////////////////////////////////////////////////
        // Cancelling (Async Only)
        ///////////////////////////////////////////////////////////////////////////
        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            IFileManager fm = application_.FileManager;            
            fm.CancelExportAsync();
        }                        
    }
}
