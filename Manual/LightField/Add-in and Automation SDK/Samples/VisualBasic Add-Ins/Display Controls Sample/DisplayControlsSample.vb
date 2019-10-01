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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrates most of the controls for adjustment on a view of data ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class AddinDisplayControlsSample
    Inherits AddInBase

    Public toolBarState_ As Boolean?

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ApplicationToolBar
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Button style
        toolBarState_ = Nothing
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides Sub UIApplicationToolBarExecute()
        'Build your controls
        Dim wnd As DisplayControlsSample = New DisplayControlsSample(LightFieldApplication)
        'Call the base class
        wnd.Title = "Display Controls Sample"
        Show(wnd)
    End Sub

    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean)) 'The button in LightField was pushed
            toolBarState_ = value
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Shows how to use controls to affect the graph/image viewer"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Display Controls Sample"
        End Get
    End Property

End Class
