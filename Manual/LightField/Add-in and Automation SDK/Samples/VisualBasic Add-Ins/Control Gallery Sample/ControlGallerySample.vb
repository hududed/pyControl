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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample is nothing more than a container to show off the default ''''''''''
'''''''''' look and feel of controls from LightField.                           ''''''''''
'''''''''' It makes a view type of add-in and sticks a bunch of controls in it. ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class ControlGallerySample
    Inherits AddInBase
    
    Private control_ As GalleryControlSample

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ExperimentView
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        ' Build your controls
        Dim sv As ScrollViewer = New ScrollViewer()
        control_ = New GalleryControlSample()
        sv.Content = control_
        ExperimentViewElement = sv
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides ReadOnly Property UIExperimentViewTitle As String
        Get
            Return "Control Gallery Sample"
        End Get
    End Property

End Class