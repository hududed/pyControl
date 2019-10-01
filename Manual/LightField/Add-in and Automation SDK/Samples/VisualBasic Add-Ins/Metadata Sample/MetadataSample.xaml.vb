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
Imports System.Collections.ObjectModel
Imports PrincetonInstruments.LightField.AddIns

'Interaction logic for MetadataSample.xaml
Public Class MetadataSample
    Private app_ As ILightFieldApplication
    Private stampCollection_ As ObservableCollection(Of StampData) = New ObservableCollection(Of StampData)()
    Delegate Sub delegateAction(fileManager As IFileManager, files As IList(Of String))

    Public Class StampData
        Private exposureStart_ As TimeSpan?
        Private exposureEnd_ As TimeSpan?
        Private frame_ As Long?
        Private gateTrackingDelay_ As Double?
        Private gateTrackingWidth_ As Double?
        Private trackingPhase_ As Double?

        Public Property ExposureStart As Nullable(Of TimeSpan)
            Get
                Return exposureStart_
            End Get
            Set(value As Nullable(Of TimeSpan))
                exposureStart_ = value
            End Set
        End Property

        Public Property ExposureEnd As Nullable(Of TimeSpan)
            Get
                Return exposureEnd_
            End Get
            Set(value As Nullable(Of TimeSpan))
                exposureEnd_ = value
            End Set
        End Property

        Public Property Frame As Long?
            Get
                Return frame_
            End Get
            Set(value As Long?)
                frame_ = value
            End Set
        End Property

        Public Property GateTrackingDelay As Double?
            Get
                Return gateTrackingDelay_
            End Get
            Set(value As Double?)
                gateTrackingDelay_ = value
            End Set
        End Property

        Public Property GateTrackingWidth As Double?
            Get
                Return gateTrackingWidth_
            End Get
            Set(value As Double?)
                gateTrackingWidth_ = value
            End Set
        End Property

        Public Property TrackingPhase As Double?
            Get
                Return trackingPhase_
            End Get
            Set(value As Double?)
                trackingPhase_ = value
            End Set
        End Property
    End Class

    Public ReadOnly Property StampCollection As ObservableCollection(Of StampData)
        Get
            Return stampCollection_
        End Get
    End Property

    Public Sub New(application As ILightFieldApplication)
        app_ = application
        'This call is required by the designer.
        InitializeComponent()
        'Add any initialization after the InitializeComponent() call.
        textBoxFrames.Text = "5"
    End Sub

    'Acquire 5 frames with stamping on
    Private Sub button1_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Are we in a state where we can acquire?
        If Not ValidateAcquisition() Then
            Exit Sub
        End If
        'Get the experiment object
        Dim experiment As IExperiment = app_.Experiment
        If experiment IsNot Nothing Then
            'Empty the time stamping collection
            stampCollection_.Clear()
            'Turn on time stamping
            experiment.SetValue(CameraSettings.AcquisitionTimeStampingStamps, TimeStamps.ExposureEnded Or TimeStamps.ExposureStarted)
            'Turn On Frame Tracking
            experiment.SetValue(CameraSettings.AcquisitionFrameTrackingEnabled, True)
            'Don't attach date/time
            experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, False)
            experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, False)
            'Save file as Specific.Spe to the default directory
            experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, "MetaDataSample")
            'Set the number of frames
            experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, textBoxFrames.Text)
            'Connect completion event
            AddHandler experiment.ExperimentCompleted, AddressOf experiment_ExperimentCompleted
            'Capture 5 Frames
            experiment.Acquire()
        End If
    End Sub

    Private Function ValidateAcquisition() As Boolean
        Dim camera As IDevice = Nothing
        For Each device As IDevice In app_.Experiment.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                camera = device
            End If
        Next
        If camera Is Nothing Then
            MsgBox("This sample requires a camera!")
            Return False
        End If
        If Not app_.Experiment.IsReadyToRun Then
            MsgBox("The system is not ready for acquisition, is there an error?")
            Return False
        End If
        Return True
    End Function
        
    'Handler for acquire completed event        
    Private Sub experiment_ExperimentCompleted(sender As Object, e As ExperimentCompletedEventArgs)
        'Remove handler
        Dim sender_ As IExperiment = sender
        RemoveHandler sender_.ExperimentCompleted, AddressOf experiment_ExperimentCompleted
        'Show meta data
        Dim fileManager As IFileManager = app_.FileManager
        If fileManager IsNot Nothing Then
            'Get the recently acquired file list
            Dim files As IList(Of String) = fileManager.GetRecentlyAcquiredFileNames()
            'Open the last one if there is one
            If files.Count > 0 Then
                'We can't update our observable collection here. 
                'It must be done on this dispatcher not from within this callback.
                Dim action_ As delegateAction = AddressOf ShowInfo
                Dim para As Object() = {fileManager, files}
                Dispatcher.Invoke(action_, Windows.Threading.DispatcherPriority.Background, para)
            End If
        End If
    End Sub

    Private Sub ShowInfo(ByVal fileManager As IFileManager, ByVal files As IList(Of String))
        'Get the image dataset
        Dim dataSet As IImageDataSet = fileManager.OpenFile(files(0), System.IO.FileAccess.Read)
        'Show the origin
        origin.Text = dataSet.TimeStampOrigin.ToString()
        'Display the metadata for each frame
        For i As Integer = 0 To dataSet.Frames - 1
            Dim md As Metadata = dataSet.GetFrameMetaData(i)
            'Add the meta data to the observable collection that appears in the listview
            Dim data As New StampData
            data.ExposureStart = md.ExposureStarted
            data.ExposureEnd = md.ExposureEnded
            data.Frame = md.FrameTrackingNumber
            data.GateTrackingDelay = md.GateTrackingDelay
            data.GateTrackingWidth = md.GateTrackingWidth
            data.TrackingPhase = md.ModulationTrackingPhase
            stampCollection_.Add(data)
        Next
    End Sub
End Class