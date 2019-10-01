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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample is intended to show how to acquire data (to the default name and location) ''''''''''
'''''''''' and demonstrate how to hook into the acquisition started                               ''''''''''
'''''''''' and acquisition completed events.                                                      ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class AddinAcquireAsyncSample
    Inherits AddInBase

    Public control_ As AsynAcquireSample

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentSetting
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture Interface
        LightFieldApplication = app
        'Build your controls
        control_ = New AsynAcquireSample(LightFieldApplication)
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

    Public Shadows ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return "Acquire Asynchronous Sample"
        End Get
    End Property

End Class
