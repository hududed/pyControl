Imports System
Imports System.Collections.Generic
Imports System.Linq
Imports System.Text
Imports System.Windows
Imports System.Windows.Controls
Imports System.AddIn
Imports System.AddIn.Pipeline
Imports PrincetonInstruments.LightField.AddIns

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample acquires a single frame of data synchronously.                               ''''''''''
'''''''''' When the data is returned, pop it into a window (experiment view 1) for user to look at. ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
Public Class AcquireSyncSample
    Inherits AddInBase

    Private control_ As SyncAcquireSample

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentSetting
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Build your controls
        control_ = New SyncAcquireSample(app)
        ExperimentSettingElement = control_
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Shadows ReadOnly Property UIExperimentSetting As Windows.FrameworkElement
        Get
            If ExperimentSettingElement Is Nothing Then
                Throw New NotImplementedException("UIExperiment has no implementation!")
            Else
                Return ExperimentSettingElement
            End If
        End Get
    End Property

    Public Overrides ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return "Acquire Synchronous Sample"
        End Get
    End Property

End Class
