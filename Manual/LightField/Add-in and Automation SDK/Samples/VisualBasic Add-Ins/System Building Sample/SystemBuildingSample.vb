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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrate how to determine available devices as well as check the devices in use ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class SystemBuildingSample
    Inherits AddInBase
    
    Private toolBarState_ As Boolean?

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
        'Bring up a wpf dialog  
        Dim wnd As SystemBuildingSampleControl = New SystemBuildingSampleControl(LightFieldApplication)
        'Show the dialog
        wnd.Title = "System Building Sample"
        ShowDialog(wnd)
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
            Return "Demonstrates how to build a system from components"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "System Building Sample"
        End Get
    End Property

End Class