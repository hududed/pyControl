Imports System
Imports System.Collections.Generic
Imports System.Linq
Imports System.Text
Imports System.Windows
Imports System.Windows.Controls
Imports System.Windows.Data
Imports System.Windows.Documents
Imports System.Windows.Input
Imports System.Windows.Media
Imports System.Windows.Media.Imaging
Imports System.Windows.Navigation
Imports System.Windows.Shapes
Imports PrincetonInstruments.LightField.AddIns

'Interaction logic for ExportSample.xaml
Public Class ExportSample
    Private application_ As ILightFieldApplication
    Private customPath_ As String = Nothing
    Private options_ As ExportOutputPathOption = ExportOutputPathOption.InputPath
    Private baseSettings_ As IExportSettings = Nothing

    Public Sub New(application As ILightFieldApplication)
        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        application_ = application 'Store the application for future reference
    End Sub

    Private Sub AddFile_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim dlg As Microsoft.Win32.OpenFileDialog = New Microsoft.Win32.OpenFileDialog()
        dlg.FileName = "Document"                  'Default file name
        dlg.DefaultExt = ".spe"                   'Default file extension
        dlg.Filter = "SPE documents (.spe)|*.spe" 'Filter files by extension
        Dim result As Nullable(Of Boolean) = dlg.ShowDialog() 'Show open file dialog box
        'Process open file dialog box result
        If result = True Then
            FilesListBox.Items.Add(dlg.FileName)
        End If
    End Sub

    Private Sub AddFolder_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Folder Selector
        Dim dialog As Object = New System.Windows.Forms.FolderBrowserDialog()
        dialog.Description = "Please choose folder containing SPE file(s)."
        Dim result As System.Windows.Forms.DialogResult = dialog.ShowDialog()
        If result <> System.Windows.Forms.DialogResult.OK Then 'Do not want to export the files
            Exit Sub
        End If
        'Add this path
        FilesListBox.Items.Add(dialog.SelectedPath)
    End Sub

    Private Sub RemoveFile_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If FilesListBox.SelectedIndex <> -1 Then
            FilesListBox.Items.RemoveAt(FilesListBox.SelectedIndex)
        End If
    End Sub

    'When the file out type is changed, only show the supported modes for that output file type.
    Private Sub OutputFormat_SelectionChanged(sender As System.Object, e As System.Windows.Controls.SelectionChangedEventArgs)
        If Not IsLoaded Then
            Exit Sub
        End If
        'Clear old items 
        ModeCombo.Items.Clear()
        'Change to supported modes
        Select Case OutputFormat.SelectedIndex
            Case 1 'Comma seperated values
                ModeCombo.Items.Add(ExportOutputMode.OneFile)
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerFrame)
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi)
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoiPerFrame)
                ModeCombo.SelectedIndex = 0
            Case 4 'AVI file format
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi)
                ModeCombo.SelectedIndex = 0
            Case Else '0 Or 2 Or 3 'Common cases
                '0 is Tagged image file format; 2 is Galactic SPC spectroscopy file type; 3 is Grams Fits file format.
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoi)
                ModeCombo.Items.Add(ExportOutputMode.OneFilePerRoiPerFrame)
                ModeCombo.SelectedIndex = 0
        End Select
    End Sub
    
    Private Sub SourceLocationRadio_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        options_ = ExportOutputPathOption.InputPath
    End Sub

    Private Sub OtherDirectoryRadio_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        options_ = ExportOutputPathOption.CustomPath
    End Sub

    Private Sub OutputPathButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Folder selector
        Dim dialog As Object = New System.Windows.Forms.FolderBrowserDialog()
        dialog.Description = "Please choose folder containing SPE file(s)."
        Dim result As System.Windows.Forms.DialogResult = dialog.ShowDialog()
        If result <> System.Windows.Forms.DialogResult.OK Then 'Do not want to export the files
            Exit Sub
        End If
       'Add this path
        customPath_ = dialog.SelectedPath
        CustomPathLabel.Content = customPath_
    End Sub

    Private Sub ExportButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Get the file manager
        Dim fm As IFileManager = application_.FileManager
        'Block user pop ups
        application_.UserInteractionManager.SuppressUserInteraction = True

        Try
            'Clear out prior errors
            ErrorTextBox.Clear()
            'Add files
            Dim itemsForExport As List(Of String) = New List(Of String)()
            itemsForExport.AddRange(FilesListBox.Items.Cast(Of String)())
            Dim selectedErrors As IList(Of IExportSelectionError) = New List(Of IExportSelectionError)()
            'Settings
            Select Case OutputFormat.SelectedIndex
                Case 0 'Tagged image file format
                    Dim tifSettings As ITiffExportSettings = fm.CreateExportSettings(ExportFileType.Tiff)
                    tifSettings.IncludeAllExperimentInformation = True 'Specifics
                    baseSettings_ = tifSettings
                Case 1 'Comma seperated values
                    Dim csvSettings As ICsvExportSettings = fm.CreateExportSettings(ExportFileType.Csv)
                    Dim list As List(Of CsvTableFormat) = New List(Of CsvTableFormat)()
                    list.Add(CsvTableFormat.Frame)
                    list.Add(CsvTableFormat.Region)
                    list.Add(CsvTableFormat.Wavelength)
                    list.Add(CsvTableFormat.Column)
                    list.Add(CsvTableFormat.Intensity)
                    list.Add(CsvTableFormat.Row)
                    'Specifics
                    csvSettings.TableFormat = list
                    csvSettings.HeaderType = CsvExportHeader.Long
                    csvSettings.IncludeFormatMarkers = True
                    csvSettings.Layout = CsvLayout.Matrix

                    'Set culture to regional with the default separator
                    csvSettings.FieldSeparator = CsvFieldSeparator.Auto
                    csvSettings.NumberFormat = CsvNumberFormat.Regional

                    baseSettings_ = csvSettings
                Case 2 'Galactic SPC spectroscopy file type
                    Dim spcSettings As ISpcExportSettings = fm.CreateExportSettings(ExportFileType.Spc)
                    'Specifics
                    spcSettings.GlobalTimeUnit = TimeUnit.Milliseconds
                    baseSettings_ = spcSettings
                Case 3 'Grams fits file format
                    Dim fitsSettings As IFitsExportSettings = fm.CreateExportSettings(ExportFileType.Fits)
                    'Specifics
                    fitsSettings.IncludeAllExperimentInformation = True
                    baseSettings_ = fitsSettings
                Case 4 'AVI file format
                    Dim aviSettings As IAviExportSettings = fm.CreateExportSettings(ExportFileType.Avi)
                    'Specifics
                    aviSettings.FrameRate = 30.0
                    aviSettings.Compressed = False
                    aviSettings.AlwaysAutoScale = True
                    baseSettings_ = aviSettings
            End Select
            'Common settings for all types
            baseSettings_.CustomOutputPath = customPath_
            baseSettings_.OutputPathOption = options_
            baseSettings_.OutputMode = [Enum].Parse(GetType(ExportOutputMode), ModeCombo.Text)
            selectedErrors = baseSettings_.Validate(itemsForExport)
            'Show any errors
            UpdateSelectedErrorTextBox(selectedErrors)
            'Export
            If AsyncCheckBox.IsChecked Then 'Async Mode
                AddHandler fm.ExportCompleted, AddressOf fm_ExportCompleted
                application_.UserInteractionManager.ApplicationBusyStatus = ApplicationBusyStatus.Busy
                fm.ExportAsync(baseSettings_, itemsForExport)
                CancelButton.IsEnabled = True 'Enable cancel
                ExportButton.IsEnabled = False
            Else 'Sync Mode
                ExportButton.IsEnabled = False
                'Busy cursor during write
                Using New AddInStatusHelper(application_, ApplicationBusyStatus.Busy)
                    fm.Export(baseSettings_, itemsForExport)
                End Using
                ExportButton.IsEnabled = True
            End If
        Catch ex As Exception
        Finally
            application_.UserInteractionManager.SuppressUserInteraction = False
        End Try
    End Sub

    'Cancel exporting (async only)
    Private Sub CancelButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim fm As IFileManager = application_.FileManager
        fm.CancelExportAsync()
    End Sub

    Private Sub fm_ExportCompleted(sender As Object, e As ExportCompletedEventArgs)
        application_.UserInteractionManager.ApplicationBusyStatus = ApplicationBusyStatus.NotBusy
        RemoveHandler CType(sender, IFileManager).ExportCompleted, AddressOf fm_ExportCompleted
        CancelButton.IsEnabled = False
        ExportButton.IsEnabled = True
    End Sub
       
    Private Function FolderOrFile(path As String) As String
        Dim isDirectory As Boolean = (System.IO.Directory.Exists(path)) And (Not System.IO.File.Exists(path))
        If isDirectory Then
            Return "Folder"
        Else
            Return "File"
        End If
    End Function
        
    Private Sub UpdateSelectedErrorTextBox(selectedErrors As IList(Of IExportSelectionError))
        If selectedErrors.Count = 0 Then
            Exit Sub
        End If
        'Iterate through each file 
        For Each err As IExportSelectionError In selectedErrors
            Dim sourceType As String = FolderOrFile(err.InputPath) + ": "
            'Spin through our error list and update the ui per file or folder
            For Each e As ExportItemSelectionError In err.Errors
                ErrorTextBox.AppendText(sourceType + e.ToString() + " " + err.InputPath + "\n")
            Next e
        Next err
    End Sub
End Class