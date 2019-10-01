
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

''''''''''''''''''''''''''''''
'''''''''' TEMPLATE ''''''''''
''''''''''''''''''''''''''''''
'<AddIn("VB_TEMPLATE", Version:="1.0.0", Publisher:="Princeton Instruments", Description:="This sample Add-in from VB.")>
Public Class Template
    Inherits AddInBase
    Implements ILightFieldAddIn

#Region "Other implementations"

#Region "Event"
    'For this event we have to define it as custom and connect the interfaces implementation to the base 
    'implementation so that the connection is made. Otherwise the event is completely overridden and will not work properly.
    'Since this is the only event the base class supports, it is the only event that needs this special handling.
    Public Shadows Custom Event UISupportChanged As EventHandler(Of UISupportChangedEventArgs) Implements ILightFieldAddIn.UISupportChanged
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
#End Region

#Region "Method"
    Public ReadOnly Property UISupport As UISupport Implements ILightFieldAddIn.UISupport
        Get
            Return UISupport.ApplicationToolBar
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication) Implements ILightFieldAddIn.Activate
    End Sub

    Public Sub Deactive() Implements ILightFieldAddIn.Deactivate
    End Sub

    Public Overrides Sub UIApplicationToolBarExecute() Implements ILightFieldAddIn.UIApplicationToolBarExecute
        Throw New NotImplementedException("UIApplicationToolBarExecute has no implementation!")
    End Sub

    Public Overrides Sub UIMenuExecute() Implements ILightFieldAddIn.UIMenuExecute
    End Sub

    Public Overrides Sub RequestHelp(ByVal helpTopicID As Integer) Implements ILightFieldAddIn.RequestHelp
        Throw New NotImplementedException("RequestHelp has no implementation!")
    End Sub

    Public Overrides Sub UIDataToolBarExecute() Implements ILightFieldAddIn.UIDataToolBarExecute
        Throw New NotImplementedException("UIDataToolBarExecute has no implementation!")
    End Sub
#End Region

#Region "Property"
    'UIMenu
    Public Shadows ReadOnly Property UIMenuISEnabled As Boolean Implements ILightFieldAddIn.UIMenuIsEnabled
        Get
            Throw New NotImplementedException("UIMenuCanExecute has no get implementation!")
            'Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIMenuTitle As String Implements ILightFieldAddIn.UIMenuTitle
        Get
            Throw New NotImplementedException("UIMenuTitle has no implementation!")
            'Return Nothing
        End Get
    End Property

    Public Overrides Property UIMenuIsChecked As Nullable(Of Boolean) Implements ILightFieldAddIn.UIMenuIsChecked
        Get
            Throw New NotImplementedException("UIMenuIsChecked has no get implementation!")
            'Return Nothing
        End Get
        Set(value As Nullable(Of Boolean))
            Throw New NotImplementedException("UIMenuIsChecked has no set implementation!")
        End Set
    End Property

    'UIApplicationToolBar
    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean) Implements ILightFieldAddIn.UIApplicationToolBarIsChecked
        Get
            Throw New NotImplementedException("UIApplicationToolBarIsChecked has no get implementation!")
            'Return Nothing
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            Throw New NotImplementedException("UIApplicationToolBarIsChecked has no set implementation!")
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String Implements ILightFieldAddIn.UIApplicationToolBarToolTip
        Get
            Throw New NotImplementedException("UIApplicationToolBarToolTip has no implementation!")
            'Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean Implements ILightFieldAddIn.UIApplicationToolBarIsEnabled
        Get
            Throw New NotImplementedException("UIApplicationToolbarCanExecute has no implementation!")
            'Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String Implements ILightFieldAddIn.UIApplicationToolBarTitle
        Get
            Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarHelpTopicID As Nullable(Of Integer) Implements ILightFieldAddIn.UIApplicationToolBarHelpTopicID
        Get
            Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarBitmap As Drawing.Bitmap Implements ILightFieldAddIn.UIApplicationToolBarBitmap
        Get
            Return Nothing
        End Get
    End Property

    'UIDataToolBar
    Public Overrides ReadOnly Property UIDataToolBarTitle As String Implements ILightFieldAddIn.UIDataToolBarTitle
        Get
            Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarToolTip As String Implements ILightFieldAddIn.UIDataToolBarToolTip
        Get
            Throw New NotImplementedException("UIDataToolBarToolTip has no implementation!")
            'Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarIsEnabled As Boolean Implements ILightFieldAddIn.UIDataToolBarIsEnabled
        Get
            Throw New NotImplementedException("UIDataToolbarCanExecute has no implementation!")
            'Return False
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarBitmap As Drawing.Bitmap Implements ILightFieldAddIn.UIDataToolBarBitmap
        Get
            Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarHelpTopicID As Nullable(Of Integer) Implements ILightFieldAddIn.UIDataToolBarHelpTopicID
        Get
            Return Nothing
        End Get
    End Property

    Public Overrides Property UIDataToolBarIsChecked As Nullable(Of Boolean) Implements ILightFieldAddIn.UIDataToolBarIsChecked
        Get
            Throw New NotImplementedException("UIDataToolBarIsChecked has no get implementation!")
            'Return Nothing
        End Get
        Set(value As Nullable(Of Boolean))
            Throw New NotImplementedException("UIDataToolBarIsChecked has no set implementation!")
        End Set
    End Property

    'UIExperimentSetting
    Public Shadows ReadOnly Property UIExperimentSetting As Windows.FrameworkElement Implements ILightFieldAddIn.UIExperimentSetting
        Get
            If ExperimentSettingElement Is Nothing Then
                Throw New NotImplementedException("UIExperiment has no implementation!")
            Else
                Return ExperimentSettingElement
            End If
        End Get
    End Property

    Public Overrides ReadOnly Property UIExperimentSettingTitle As String Implements ILightFieldAddIn.UIExperimentSettingTitle
        Get
            Throw New NotImplementedException("UIExperimentTitle has no implementation!")
            'Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIExperimentSettingHelpTopicID As Nullable(Of Integer) Implements ILightFieldAddIn.UIExperimentSettingHelpTopicID
        Get
            Return Nothing
        End Get
    End Property

    'UIExperimentView
    Public Overrides ReadOnly Property UIExperimentView As Windows.FrameworkElement Implements ILightFieldAddIn.UIExperimentView
        Get
            If ExperimentViewElement Is Nothing Then
                Throw New NotImplementedException("UIExperimentView has no implementation!")
            Else
                Return ExperimentViewElement
            End If
        End Get
    End Property

    Public Overrides ReadOnly Property UIExperimentViewTitle As String Implements ILightFieldAddIn.UIExperimentViewTitle
        Get
            Throw New NotImplementedException("UIExperimentViewTitle has no implementation!")
            'Return Nothing
        End Get
    End Property

    Public Overrides ReadOnly Property UIExperimentViewHelpTopicID As Nullable(Of Integer) Implements ILightFieldAddIn.UIExperimentViewHelpTopicID
        Get
            Return Nothing
        End Get
    End Property
#End Region

#End Region
End Class