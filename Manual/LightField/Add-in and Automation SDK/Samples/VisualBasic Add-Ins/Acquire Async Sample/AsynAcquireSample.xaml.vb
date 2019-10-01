Imports PrincetonInstruments.LightField.AddIns
Imports System.Windows.Threading
Imports System.IO


'Interaction logic for AsynAcquireSample.xaml
Partial Public Class AsynAcquireSample
    'Inherits System.Windows.Controls.UserControl

    Public application_ As ILightFieldApplication
    Public experiment_ As IExperiment
    Public totalAcquisitions_, acquisitionsCompleted_, frames_ As Integer
    Public fileManager_ As IFileManager


    'Constructor: Pull the experiment out of the app and store it for use
    Public Sub New(ByVal app As ILightFieldApplication)
        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        application_ = app
        experiment_ = application_.Experiment
        fileManager_ = application_.FileManager
    End Sub

    Private Function ValidateAcquisition() As Boolean
        Dim camera As IDevice = Nothing
        For Each device As IDevice In experiment_.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                camera = device
            End If
        Next
        If camera Is Nothing Then
            MsgBox("This sample requires a camera!")
            Return False
        End If
        If Not experiment_.IsReadyToRun Then
            MsgBox("The system is not ready for acquisition, is there an error?")
            Return False
        End If
        Return True
    End Function

    '   Acquire Full Chip Asynchronously
    Private Sub AcquireAsync_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        '   Can we do this?
        If (Not ValidateAcquisition()) Then
            Return
        End If

        '   n case a previous run was not completed make sure we start out not listening
        RemoveHandler experiment_.ExperimentStarted, AddressOf exp_AcquisitionStarted
        RemoveHandler experiment_.ExperimentCompleted, AddressOf exp_AcquisitionComplete

        acquisitionsCompleted_ = 0
        totalAcquisitions_ = 3
        frames_ = 1

        '   We want unique file names for this
        experiment_.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, True)

        '   Set number of frames
        experiment_.SetValue(ExperimentSettings.AcquisitionFramesToStore, frames_)

        '   Connect Completion Event
        AddHandler experiment_.ExperimentStarted, AddressOf exp_AcquisitionStarted

        ' Begin the acquisition (Note: current exposure, frames, filename etc will be used)
        experiment_.Acquire()
    End Sub

    'Acquire Completed Handler. This just fires a message saying that the data is acquired.
    Private Sub exp_AcquisitionComplete(ByVal sender As Object, ByVal e As ExperimentCompletedEventArgs)

        '   We can not call acquire in the completed handler, it must be deferred because 
        '   the current acquisition will not be considered complete until this handler has
        '   returned. 
        Dispatcher.BeginInvoke(DispatcherPriority.Background,
                               CType((Sub()
                                          acquisitionsCompleted_ += 1

                                          '  Safe to get data once acquisition is complete
                                          ShowImageDataFromLastAcquire()

                                          ' Disconnect from the completed as the start event will reconnect
                                          RemoveHandler experiment_.ExperimentCompleted, AddressOf exp_AcquisitionComplete

                                          '   Start the next one
                                          If (acquisitionsCompleted_ < totalAcquisitions_) Then
                                              experiment_.Acquire()

                                              '   Or no starts and disconnect starting as the next button click
                                              '   will reconnect started.
                                          Else
                                              RemoveHandler experiment_.ExperimentStarted, AddressOf exp_AcquisitionStarted
                                          End If

                                      End Sub), Action))
    End Sub

    ' Acquire Started Handler. This just fires a message saying that the data is acquired.
    Private Sub exp_AcquisitionStarted(ByVal sender As Object, ByVal e As ExperimentStartedEventArgs)
        AddHandler experiment_.ExperimentCompleted, AddressOf exp_AcquisitionComplete
    End Sub

    Private Sub ShowImageDataFromLastAcquire()
        '   Expected resulting file name
        Dim resultName As String =
            experiment_.GetValue(ExperimentSettings.AcquisitionOutputFilesResult)

        '   Open the last acquired file
        Dim files As IList(Of String) = fileManager_.GetRecentlyAcquiredFileNames()

        '   Is our result in the acquired
        If (files.Contains(resultName)) Then

            '   Open file
            Dim dataSet As IImageDataSet = fileManager_.OpenFile(resultName, FileAccess.Read)

            ' Stop processing if we do not have all frames
            If (dataSet.Frames <> frames_) Then

                '   Close the file
                fileManager_.CloseFile(dataSet)

                Throw New ArgumentException("Frames are not equal")
            End If

            '   Cache image data
            Dim imageData As Array = dataSet.GetFrame(0, frames_ - 1).GetData()

            '    Cache the frame
            Dim imageFrame As IImageData = dataSet.GetFrame(0, frames_ - 1)

            '   Print some of the cached data
            PrintData(imageData, imageFrame)

            '   Close the file
            fileManager_.CloseFile(dataSet)
        End If

    End Sub

    Private Sub PrintData(ByVal imageData As Array, ByVal imageFrame As IImageData)

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
                          acquisitionsCompleted_, totalAcquisitions_, pixel1, pixel2, pixel3)

        MsgBox(message)

    End Sub

End Class