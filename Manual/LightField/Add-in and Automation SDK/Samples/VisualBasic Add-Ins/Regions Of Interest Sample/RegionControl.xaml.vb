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

Public Class RegionControl
    Private application_ As ILightFieldApplication
    Private experiment_ As IExperiment
    Private xbin_ As Integer = 1
    Private ybin_ As Integer = 1
    Private rowsbinned_ As Integer = 1
    Private x_ As Integer = 0
    Private y_ As Integer = 0
    Private w_ As Integer = 1
    Private h_ As Integer = 1
    Private xb_ As Integer = 1
    Private yb_ As Integer = 0
    Private controlsInitialized_ As Boolean = False

    Public ReadOnly Property CameraExist As Boolean
        Get
            Dim exist As Boolean = experiment_.Exists(CameraSettings.AcquisitionFrameRate)
            If exist And Not controlsInitialized_ Then
                'Get the full size
                Dim full As RegionOfInterest = experiment_.FullSensorRegion
                'Full sensor binned
                Dim binned As RegionOfInterest = experiment_.BinnedSensorRegion
                xbin_ = binned.XBinning
                ybin_ = binned.YBinning
                FullSensorBinW.Text = xbin_.ToString()
                FullSensorBinH.Text = ybin_.ToString()
                'Line sensor
                Dim line As RegionOfInterest = experiment_.LineSensorRegion
                rowsbinned_ = line.YBinning
                RowsBinnedH.Text = rowsbinned_.ToString()
                'Custom region
                Dim custom As RegionOfInterest() = experiment_.CustomRegions
                x_ = custom(0).X
                RegionX.Text = x_.ToString()
                w_ = custom(0).Width
                RegionWidth.Text = w_.ToString()
                xb_ = custom(0).XBinning
                XBin.Text = xb_.ToString()
                y_ = custom(0).Y
                RegionY.Text = y_.ToString()
                h_ = custom(0).Height
                RegionHeight.Text = h_.ToString()
                yb_ = custom(0).YBinning
                YBin.Text = yb_.ToString()
                'Set initialized
                controlsInitialized_ = True
            End If
            Return exist
        End Get
    End Property

    Public Sub New(app As ILightFieldApplication)
        application_ = app
        ' This call is required by the designer.
        InitializeComponent()
        ' Add any initialization after the InitializeComponent() call.
        'Get the experiment since we need it for everything
        experiment_ = application_.Experiment
        'Set to full chip
        FullChip.IsChecked = True
    End Sub

    Private Sub radioButton1_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If CameraExist Then
            experiment_.SetFullSensorRegion()
        End If
    End Sub

    Private Sub FullSensorBinned_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If CameraExist Then
            experiment_.SetBinnedSensorRegion(xbin_, ybin_)
        End If
    End Sub

    Private Sub FullSensorBinW_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If FullSensorBinW.Text IsNot String.Empty And controlsInitialized_ Then
            xbin_ = Convert.ToInt32(FullSensorBinW.Text)
            If CameraExist Then
                experiment_.SetBinnedSensorRegion(xbin_, ybin_)
            End If
        End If
    End Sub

    Private Sub FullSensorBinH_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If FullSensorBinH.Text IsNot String.Empty And controlsInitialized_ Then
            ybin_ = Convert.ToInt32(FullSensorBinH.Text)
            If CameraExist Then
                experiment_.SetBinnedSensorRegion(xbin_, ybin_)
            End If
        End If
    End Sub

    Private Sub RowsBinned_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If CameraExist Then
            experiment_.SetLineSensorRegion(rowsbinned_)
        End If
    End Sub

    Private Sub RowsBinnedH_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If RowsBinnedH.Text IsNot String.Empty And controlsInitialized_ Then
            rowsbinned_ = Convert.ToInt32(RowsBinnedH.Text)
            If CameraExist Then
                experiment_.SetLineSensorRegion(rowsbinned_)
            End If
        End If
    End Sub

    Private Sub CustomRegion_Checked(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim roi As RegionOfInterest = New RegionOfInterest(x_, y_, w_, h_, xb_, yb_)
        Dim regions As RegionOfInterest() = {roi}
        If CameraExist Then
            experiment_.SetCustomRegions(regions)
        End If
    End Sub

    Private Sub RegionX_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If RegionX.Text IsNot String.Empty And controlsInitialized_ Then
            x_ = Convert.ToInt32(RegionX.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub RegionY_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If RegionY.Text IsNot String.Empty And controlsInitialized_ Then
            y_ = Convert.ToInt32(RegionY.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub RegionWidth_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If RegionWidth.Text IsNot String.Empty And controlsInitialized_ Then
            w_ = Convert.ToInt32(RegionWidth.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub RegionHeight_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If RegionHeight.Text IsNot String.Empty And controlsInitialized_ Then
            h_ = Convert.ToInt32(RegionHeight.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub XBin_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If XBin.Text IsNot String.Empty And controlsInitialized_ Then
            xb_ = Convert.ToInt32(XBin.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub YBin_TextChanged(sender As System.Object, e As System.Windows.Controls.TextChangedEventArgs)
        If YBin.Text IsNot String.Empty And controlsInitialized_ Then
            yb_ = Convert.ToInt32(YBin.Text)
            CustomRegion_Checked(Me, New RoutedEventArgs())
        End If
    End Sub

    Private Sub button1_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Check if can acquire
        If Not ValidateAcquisition() Then
            Exit Sub
        End If
        'Snap an image
        If CameraExist Then
            experiment_.Acquire()
        End If
    End Sub

    Private Function ValidateAcquisition() As Boolean
        Dim camera As IDevice = Nothing
        For Each device As IDevice In experiment_.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                camera = device
            End If
        Next
        If camera Is Nothing Then
            MsgBox("This sample requires a camera!")
            Return False
        End If
        If Not experiment_.IsReadyToRun Then
            MsgBox("The system is not ready for acquisition, is there an error?")
            Return False
        End If
        Return True
    End Function
End Class