Imports System
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Windows
Imports PrincetonInstruments.LightField.AddIns
Imports PrincetonInstruments.LightField.Automation

'Interaction logic for MainWindow.xaml
Class MainWindow

    Private experiment_ As IExperiment
    Private automation_ As Automation
    Private application_ As ILightFieldApplication


    Public Sub New()
        ' This call is required by the designer.
        InitializeComponent()

        Cameras = New List(Of CameraSetup)
        OpenLightFields = New List(Of OpenLightField)()
        IncrementFileName = 0

        ' Open one invisible instance of LightField
        Dim openLightFieldObject = New OpenLightField(Me, visible_LightField:=False)

        ' return its automation object
        automation_ = openLightFieldObject.Auto

        ' return its experiment object
        experiment_ = openLightFieldObject.Experiment

        ' return its application object
        application_ = openLightFieldObject.Application

        AddHandler IsVisibleChanged,
                AddressOf MainWindow_IsVisibleChanged
    End Sub

    Private Sub MainWindow_IsVisibleChanged(sender As Object, e As DependencyPropertyChangedEventArgs)
        ' Update list box when the main window becomes visible
        If CBool(e.NewValue) = True Then
            UpdateListBox()
        End If

        RemoveHandler IsVisibleChanged,
            AddressOf MainWindow_IsVisibleChanged
    End Sub

    ''' <summary> 
    ''' Collection of all open LightFields
    ''' </summary>
    Private Property OpenLightFields() As List(Of OpenLightField)

    ''' <summary>
    ''' Collection of all cameras
    ''' </summary>
    ''' <value></value>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Property Cameras() As List(Of CameraSetup)

    ''' <summary>
    ''' Used for unique file naming
    ''' </summary>
    ''' <value></value>
    ''' <returns></returns>
    ''' <remarks></remarks>
    Property IncrementFileName() As String

    Private Sub StopButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        ' Get all running cameras
        Dim runningExperiments = Cameras.FindAll(Function(p) p.ExperimentObject.IsRunning)

        ' Stop acquisition for all running cameras
        For Each experiment In runningExperiments
            experiment.EndAquisition()
        Next

    End Sub

    Private Sub StartButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)

        ' Get all idle cameras
        Dim experimentNotRunning =
            Cameras.FindAll(Function(p) Not p.ExperimentObject.IsRunning)

        For Each experiment In experimentNotRunning
            ' Run worker asynchronously to start acquisition
            experiment.StartAcquisitionWorker.RunWorkerAsync()
        Next

    End Sub

    Private Sub LaunchButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        ' Disable button after first use
        LaunchButton.IsEnabled = False

        ' Add all available experiments
        AddAvailableCameras()
    End Sub

    Private Sub Close_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        ' Close application
        Close()

        ' Unhook event handlers from each object
        Cameras.ForEach(Sub(p) p.UnHookEvents())
        OpenLightFields.ForEach(Sub(p) p.UnHookEvents())
    End Sub

    Private Sub HideLFCheckbox_Checked(sender As Object, e As RoutedEventArgs)
        ' controls visibility of first LightField instance
        If (IsLoaded) Then
            automation_.IsApplicationVisible = False
        End If
    End Sub

    Private Sub HideLFCheckbox_OnUnchecked(sender As Object, e As RoutedEventArgs)
        ' controls visibility of first LightField instance
        If (IsLoaded) Then
            automation_.IsApplicationVisible = True
        End If
    End Sub

    Private Sub SuppressPromptCheckBox_Checked(sender As Object, e As RoutedEventArgs)
        ' control suppression of messages from the first LightField instance
        If (IsLoaded) Then
            application_.UserInteractionManager.SuppressUserInteraction = True
        End If
    End Sub

    Private Sub SuppressPromptCheckBox_OnUnchecked(sender As Object, e As RoutedEventArgs)
        ' control suppression of messages from the first LightField instance
        If (IsLoaded) Then
            application_.UserInteractionManager.SuppressUserInteraction = False
        End If
    End Sub

    ''' <summary>
    ''' Update list box with available cameras
    ''' </summary>
    Private Sub UpdateListBox()
        Dim cameraName As String = String.Empty

        ' Add available camera to the list box
        For Each camera As IDevice In experiment_.AvailableDevices
            If experiment_.AvailableDevices.Count > 0 AndAlso
                camera.Type = DeviceType.Camera Then
                cameraName =
                    String.Format("Model: {0}, SN: {1}",
                                  camera.Model, camera.SerialNumber)

                ' Add camera identity to user list if it is not present
                If Not AvaiableCamerasListBox.Items.Contains(cameraName) Then
                    AvaiableCamerasListBox.Items.Add(cameraName)
                End If
            End If
        Next
    End Sub

    ''' <summary>
    ''' Associate available cameras with automation and setup class
    ''' Connect camera to LightField
    ''' </summary>
    ''' <remarks></remarks>
    Private Sub AddAvailableCameras()

        ' Add available camera
        For Each camera As IDevice In experiment_.AvailableDevices
            If (experiment_.AvailableDevices.Count > 0 And
               camera.Type = DeviceType.Camera) Then

                experiment_ = New OpenLightField(Me, visible_LightField:=True).Experiment

                ' Connect camera to LightField
                experiment_.Add(camera)

                Dim cameraName As String =
                    String.Format("Model: {0}, SN: {1}",
                                  camera.Model, camera.SerialNumber)

                ' Assign background worker, identity, etc..
                ' through camera setup class
                Dim camera_setup As CameraSetup =
                    New CameraSetup(experiment_, Me, cameraName)

                experiment_ = camera_setup.ExperimentObject
            End If
        Next
    End Sub

    ''' <summary>
    ''' Encapsulation of individual LightField instances
    ''' </summary>
    ''' <remarks></remarks>
    Class OpenLightField
        Friend Property Auto() As Automation
        Friend Property Application() As ILightFieldApplication
        Friend Property Experiment() As IExperiment
        Friend Property VisibleLightField() As Boolean

        Private mainWindow_ As MainWindow

        Public Sub New(mainWindow As MainWindow, visible_LightField As Boolean)
            VisibleLightField = visible_LightField
            mainWindow_ = mainWindow

            OpenSingleInstance()

            ' Add this LightField to the List of open LightFields
            mainWindow_.OpenLightFields.Add(Me)
        End Sub

        ''' <summary>
        ''' Creates and opens a new instance of LightField
        ''' </summary>
        ''' <remarks></remarks>
        Private Sub OpenSingleInstance()
            Automation()

            AutoApplication()

            Experiment = Application.Experiment
        End Sub

        ''' <summary>
        ''' Create a new automation object
        ''' Hook closing event handler
        ''' Set LightField to visible or invisible
        ''' </summary>
        Private Sub Automation()
            ' Create a new automation object
            ' Set LightField to visible or invisible
            Auto = New Automation(VisibleLightField, 
                                  New List(Of String) From {New String("/empty")})

            ' Hook closing event handler
            AddHandler Auto.LightFieldClosing,
                AddressOf auto_LightFieldClosing
        End Sub

        ''' <summary>
        ''' Return ILightFieldApplication object
        ''' </summary>
        Private Sub AutoApplication()
            Application = Auto.LightFieldApplication
        End Sub

        Private Sub auto_LightFieldClosing(sender As Object, e As LightFieldClosingEventArgs)
            ' Prevent closing of any LightField instance
            e.Cancel = True
        End Sub

        ''' <summary>
        ''' Removes event/event handler association 
        ''' </summary>
        Friend Sub UnHookEvents()
            RemoveHandler Auto.LightFieldClosing,
                AddressOf auto_LightFieldClosing

            Auto.Dispose()
        End Sub

    End Class

    ''' <summary>
    ''' Encapsulation of individual experiment associations
    ''' </summary>
    ''' <remarks></remarks>
    Class CameraSetup

        Friend Property ExperimentObject() As IExperiment
        Friend Property ExperimentName() As String
        Friend Property StartAcquisitionWorker() As BackgroundWorker

        Private mainWindow_ As MainWindow

        ''' <summary>
        ''' Constructor
        ''' </summary>
        ''' <param name="experiment"></param>
        ''' <param name="mainWIndow"></param>
        ''' <remarks></remarks>
        Public Sub New(experiment As IExperiment, mainWIndow As MainWindow, name As String)
            ExperimentObject = experiment
            mainWindow_ = mainWIndow
            ExperimentName = Name

            CreateAcquisitionBGW()
            SaveFileOptions()

            '  Add camera setup to List
            mainWindow_.Cameras.Add(Me)
        End Sub

        ''' <summary>
        ''' Instantiate a new background worker for every experiment's start acquisition
        ''' </summary>
        ''' <remarks></remarks>
        Private Sub CreateAcquisitionBGW()
            StartAcquisitionWorker = New BackgroundWorker
            StartAcquisitionWorker.WorkerReportsProgress = False
            StartAcquisitionWorker.WorkerSupportsCancellation = False
            AddHandler StartAcquisitionWorker.DoWork,
                AddressOf StartAcquisitionWorker__DoWork
        End Sub

        Private Sub StartAcquisitionWorker__DoWork(ByVal sender As System.Object, ByVal e As DoWorkEventArgs)
            ' Acquire from passed in experiment/associated LightField
            If (ExperimentObject.IsReadyToRun And
                Not ExperimentObject.IsUpdating And
                Not ExperimentObject.IsRunning) Then

                ExperimentObject.Acquire()
            End If

        End Sub

        Sub EndAquisition()

            ' End acquisition of passed in experiment/associated LightField
            ExperimentObject.Stop()

        End Sub

        ''' <summary>
        ''' Set file options for each LightField instance
        ''' </summary>
        ''' <remarks></remarks>
        Private Sub SaveFileOptions()
            ' Option to Increment, set to false will not increment
            ExperimentObject.SetValue(
                ExperimentSettings.FileNameGenerationAttachIncrement,
                True)

            ' Increment on each file name
            mainWindow_.IncrementFileName += 1

            ExperimentObject.SetValue(
                ExperimentSettings.FileNameGenerationIncrementNumber,
                mainWindow_.IncrementFileName)

            ' Option to add date
            ExperimentObject.SetValue(
                ExperimentSettings.FileNameGenerationAttachDate,
                True)

            ' Option to add time
            ExperimentObject.SetValue(
                ExperimentSettings.FileNameGenerationAttachTime,
                True)
        End Sub

        ''' <summary>
        ''' Removes event/event handler association
        ''' </summary>
        ''' <remarks></remarks>
        Sub UnHookEvents()
            RemoveHandler StartAcquisitionWorker.DoWork,
                AddressOf StartAcquisitionWorker__DoWork
        End Sub

        Public Overrides Function ToString() As String
            Return ExperimentName
        End Function
    End Class
End Class