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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Acquire multiple frames and show the meta data for each frame ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class AddinMetaDataSample
    Inherits AddInBase

    Private control_ As MetadataSample

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentSetting
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Build your controls            
        control_ = New MetadataSample(LightFieldApplication)
        ExperimentSettingElement = control_
    End Sub

    Public Sub Deactivate()
    End Sub


    Public Overrides ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return "Metadata Sample"
        End Get
    End Property

End Class