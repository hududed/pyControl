Imports System
Imports System.Collections.Generic
Imports System.Linq
Imports System.Text
Imports System.Windows
Imports System.Windows.Controls
Imports System.Windows.Data
Imports System.Windows.Documents
Imports System.Windows.Input
Imports System.Windows.Media
Imports System.Windows.Media.Imaging
Imports System.Windows.Navigation
Imports System.Windows.Shapes
Imports PrincetonInstruments.LightField.AddIns

'Interaction logic for SystemBuildingSampleControl.xaml
Public Class SystemBuildingSampleControl
    Private application_ As ILightFieldApplication
    Private experiment_ As IExperiment

    'Modal dialog constructor
    Public Sub New(app As ILightFieldApplication)
        application_ = app
        experiment_ = app.Experiment
        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        'Initial Update
        RefreshListBoxes()
        'Connect to device changed event
        AddHandler experiment_.AvailableDevicesChanged, AddressOf Experiment_DeviceChanged
        AddHandler experiment_.ExperimentDevicesChanged, AddressOf Experiment_DeviceChanged
        AddHandler Closed, AddressOf Window_Closed
    End Sub


    'Add from Available to Experiment
    Private Sub Add_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim idx As Integer = AvailableList.SelectedIndex
        Dim count As Integer = application_.Experiment.AvailableDevices.Count
        If idx >= 0 And idx < count Then 'Validate index
            application_.Experiment.Add(application_.Experiment.AvailableDevices(idx))
            RefreshListBoxes()
        End If
    End Sub

    'Remove from Experiment
    Private Sub Remove_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim idx As Integer = ExperimentList.SelectedIndex
        Dim count As Integer = application_.Experiment.ExperimentDevices.Count
        If idx >= 0 And idx < count Then 'Validate index
            application_.Experiment.Remove(application_.Experiment.ExperimentDevices(idx))
            RefreshListBoxes()
        End If
    End Sub

    'Clear all Experiment
    Private Sub ClearAll_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        application_.Experiment.Clear()
        RefreshListBoxes()
    End Sub

    'If get a device changed, update our listboxes to reflect the new current state.
    Private Sub Experiment_DeviceChanged(sender As Object, e As DevicesChangedEventArgs)
        RefreshListBoxes()
    End Sub

    'Update ListBox from application
    Private Sub RefreshListBoxes()
        'Available list
        Dim avail As IList(Of IDevice) = application_.Experiment.AvailableDevices
        AvailableList.Items.Clear()
        For Each device As IDevice In avail
            Dim s As String = String.Format("{0} {1} {2}", device.Model, device.SerialNumber, device.Type.ToString())
            AvailableList.Items.Add(s)
        Next
        'Experiment list
        Dim exper As IList(Of IDevice) = application_.Experiment.ExperimentDevices
        ExperimentList.Items.Clear()
        For Each device As IDevice In exper
            Dim s As String = String.Format("{0} {1} {2}", device.Model, device.SerialNumber, device.Type.ToString())
            ExperimentList.Items.Add(s)
        Next
    End Sub

    Private Sub Window_Closed(sender As System.Object, e As System.EventArgs)
        'Disconnect to device changed event
        RemoveHandler experiment_.AvailableDevicesChanged, AddressOf Experiment_DeviceChanged
        RemoveHandler experiment_.ExperimentDevicesChanged, AddressOf Experiment_DeviceChanged
    End Sub
End Class