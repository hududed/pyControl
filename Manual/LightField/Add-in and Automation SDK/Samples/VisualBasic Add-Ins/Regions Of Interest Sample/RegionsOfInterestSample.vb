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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrate the modes of regions: full frame, binned, line sensor and custom.               ''''''''''
'''''''''' This sample is intended to be activated and used only when you have a camera in the system. ''''''''''
'''''''''' If no camera is in the system, this will simply fail to initialize and unload itself.       ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class RegionsOfInterestSample
    Inherits AddInBase

    Private control_ As RegionControl

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentSetting
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Build your controls
        control_ = New RegionControl(LightFieldApplication)
        ExperimentSettingElement = control_
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return "Regions Of Interest Sample"
        End Get
    End Property

End Class