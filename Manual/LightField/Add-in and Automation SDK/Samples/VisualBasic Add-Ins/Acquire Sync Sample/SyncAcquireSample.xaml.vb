Imports PrincetonInstruments.LightField.AddIns
Imports System.Windows

'Interaction logic for SyncAcquireSample.xaml
Public Class SyncAcquireSample

    Public application_ As ILightFieldApplication

    Public Sub New(ByVal app As ILightFieldApplication)
        InitializeComponent()
        application_ = app
    End Sub

    Private Function ValidateAcquisition() As Boolean
        Dim camera As IDevice = Nothing
        For Each device As IDevice In application_.Experiment.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                camera = device
            End If
        Next
        If camera Is Nothing Then
            MsgBox("This sample requires a camera!")
            Return False
        End If
        If Not application_.Experiment.IsReadyToRun Then
            MsgBox("The system is not ready for acquisition, is there an error?")
            Return False
        End If
        Return True
    End Function

    'Synchronous full frame acquire  
    Private Sub AcquireSync_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Are we in a state we can do this?
        If Not ValidateAcquisition() Then
            Exit Sub
        End If
        'Get the experiment object
        Dim experiment As IExperiment = application_.Experiment
        'Full Frame
        experiment.SetFullSensorRegion()

        Dim acquisitions As Integer = 3
        Dim frames As Integer = 1

        experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, frames)

        For i As Integer = 1 To acquisitions

            'Capture 1 Frame
            Dim set_ As IImageDataSet = experiment.Capture(1)

            ' Stop processing if we do not have all frames
            If (set_.Frames <> frames) Then

                ' Clean up the image data set                    
                set_.Dispose()

                Throw New ArgumentException("Frames are not equal")
            End If

            'Get the data from the current frame
            Dim imageData As Array = set_.GetFrame(0, frames - 1).GetData()

            '    Cache the frame
            Dim imageFrame As IImageData = set_.GetFrame(0, frames - 1)

            PrintData(imageData, imageFrame, i, acquisitions)
        Next
    End Sub

    Private Sub PrintData(ByVal imageData As Array, ByVal imageFrame As IImageData,
                      ByVal iteration As Integer, ByVal acquisitions As Integer)

        '   Calculate center
        Dim centerPixel = ((imageFrame.Height / 2 - 1) * imageFrame.Width) + imageFrame.Width / 2

        '   Last Pixel
        Dim lastPixel = (imageFrame.Width * imageFrame.Height) - 1

        '   First Pixel
        Dim pixel1 = String.Format(vbCrLf + "First Pixel Intensity: {0}",
                                   imageData.GetValue(0))

        '   Center Pixel, zero based
        Dim pixel2 =
            String.Format(vbCrLf + "Center Pixel Intensity: {0}",
                          imageData.GetValue(CInt(centerPixel)))

        '   Last Pixel
        Dim pixel3 =
            String.Format(vbCrLf + "Last Pixel Intensity: {0}",
                          imageData.GetValue(lastPixel))

        '   Create message
        Dim message As String =
            String.Format("Acquire {0} of {1} Completed {2} {3} {4}",
                          iteration, acquisitions, pixel1, pixel2, pixel3)

        MsgBox(message)

    End Sub

End Class