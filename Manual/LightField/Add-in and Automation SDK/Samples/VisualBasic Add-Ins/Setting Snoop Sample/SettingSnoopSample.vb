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
Imports System.Reflection
Imports PrincetonInstruments.LightField.AddIns

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrates an Add-in with no user interface that registers for setting changed events and logs them. ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class SettingSnoopSample
    Inherits AddInBase

    Private theExperiment_ As IExperiment 'Keep a single reference instead of getting it each time, since need to hook/unhook the filter.
    Private fullName_ As String

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.None 'Do not support a user interface
        End Get
    End Property

    'Make a list of settings and set the filter to them as well as hook the changed event
    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Set the add-ins discovery root directory to be the current directory
        Dim addinRoot As String = AppDomain.CurrentDomain.BaseDirectory
        fullName_ = Path.Combine(addinRoot, "SettingSnoopSample.txt")
        theExperiment_ = app.Experiment
        'Generate a filter with only the valid settings 
        Dim filteredSettings As List(Of String) = New List(Of String)()
        'Load up the setting strings
        Dim CameraSettings As IEnumerable(Of String) = GetAllNames(GetType(CameraSettings))
        Dim ExperimentSettings As IEnumerable(Of String) = GetAllNames(GetType(ExperimentSettings))
        Dim FilterSettings As IEnumerable(Of String) = GetAllNames(GetType(FilterWheelSettings))
        Dim SpectrometerSettings As IEnumerable(Of String) = GetAllNames(GetType(SpectrometerSettings))
        'Put them all into the filter    
        Dim str As String
        For Each str In CameraSettings 'Camera
            filteredSettings.Add(str)
        Next
        For Each str In ExperimentSettings 'Experiment
            filteredSettings.Add(str)
        Next
        For Each str In FilterSettings 'FilterWheel
            filteredSettings.Add(str)
        Next
        For Each str In SpectrometerSettings  'Spectrometer
            filteredSettings.Add(str)
        Next
        'Connect the setting change handler
        AddHandler theExperiment_.SettingChanged, AddressOf Experiment_SettingChanged
        'Apply the filter
        theExperiment_.FilterSettingChanged(filteredSettings)
        'Also monitor System building events
        AddHandler theExperiment_.ExperimentUpdating, AddressOf Experiment_ExperimentUpdating
        AddHandler theExperiment_.ExperimentUpdated, AddressOf Experiment_ExperimentUpdated
    End Sub

    'Disconnect the event handler from the event
    Public Sub Deactivate()
        RemoveHandler theExperiment_.SettingChanged, AddressOf Experiment_SettingChanged
        RemoveHandler theExperiment_.ExperimentUpdating, AddressOf Experiment_ExperimentUpdating
        RemoveHandler theExperiment_.ExperimentUpdated, AddressOf Experiment_ExperimentUpdated
    End Sub

    'Get all the setting names of a given type
    Private Function GetAllNames(type As Type) As IEnumerable(Of String)
        Dim fieldInfos As FieldInfo() = type.GetFields(BindingFlags.Public Or BindingFlags.Static)
        Return fieldInfos.Where(Function(fi) fi.IsLiteral AndAlso Not fi.IsInitOnly).[Select](Function(fi) fi.GetValue(Nothing).ToString())
    End Function

    'When a setting in the filter list changes, this will get called by the application.
    Private Sub Experiment_SettingChanged(sender As Object, e As SettingChangedEventArgs)
        'Setting name
        Dim settingName As String = ":  Setting:" + e.Setting
        'Setting value
        Dim settingValue As String = " Value: " + theExperiment_.GetValue(e.Setting).ToString()
        'Time stamp
        Dim dateTimeOffset As DateTimeOffset = dateTimeOffset.Now
        'Stream writer set to append if the file is there
        Using fs As New StreamWriter(fullName_, True)
            If fs IsNot Nothing Then
                fs.WriteLine(dateTimeOffset.ToString() + settingName + settingValue)
            End If
        End Using
    End Sub

    Private Sub Experiment_ExperimentUpdated(sender As Object, e As ExperimentUpdatedEventArgs)
        'Time stamp
        Dim dateTimeOffset As DateTimeOffset = dateTimeOffset.Now
        'Stream writer set to append if the file is there
        Using fs As New StreamWriter(fullName_, True)
            If fs IsNot Nothing Then
                fs.WriteLine(dateTimeOffset.ToString() + " ExperimentUpdated Event")
            End If
        End Using
    End Sub

    Private Sub Experiment_ExperimentUpdating(sender As Object, e As ExperimentUpdatingEventArgs)
        'Time stamp
        Dim dateTimeOffset As DateTimeOffset = dateTimeOffset.Now
        'Stream writer set to append if the file is there
        Using fs As New StreamWriter(fullName_, True)
            If fs IsNot Nothing Then
                fs.WriteLine(dateTimeOffset.ToString() + " ExperimentUpdating Event")
            End If
        End Using
    End Sub

End Class