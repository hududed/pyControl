Imports System
Imports System.Collections.Generic
Imports System.Linq
Imports System.Text
Imports System.Windows
Imports System.Windows.Controls
Imports System.Windows.Markup
Imports System.AddIn
Imports System.IO
Imports System.AddIn.Pipeline
Imports PrincetonInstruments.LightField.AddIns

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample sets an exposure time, disables date and time as part of the     ''''''''''
'''''''''' file name and sets a specific name.                                          ''''''''''  
'''''''''' Note pressing the button multiple times will continually overwrite the file. ''''''''''
'''''''''' This sample also overrides the file already exists dialog.                   ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class CustomAcquireSample
    Inherits AddInBase

    Private WithEvents control_ As Button

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentSetting
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app

        'Build your controls
        control_ = New Button()
        control_.Content = "Acquire"
        ExperimentSettingElement = control_
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return "Custom Acquire Sample"
        End Get
    End Property

    'Override some typical settings and acquire an spe file with a specific name
    Private Sub control_Click(sender As Object, e As System.Windows.RoutedEventArgs) Handles control_.Click
        'Are we in a state where we can do this?
        If Not ValidateAcquisition() Then
            Exit Sub
        End If
        'Get the experiment object
        Dim experiment As IExperiment = LightFieldApplication.Experiment
        If experiment IsNot Nothing Then
            'Not all systems have an exposure setting, if they do get the minimum and set it.
            If experiment.Exists(CameraSettings.ShutterTimingExposureTime) Then
                Dim currentRange As ISettingRange = experiment.GetCurrentRange(CameraSettings.ShutterTimingExposureTime)
                experiment.SetValue(CameraSettings.ShutterTimingExposureTime, currentRange.Minimum)
            End If
            'Don't attach date/time
            experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, False)
            experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, False)
            'Save file as Specific.Spe to the default directory
            experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, "Specific")
            'Connnect the event handler
            AddHandler experiment.ExperimentCompleted, AddressOf exp_AcquisitionComplete

            'Begin the acquisition 
            experiment.Acquire()
        End If
    End Sub

    Private Function ValidateAcquisition() As Boolean
        Dim camera As IDevice = Nothing
        For Each device As IDevice In LightFieldApplication.Experiment.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                camera = device
            End If
        Next
        If camera Is Nothing Then
            MsgBox("This sample requires a camera!")
            Return False
        End If
        If Not LightFieldApplication.Experiment.IsReadyToRun Then
            MsgBox("The system is not ready for acquisition, is there an error?")
            Return False
        End If
        Return True
    End Function

    'Acquire Completed Handler. This just fires a message saying that the data is acquired.
    Private Sub exp_AcquisitionComplete(sender As Object, e As ExperimentCompletedEventArgs)
        Dim exp As IExperiment = sender
        RemoveHandler exp.ExperimentCompleted, AddressOf exp_AcquisitionComplete
        MsgBox("Acquire Completed")
    End Sub

End Class
