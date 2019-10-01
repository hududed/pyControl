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
Imports System.Drawing
Imports System.Reflection
Imports PrincetonInstruments.LightField.AddIns

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Generate data in memory and plots to Data view.   ''''''''''
'''''''''' Also show putting more than one source on a view. ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class PlotSample
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
        toolBarState_ = Nothing
    End Sub

    Public Sub Deactivate()
    End Sub

    Public Overrides Sub UIApplicationToolBarExecute()
        PlotSinAndCos()
    End Sub

    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            toolBarState_ = value
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Generate Cos & Sin Curves and display results in four windows to demonstrate making data in memory and plotting graphs"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Plot Sample"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarHelpTopicID As Nullable(Of Integer)
        Get
            Return 1
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarBitmap As Drawing.Bitmap
        Get
            Dim img As Drawing.Image = My.Resources.PlotSample
            Dim image As Bitmap = New Bitmap(img)
            Return image
        End Get
    End Property

    'Show four Plots of Cos vs Sine in Quad Display
    '1. Generate Raw Data.
    '2. Build IImageData(s) with the raw data from the DataManager. 
    '3. Get four displays and puts two waveforms in each display.        
    Private Sub PlotSinAndCos()
        'Generate curves (angle=-2*PI~2*PI, amplitude=0~200)
        Dim cosine(720) As UShort
        Dim sine(720) As UShort
        For pix As Integer = 0 To 719
            'Convert to angle
            Dim angle As Double = Math.PI * (pix - 360) / 180.0
            'Compute points
            cosine(pix) = 100.0 * (Math.Cos(angle) + 1.0)
            sine(pix) = 100.0 * (Math.Sin(angle) + 1.0)
        Next
        'Get the data manager
        Dim datamgr As IDataManager = LightFieldApplication.DataManager
        If datamgr IsNot Nothing Then
            Dim roi As RegionOfInterest = New RegionOfInterest(0, 0, 720, 1, 1, 1)
            'Create blobs
            Dim cosData As IImageDataSet = datamgr.CreateImageDataSet(cosine, roi, ImageDataFormat.MonochromeUnsigned16)
            Dim sineData As IImageDataSet = datamgr.CreateImageDataSet(sine, roi, ImageDataFormat.MonochromeUnsigned16)
            'Get the Display object
            Dim display As IDisplay = LightFieldApplication.DisplayManager
            If display IsNot Nothing Then
                'Select data file compare mode and four even windows
                display.ShowDisplay(DisplayLocation.ExperimentWorkspace, DisplayLayout.FourEven)
                Dim view As IDisplayViewer = Nothing
                'Put the data in all 4 windows
                For i As Integer = 0 To 3
                    view = display.GetDisplay(DisplayLocation.ExperimentWorkspace, i)
                    view.Display("Cosine", cosData)
                    Dim sinSource As IDisplaySource = display.Create("Sine", sineData)
                    view.Add(sinSource)
                Next
            End If
        End If
    End Sub

End Class