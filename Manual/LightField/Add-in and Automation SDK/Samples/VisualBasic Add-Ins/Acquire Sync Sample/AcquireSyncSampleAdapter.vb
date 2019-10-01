Imports System.AddIn
Imports System.AddIn.Pipeline
Imports System.Drawing
Imports System.Windows
Imports PrincetonInstruments.LightField.AddIns

#Region "LightField Add-in Adapter"

' This class exposes the add-in to lightfield to simplify the implementation of the add-in itself
<AddIn("Acquire Synchronous Sample (VB)", Version:="1.0.0", Publisher:="Teledyne Princeton Instruments", Description:="Shows an example of synchronous acquisition")>
<QualificationData("IsSample", "True")>
Public Class AcquireSyncSampleAdapter
    Implements ILightFieldAddIn

    Private impl_ As AcquireSyncSample

    Public Sub Activate(ByVal lightField As ILightFieldApplication) Implements ILightFieldAddIn.Activate
        impl_ = New AcquireSyncSample
        impl_.Activate(lightField)
    End Sub

    Public Sub Deactivate() Implements ILightFieldAddIn.Deactivate
        impl_.Deactivate()
    End Sub

    Public Sub RequestHelp(ByVal helpTopicID As Integer) Implements ILightFieldAddIn.RequestHelp
        impl_.RequestHelp(helpTopicID)
    End Sub

    Public Sub UIApplicationToolBarExecute() Implements ILightFieldAddIn.UIApplicationToolBarExecute
        impl_.UIApplicationToolBarExecute()
    End Sub

    Public Sub UIDataToolBarExecute() Implements ILightFieldAddIn.UIDataToolBarExecute
        impl_.UIDataToolBarExecute()
    End Sub

    Public Sub UIMenuExecute() Implements ILightFieldAddIn.UIMenuExecute
        impl_.UIMenuExecute()
    End Sub

    Public ReadOnly Property UIApplicationToolBarBitmap As Bitmap Implements ILightFieldAddIn.UIApplicationToolBarBitmap
        Get
            Return impl_.UIApplicationToolBarBitmap
        End Get
    End Property

    Public ReadOnly Property UIApplicationToolBarHelpTopicID As Integer? Implements ILightFieldAddIn.UIApplicationToolBarHelpTopicID
        Get
            Return impl_.UIApplicationToolBarHelpTopicID
        End Get
    End Property

    Public Property UIApplicationToolBarIsChecked As Boolean? Implements ILightFieldAddIn.UIApplicationToolBarIsChecked
        Get
            Return impl_.UIApplicationToolBarIsChecked
        End Get
        Set(ByVal value As Boolean?)
            impl_.UIApplicationToolBarIsChecked = value
        End Set
    End Property

    Public ReadOnly Property UIApplicationToolBarIsEnabled As Boolean Implements ILightFieldAddIn.UIApplicationToolBarIsEnabled
        Get
            Return impl_.UIApplicationToolBarIsEnabled
        End Get
    End Property

    Public ReadOnly Property UIApplicationToolBarTitle As String Implements ILightFieldAddIn.UIApplicationToolBarTitle
        Get
            Return impl_.UIApplicationToolBarTitle
        End Get
    End Property

    Public ReadOnly Property UIApplicationToolBarToolTip As String Implements ILightFieldAddIn.UIApplicationToolBarToolTip
        Get
            Return impl_.UIApplicationToolBarToolTip
        End Get
    End Property

    Public ReadOnly Property UIDataToolBarBitmap As Bitmap Implements ILightFieldAddIn.UIDataToolBarBitmap
        Get
            Return impl_.UIDataToolBarBitmap
        End Get
    End Property

    Public ReadOnly Property UIDataToolBarHelpTopicID As Integer? Implements ILightFieldAddIn.UIDataToolBarHelpTopicID
        Get
            Return impl_.UIDataToolBarHelpTopicID
        End Get
    End Property

    Public Property UIDataToolBarIsChecked As Boolean? Implements ILightFieldAddIn.UIDataToolBarIsChecked
        Get
            Return impl_.UIDataToolBarIsChecked
        End Get
        Set(value As Boolean?)
            impl_.UIDataToolBarIsChecked = value
        End Set
    End Property

    Public ReadOnly Property UIDataToolBarIsEnabled As Boolean Implements ILightFieldAddIn.UIDataToolBarIsEnabled
        Get
            Return impl_.UIDataToolBarIsEnabled
        End Get
    End Property

    Public ReadOnly Property UIDataToolBarTitle As String Implements ILightFieldAddIn.UIDataToolBarTitle
        Get
            Return impl_.UIDataToolBarTitle
        End Get
    End Property

    Public ReadOnly Property UIDataToolBarToolTip As String Implements ILightFieldAddIn.UIDataToolBarToolTip
        Get
            Return impl_.UIDataToolBarToolTip
        End Get
    End Property

    Public ReadOnly Property UIExperimentSetting As FrameworkElement Implements ILightFieldAddIn.UIExperimentSetting
        Get
            Return impl_.UIExperimentSetting
        End Get
    End Property

    Public ReadOnly Property UIExperimentSettingHelpTopicID As Integer? Implements ILightFieldAddIn.UIExperimentSettingHelpTopicID
        Get
            Return impl_.UIExperimentSettingHelpTopicID
        End Get
    End Property

    Public ReadOnly Property UIExperimentSettingTitle As String Implements ILightFieldAddIn.UIExperimentSettingTitle
        Get
            Return impl_.UIExperimentSettingTitle
        End Get
    End Property

    Public ReadOnly Property UIExperimentView As FrameworkElement Implements ILightFieldAddIn.UIExperimentView
        Get
            Return impl_.UIExperimentView
        End Get
    End Property

    Public ReadOnly Property UIExperimentViewHelpTopicID As Integer? Implements ILightFieldAddIn.UIExperimentViewHelpTopicID
        Get
            Return impl_.UIExperimentViewHelpTopicID
        End Get
    End Property

    Public ReadOnly Property UIExperimentViewTitle As String Implements ILightFieldAddIn.UIExperimentViewTitle
        Get
            Return impl_.UIExperimentViewTitle
        End Get
    End Property

    Public Property UIMenuIsChecked As Boolean? Implements ILightFieldAddIn.UIMenuIsChecked
        Get
            Return impl_.UIMenuIsChecked
        End Get
        Set(value As Boolean?)
            impl_.UIMenuIsChecked = value
        End Set
    End Property

    Public ReadOnly Property UIMenuIsEnabled As Boolean Implements ILightFieldAddIn.UIMenuIsEnabled
        Get
            Return impl_.UIMenuIsEnabled
        End Get
    End Property

    Public ReadOnly Property UIMenuTitle As String Implements ILightFieldAddIn.UIMenuTitle
        Get
            Return impl_.UIMenuTitle
        End Get
    End Property

    Public ReadOnly Property UISupport As UISupport Implements ILightFieldAddIn.UISupport
        Get
            Return impl_.UISupport
        End Get
    End Property

    Public Custom Event UISupportChanged As EventHandler(Of UISupportChangedEventArgs) Implements ILightFieldAddIn.UISupportChanged
        AddHandler(ByVal value As EventHandler(Of UISupportChangedEventArgs))
            AddHandler impl_.UISupportChanged, value
        End AddHandler
        RemoveHandler(ByVal value As EventHandler(Of UISupportChangedEventArgs))
            RemoveHandler impl_.UISupportChanged, value
        End RemoveHandler
        RaiseEvent()
        End RaiseEvent
    End Event

End Class

#End Region
