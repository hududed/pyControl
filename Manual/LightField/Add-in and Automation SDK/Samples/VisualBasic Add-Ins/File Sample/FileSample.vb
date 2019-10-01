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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Generate data in memory and stores the data in two SPE files at user-designed location. ''''''''''
'''''''''' One file contrains multiple frames with a single region,                                ''''''''''
'''''''''' and the other contains a single frame with multiple regions.                            ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class FileSample
    Inherits AddInBase

    Public toolBarState_ As Boolean?

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.DataToolBar
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        'Capture interface
        LightFieldApplication = app
        toolBarState_ = Nothing 'Forces it to be a button. True/False would make it a checkbox.
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides Sub UIDataToolBarExecute()
        GenerateFiles()
    End Sub

    Public Overrides ReadOnly Property UIDataToolBarTitle As String
        Get
            Return "File Sample"
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarToolTip As String
        Get
            Return "Generate a multi-frame single region file and a multi region single frame file sample"
        End Get
    End Property

    Public Overrides ReadOnly Property UIDataToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Overrides Property UIDataToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(value As Nullable(Of Boolean)) 'The button In LightField was pushed
            GenerateFiles()
        End Set
    End Property

    'The following routine demonstrates how to create files using the LightField Addin SDK. 
    'Create one File with 2 frames and 1 region  (TwoFrameOneRoi.Spe)
    'Create one File with 1 frames and 2 regions (OneFrameTwoRoi.Spe)        
    Private Sub GenerateFiles()
        Dim filemgr As IFileManager = LightFieldApplication.FileManager 'Get the addin file manager
        If filemgr Is Nothing Then
            Exit Sub
        End If

        'Part 1: two frames one region
        Dim w1() As Integer = {100}
        Dim h1() As Integer = {200}
        Dim frame1(100 * 200) As UShort
        Dim frame2(100 * 200) As UShort
        For pix As Integer = 0 To 100 * 200 - 1
            frame1(pix) = pix
            frame2(pix) = pix * 2
        Next
        'Folder Selector
        Dim dialog As Object = New System.Windows.Forms.FolderBrowserDialog()
        dialog.Description = "Please choose folder for resulting SPE file(s)."
        Dim result As System.Windows.Forms.DialogResult = dialog.ShowDialog()
        If result <> System.Windows.Forms.DialogResult.OK Then 'If do not want to write the files.
            Exit Sub
        End If
        Dim path As String = dialog.SelectedPath 'Local variable containing path
        'Create a file with 2 frames and the proper width and height.
        'The file is initially created as empty and the user must load data to it. 
        Dim roi As RegionOfInterest = New RegionOfInterest(0, 0, w1(0), h1(0), 1, 1)
        Dim rois As RegionOfInterest() = {roi}
        Dim TwoFrameOneRoi As IImageDataSet = filemgr.CreateFile(path + "\\TwoFrameOneRoi.spe", rois, 2, ImageDataFormat.MonochromeUnsigned16)
        'Put data to frame 1
        Dim data1 As IImageData = TwoFrameOneRoi.GetFrame(0, 0)
        data1.SetData(frame1)
        'Put data to frame 2
        Dim data2 As IImageData = TwoFrameOneRoi.GetFrame(0, 1)
        data2.SetData(frame2)
        'Finally close this file
        filemgr.CloseFile(TwoFrameOneRoi)

        'Part 2: one frame two regions
        Dim w2 As Integer() = {300, 500}
        Dim h2 As Integer() = {400, 600}
        Dim frame1_roi1(300 * 400) As UShort
        For pix As Integer = 0 To 300 * 400 - 1
            frame1_roi1(pix) = pix Mod 65536
        Next
        Dim frame1_roi2(500 * 600) As UShort
        For pix As Integer = 0 To 500 * 600 - 1
            frame1_roi2(pix) = pix Mod 65536
        Next
        'Create a file, get the buffer and fill it in for each region.
        'The file is initially created as empty and the user must load data to it. 
        'The regions can not overlap
        Dim r1 As RegionOfInterest = New RegionOfInterest(0, 0, w2(0), h2(0), 1, 1)
        Dim r2 As RegionOfInterest = New RegionOfInterest(w2(0) + 1, h2(0) + 1, w2(1), h2(1), 1, 1)
        Dim rois2 As RegionOfInterest() = {r1, r2}
        Dim OneFrameTwoRoi As IImageDataSet = filemgr.CreateFile(path + "\\OneFrameTwoRoi.spe", rois2, 1, ImageDataFormat.MonochromeUnsigned16)
        'Put data to region 1
        Dim data2_roi1 As IImageData = OneFrameTwoRoi.GetFrame(0, 0)
        data2_roi1.SetData(frame1_roi1)
        'Put data to region 2
        Dim data2_roi2 As IImageData = OneFrameTwoRoi.GetFrame(1, 0)
        data2_roi2.SetData(frame1_roi2)
        'Finally close this file
        filemgr.CloseFile(OneFrameTwoRoi)
    End Sub

End Class