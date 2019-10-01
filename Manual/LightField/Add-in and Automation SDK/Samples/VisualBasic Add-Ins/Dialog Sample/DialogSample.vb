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

'''''''''''''''''''''''''''''''''''''''''
'''''''''' MODAL DIALOG SAMPLE ''''''''''
'''''''''''''''''''''''''''''''''''''''''
Public Class ModalDialogSample
    Inherits AddInBase

    Public toolBarState_ As Nullable(Of Boolean)

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ApplicationToolBar
        End Get
    End Property

    Public Shadows Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            toolBarState_ = value 'The button in LightField was pushed
        End Set
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Open a modal dialog window that inherits its styles from LightField"
        End Get
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Modal Dialog Sample"
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'The toolbar item is in simple button style
        toolBarState_ = Nothing
        ' Initialize the AddInBase with the current dispatcher
        'Initialize(Application.Current.Dispatcher, "Modal Dialog Sample (VB)")
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Shadows Sub UIApplicationToolBarExecute()
        'Show WinForm window
        'Dim wnd As New DialogSampleWindow_WinForm()
        'wnd.Text = "Modal Dialog Example"
        'wnd.ShowDialog()

        'Bring up a WPF dialog and show the dialog
        Dim wnd As New DialogSampleWindow()
        wnd.Title = "Modal Dialog Example"
        wnd.ShowDialog()
    End Sub

End Class

''''''''''''''''''''''''''''''''''''''''''''
'''''''''' MODELESS DIALOG SAMPLE ''''''''''
''''''''''''''''''''''''''''''''''''''''''''
Public Class ModelessDialogSample
    Inherits AddInBase

    Public toolBarState_ As Nullable(Of Boolean)

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ApplicationToolBar
        End Get
    End Property

    Public Shadows Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            toolBarState_ = value 'The button in LightField was pushed
        End Set
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Open a modal dialog window that inherits its styles from LightField"
        End Get
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Shadows ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Modeless Dialog Sample"
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        'Simple button style
        toolBarState_ = Nothing
        ' Initialize the AddInBase with the current dispatcher
        'Initialize(Application.Current.Dispatcher, "Modeless Dialog Sample (VB)")
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Shadows Sub UIApplicationToolBarExecute()
        'Bring up a WPF dialog
        Dim wnd As New DialogSampleWindow()
        'Call the base class
        wnd.Title = "Modeless Dialog Example"
        wnd.Show()
    End Sub

End Class
