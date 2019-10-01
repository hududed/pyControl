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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample shows adding add-in that can dynamically change '''''''''' 
'''''''''' its appearance and what LightField zones it suports UI for  ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class CompositeSample
    Inherits AddInBase

    Private control_ As ExperimentView
    Private control2_ As System.Windows.Controls.Button

    Public ExperimentSetting As Component
    Public ExperimentView As Component
    Public AppToolBar As Component
    Public DataToolBar As Component
    Public Menu As Component

    'For this event we have to define it as custom and connect the interfaces implementation to the base 
    'implementation so that the connection is made. Otherwise the event is completely overridden and will not work properly.
    'Since this is the only event the base class supports, it is the only event that needs this special handling.
    Public Shadows Custom Event UISupportChanged As EventHandler(Of UISupportChangedEventArgs)
        AddHandler(ByVal value As EventHandler(Of UISupportChangedEventArgs))
            AddHandler MyBase.UISupportChanged, value
        End AddHandler

        RemoveHandler(ByVal value As EventHandler(Of UISupportChangedEventArgs))
            RemoveHandler MyBase.UISupportChanged, value
        End RemoveHandler

        'RaiseEvent does not need to do anything we are only concerned with listening for the event. 
        'The base class method will raise the event but only if it detects listeners.
        RaiseEvent()
        End RaiseEvent
    End Event

    'Dynamically changes support based on CheckBoxes
    Public ReadOnly Property UISupport As UISupport
        Get
            Dim flags As UISupport = UISupport.ExperimentView
            If ExperimentSetting IsNot Nothing Then
                If ExperimentSetting.CanShow Then
                    flags = flags Or UISupport.ExperimentSetting
                End If
            End If
            If Menu IsNot Nothing Then
                If Menu.CanShow Then
                    flags = flags Or UISupport.Menu
                End If
            End If
            If AppToolBar IsNot Nothing Then
                If AppToolBar.CanShow Then
                    flags = flags Or UISupport.ApplicationToolBar
                End If
            End If
            If DataToolBar IsNot Nothing Then
                If DataToolBar.CanShow Then
                    flags = flags Or UISupport.DataToolBar
                End If
            End If

            Return flags
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app

        'Build your controls
        control_ = New ExperimentView(Me)
        ExperimentViewElement = control_

        'Simple button 
        control2_ = New Button()
        control2_.Content = "Push!"
        ExperimentSettingElement = control2_
    End Sub

    Public Sub Deactivate()
    End Sub

    'Fire event to the application (change all but the view!)
    Friend Sub DingEvent()
        Dim item As UISupport = UISupport.DataToolBar Or UISupport.ApplicationToolBar Or UISupport.ExperimentSetting Or UISupport.Menu
        ChangeExperimentSetting()
        RequestUIRefresh(item)
    End Sub

    'If we change one of the UI elements it must be recreated by the addin
    'or reference a different object. 
    Public Sub ChangeExperimentSetting()
        control2_ = New Button()
        control2_.Content = "Push!"
        ExperimentSettingElement = control2_
    End Sub

    'UIMenu
    Public Shadows ReadOnly Property UIMenuISEnabled As Boolean
        Get
            Return Menu.IsEnabled
        End Get
    End Property

    Public Overrides ReadOnly Property UIMenuTitle As String
        Get
            Return Menu.Title
        End Get
    End Property

    Public Overrides Property UIMenuIsChecked As Nullable(Of Boolean)
        Get
            Return Menu.State
        End Get
        Set(value As Nullable(Of Boolean))
            Menu.State = value
        End Set
    End Property

    Public Overrides Sub UIMenuExecute()
    End Sub

    'UIExperimentView
    Public Overrides ReadOnly Property UIExperimentViewTitle As String
        Get
            Return "Composite Sample"
        End Get
    End Property

    'UIExperimentSetting
    Public Overrides ReadOnly Property UIExperimentSettingTitle As String
        Get
            Return ExperimentSetting.Title
        End Get
    End Property

    'UIApplicationToolBar
    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return AppToolBar.State
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            AppToolBar.State = value
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return AppToolBar.Tip
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return AppToolBar.IsEnabled
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return AppToolBar.Title
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarHelpTopicID As Nullable(Of Integer)
        Get
            Return 1
        End Get
    End Property

    Public Overrides Sub UIApplicationToolBarExecute()
    End Sub

    'UIDataToolBar
    Public Overrides ReadOnly Property UIDataToolBarTitle As String
        Get
            Return DataToolBar.Title
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarToolTip As String
        Get
            Return DataToolBar.Tip
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarIsEnabled As Boolean
        Get
            Return DataToolBar.IsEnabled
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarHelpTopicID As Nullable(Of Integer)
        Get
            Return 1
        End Get
    End Property

    Public Overrides Property UIDataToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return DataToolBar.State
        End Get
        Set(value As Nullable(Of Boolean))
            DataToolBar.State = value
        End Set
    End Property

    Public Overrides Sub UIDataToolBarExecute()
    End Sub
End Class

'Helper class that ties things  together     
Public Class Component
    'Private backing
    Private toolTip_ As String
    Private title_ As String
    Private executable_ As Boolean
    Private state_ As Nullable(Of Boolean)
    Private visiblity_ As Boolean
    Private type_ As UISupport

    'Create with settings
    Public Sub New(ByVal title As String, ByVal tip As String, ByVal exec As Boolean, ByVal state As Nullable(Of Boolean), ByVal vis As Boolean, ByVal type As UISupport)
        title_ = title
        toolTip_ = tip
        executable_ = exec
        state_ = state
        visiblity_ = vis
        type_ = type
    End Sub

    'Public properties
    Public ReadOnly Property Type As UISupport
        Get
            Return type_
        End Get
    End Property

    Public ReadOnly Property CanShow As Boolean
        Get
            Return visiblity_
        End Get
    End Property

    Public Property State As Nullable(Of Boolean)
        Get
            Return state_
        End Get
        Set(value As Nullable(Of Boolean))
            state_ = value
        End Set
    End Property

    Public ReadOnly Property IsEnabled As Boolean
        Get
            Return executable_
        End Get
    End Property

    Public ReadOnly Property Tip As String
        Get
            Return toolTip_
        End Get
    End Property

    Public ReadOnly Property Title As String
        Get
            Return title_
        End Get
    End Property
End Class
