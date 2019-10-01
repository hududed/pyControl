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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample generates data in memory and dumps it into data views for display. ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class DataSample
    Inherits AddInBase

    Public toolBarState_ As Nullable(Of Boolean)

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.ApplicationToolBar
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        toolBarState_ = Nothing 'Forces it to be a button. True/False would make it a checkbox.
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides Sub UIApplicationToolBarExecute()
        GenerateRamps()
    End Sub
    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean)) 'The button in LightField was pushed
            toolBarState_ = value
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Data Sample"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Generate Linear Ramps frames of data and display them as an example of how to create, modify, and display data"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    'Make a linear ramp of data and display it         
    Private Sub GenerateRamps()
        'Make a frame 200x400 pixels
        Dim frame1(200 * 400) As UShort
        For pix As Integer = 0 To 200 * 400 - 1 Step 1
            frame1(pix) = pix Mod 400
        Next
        'Make a frame 300x500 pixels with a 1k bias
        Dim frame2(300 * 500) As UShort
        For pix As Integer = 0 To 300 * 500 - 1 Step 1
            frame2(pix) = pix Mod 500 + 1000
        Next
        'Get the addin file manager
        Dim datamgr As IDataManager = LightFieldApplication.DataManager
        If datamgr IsNot Nothing Then
            Dim roi As RegionOfInterest = New RegionOfInterest(0, 0, 400, 200, 1, 1)
            Dim roi2 As RegionOfInterest = New RegionOfInterest(0, 0, 500, 300, 1, 1)
            'Simple single region
            Dim imageData As IImageDataSet = datamgr.CreateImageDataSet(frame1, roi, ImageDataFormat.MonochromeUnsigned16)
            'Complex Set contains two regions
            Dim rois = New RegionOfInterest() {roi, roi2}
            Dim buffers As New List(Of Array)
            buffers.Add(frame1)
            buffers.Add(frame2)
            Dim imageDataSets As IImageDataSet = datamgr.CreateImageDataSet(buffers, rois, ImageDataFormat.MonochromeUnsigned16)
            'Display
            Dim display As IDisplay = LightFieldApplication.DisplayManager
            If display IsNot Nothing Then
                'Select data file compare mode with 2 horizontal windows 
                display.ShowDisplay(DisplayLocation.ExperimentWorkspace, DisplayLayout.TwoHorizontal)
                Dim view As IDisplayViewer = Nothing

                'Modify the underlying data a little bit before displaying it.
                ModifyDataExample(imageData, 0)
                'Put the simple data in window 0
                view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, 0)
                view.Display("SimpleRamp", imageData)

                'Modify the underlying data a little bit before displaying it.
                ModifyDataExample(imageDataSets, 1)
                'Put the complex data in window 1
                view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, 1)
                view.Display("ComplexRamp", imageDataSets)
            End If
        End If
    End Sub

    'Change some of the values in the underlying IImageDataSet
    Private Sub ModifyDataExample(ByVal imageData As IImageDataSet, ByVal roiIdx As Integer)
        'Demostrate how to access the data and change it                
        Dim rois As RegionOfInterest() = imageData.Regions
        'Get the width & the height
        Dim h As Integer = rois(roiIdx).Height
        Dim w As Integer = rois(roiIdx).Width
        'Get sub image arrays from the data set 
        Dim row As IImageData = imageData.GetRow(roiIdx, 0, h / 2)
        Dim col As IImageData = imageData.GetColumn(roiIdx, 0, w / 2)
        Dim pix As IImageData = imageData.GetPixel(roiIdx, 0, h / 2, w / 2)
        'Create new arrays to replace data
        Dim rowData(w) As UShort
        Dim colData(h) As UShort
        Dim pixData(1) As UShort
        'Build up new data with values
        For x As Integer = 0 To w - 1
            rowData(x) = 5000 + x
        Next
        For y As Integer = 0 To h - 1
            colData(y) = 10000 + y
        Next
        pixData(0) = 65535 'Bright pixel
        'Push back to original buffer
        row.SetData(rowData)
        col.SetData(colData)
        pix.SetData(pixData)
    End Sub

End Class