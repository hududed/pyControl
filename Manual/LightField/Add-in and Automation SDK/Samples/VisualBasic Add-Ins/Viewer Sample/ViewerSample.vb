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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrate opening a file through LightField                             ''''''''''
'''''''''' and the putting it into custom WPF view as well as using a LightFieldView ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class AddinViewerSample
    Inherits AddInBase

    Private control_ As ViewerSample

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentView
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Build your controls
        control_ = New ViewerSample(LightFieldApplication)
        ExperimentViewElement = control_
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides ReadOnly Property UIExperimentViewTitle As String
        Get
            Return "Viewer Sample"
        End Get
    End Property

End Class