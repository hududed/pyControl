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
Imports System.IO
Imports PrincetonInstruments.LightField.AddIns

'Interaction logic for ViewerSample.xaml
Public Class ViewerSample
    Private application_ As ILightFieldApplication
    Private viewer_ As IDisplayViewerControl

    Public Sub New(app As ILightFieldApplication)
        application_ = app
        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        'Create a LightField style display viewer
        viewer_ = application_.DisplayManager.CreateDisplayViewerControl()
        ViewerControl.Children.Add(viewer_.Control)
        'Setup some of the properties for the viewer control
        viewer_.IsDisplayTypeSelectable = True
        viewer_.IsLiveDataAvailable = True
        viewer_.SourceAvailability = ImageDataSourceAvailability.Selectable
        'Clear old and add live display
        viewer_.DisplayViewer.Clear()
        viewer_.DisplayViewer.Add(viewer_.DisplayViewer.LiveDisplaySource)
    End Sub

    Private Sub OpenFile_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim dlg As Microsoft.Win32.OpenFileDialog = New Microsoft.Win32.OpenFileDialog()
        dlg.FileName = "Document" 'Default file name
        dlg.DefaultExt = ".spe" 'Default file extension
        dlg.Filter = "SPE documents (.spe)|*.spe" 'Filter files by extension
        'Show open file dialog box
        Dim result As Boolean? = dlg.ShowDialog()
        'Process open file dialog box results
        If result = True Then
            ShowFrame(dlg.FileName)
        End If  
    End Sub

    Private Sub ShowFrame(fileName As String)
        Dim filemgr As IFileManager = application_.FileManager
        If filemgr IsNot Nothing Then
            Dim dataSet As IImageDataSet = filemgr.OpenFile(fileName, FileAccess.Read)
            Dim d As IImageData = dataSet.GetFrame(0, 0)
            'Convert IImageData to Bitmap
            Dim bmp As System.Drawing.Bitmap = New System.Drawing.Bitmap(d.Width, d.Height)
            Dim data(bmp.Width * bmp.Height) As UShort
            'convert them all to the smallest (simple example for now)
            Dim pixels As Integer = bmp.Width * bmp.Height
            Select Case d.Format
                Case ImageDataFormat.MonochromeFloating32
                    Dim ptr As Single() = d.GetData()
                    For k As Integer = 0 To pixels - 1
                        data(k) = ptr(k)
                    Next
                Case ImageDataFormat.MonochromeUnsigned16
                    Dim ptr As UShort() = d.GetData()
                    For k As Integer = 0 To pixels - 1
                        data(k) = ptr(k)
                    Next
                Case ImageDataFormat.MonochromeUnsigned32
                    Dim ptr As UInteger() = d.GetData()
                    For k As Integer = 0 To pixels - 1
                        data(k) = ptr(k)
                    Next
            End Select
            Dim rgb_value As Short = 0
            Dim i As Integer = 0
            For y As Integer = 0 To bmp.Height - 1
                For x As Integer = 0 To bmp.Width - 1
                    rgb_value = data(i) / 256.0
                    bmp.SetPixel(x, y, System.Drawing.Color.FromArgb(rgb_value, rgb_value, rgb_value))
                    i += 1
                Next
            Next
            'Convert to WPF Bitmap
            Dim bitmapSource As System.Windows.Media.Imaging.BitmapSource = System.Windows.Interop.Imaging.CreateBitmapSourceFromHBitmap(bmp.GetHbitmap(), IntPtr.Zero, Int32Rect.Empty, System.Windows.Media.Imaging.BitmapSizeOptions.FromEmptyOptions())
            'Set the source
            image1.Source = bitmapSource
            'Show the image in a new display viewer
            viewer_.DisplayViewer.Display("Sample Display", dataSet)
        End If
    End Sub
End Class