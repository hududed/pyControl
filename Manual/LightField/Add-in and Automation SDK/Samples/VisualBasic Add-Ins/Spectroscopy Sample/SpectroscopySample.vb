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
Imports System.Xml
Imports System.Xml.XPath
Imports System.Xml.Linq
Imports PrincetonInstruments.LightField.AddIns

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' Demonstrate how to read the existing calibration data from an existing SPE file ''''''''''
'''''''''' as well as how to create and display your own calibrated data file.             ''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class SpectroscopySample
    Inherits AddInBase
    
    Private toolBarState_ As Boolean?
    'EventHandler<ExperimentCompletedEventArgs> acquireCompletedEventHandler_

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
        Dim experiment As IExperiment = LightFieldApplication.Experiment
        If experiment.IsReadyToRun Then
            'Acquire image with calibration
            AddHandler experiment.ExperimentCompleted, AddressOf experiment_ExperimentCompleted
            experiment.Acquire()
        End If
    End Sub

    Public Overrides Property UIApplicationToolBarIsChecked As Nullable(Of Boolean)
        Get
            Return toolBarState_
        End Get
        Set(ByVal value As Nullable(Of Boolean))
            toolBarState_ = value
        End Set
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarTitle As String
        Get
            Return "Spectroscopy Sample"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarToolTip As String
        Get
            Return "Get/Set the calibration data on a file to show an example of how to work with wavelength calibrated data"
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarIsEnabled As Boolean
        Get
            Return True
        End Get
    End Property

    Public Overrides ReadOnly Property UIApplicationToolBarHelpTopicID As Nullable(Of Integer)
        Get
            Return 1
        End Get
    End Property

    'Event handler for Acquire Completed        
    Private Sub experiment_ExperimentCompleted(sender As Object, e As ExperimentCompletedEventArgs)
        'Remove event handler
        RemoveHandler CType(sender, IExperiment).ExperimentCompleted, AddressOf experiment_ExperimentCompleted
        'Create a calibrated SPE file
        Dim fileManager As IFileManager = LightFieldApplication.FileManager
        If fileManager IsNot Nothing Then
            'Find the image 
            Dim files As IList(Of String) = fileManager.GetRecentlyAcquiredFileNames() 'Get the recently acquired file list        
            If files.Count <> 0 Then
                Dim waveLengths() As Double = Nothing
                Dim errors() As Double = Nothing
                'Get the xml out of the image and from that pull the calibration/error 
                Dim dataSet As IImageDataSet = fileManager.OpenFile(files(0), System.IO.FileAccess.Read) 'Get the image dataset
                GetCalibrationAndError(dataSet, waveLengths, errors)
                'Create a new file of user data
                CreateCalibratedFile(waveLengths, errors)
            End If
        End If
    End Sub

    Private Sub GetCalibrationAndError(dataSet As IImageDataSet, ByRef waveLengths As Double(), ByRef errors As Double())
        'Start off empty
        errors = Nothing
        waveLengths = Nothing
        'Create a new XML Document
        Dim xDoc As XmlDocument = New XmlDocument()
        Dim xmlText As String = LightFieldApplication.FileManager.GetXml(dataSet)
        'Convert to proper encoding buffer
        Dim byteArray(xmlText.Length) As Byte
        Dim encoding As Object = System.Text.Encoding.UTF8
        byteArray = encoding.GetBytes(xmlText)
        'Convert to MemoryStream
        Dim memoryStream As MemoryStream = New MemoryStream(byteArray)
        memoryStream.Seek(0, SeekOrigin.Begin)
        'Load the XmlDocument
        xDoc.Load(memoryStream)
        'Create an XmlNamespaceManager to resolve the default namespace.
        Dim nsmgr As New XmlNamespaceManager(xDoc.NameTable)
        nsmgr.AddNamespace("pi", "http://www.princetoninstruments.com/spe/2009")
        'Find calibrations
        Dim calRoot As XmlNode = xDoc.SelectSingleNode("//pi:Calibrations", nsmgr)
        If calRoot IsNot Nothing Then
            'Get WavelengthMapping
            Dim waveMapping As XmlNode = calRoot.SelectSingleNode("//pi:WavelengthMapping", nsmgr)
            If waveMapping IsNot Nothing Then
                'Get Wavelength errors (wave0,error0 wave1,error1 wave2,error2 ....)
                Dim waveErrors As XmlNode = waveMapping.SelectSingleNode("//pi:WavelengthError", nsmgr)
                If waveErrors IsNot Nothing Then
                    Dim pairs As String() = waveErrors.InnerText.Split(" ")
                    If (pairs IsNot Nothing) AndAlso (pairs.Count() > 0) Then
                        ReDim waveLengths(pairs.Count())
                        ReDim errors(pairs.Count())
                        For i As Integer = 0 To pairs.Count() - 1
                            Dim temp As String() = pairs(i).Split(",")
                            waveLengths(i) = XmlConvert.ToDouble(temp(0))
                            errors(i) = XmlConvert.ToDouble(temp(1))
                        Next
                    End If
                Else 'No errors
                    Dim waves As XmlNode = waveMapping.SelectSingleNode("//pi:Wavelength", nsmgr)
                    If waves IsNot Nothing Then
                        'Readin values into array
                        Dim split As String() = waves.InnerText.Split(",")
                        ReDim waveLengths(split.Length)
                        'Convert to doubles
                        For i As Integer = 0 To split.Length - 1
                            waveLengths(i) = XmlConvert.ToDouble(split(i))
                        Next
                    End If
                End If
            End If
        End If
    End Sub

    Private Sub CreateCalibratedFile(calibration As Double(), errors As Double())
        'No calibration so make something up
        If calibration Is Nothing Then
            ReDim calibration(719)
            For i As Integer = 0 To 719
                calibration(i) = i * 3.0
            Next
        End If
        'Generate curves
        Dim cosine(calibration.Length - 1) As UShort
        Dim pix As Integer
        For pix = 0 To calibration.Length - 1
            Dim angle As Double = Math.PI * (pix - 360.0) / 180.0 'Convert to angle
            cosine(pix) = 100.0 * (Math.Cos(angle) + 1) 'Compute points
        Next
        'Make a region of interest (Single Strip)
        Dim roi As RegionOfInterest = New RegionOfInterest(0, 0, calibration.Length, 1, 1, 1)
        'Get the file manager
        Dim filemgr As IFileManager = LightFieldApplication.FileManager
        If filemgr IsNot Nothing Then
            Dim rois As RegionOfInterest() = {roi}
            Dim root As String = LightFieldApplication.Experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
            Dim calSampleData As IImageDataSet = filemgr.CreateFile(root + "\\CalibrationSample.Spe", rois, 1, ImageDataFormat.MonochromeUnsigned16)
            'Put data to frame 1
            Dim data1 As IImageData = calSampleData.GetFrame(0, 0)
            data1.SetData(cosine)
            'Update the XML for the new document
            SetCalibrationAndError(calSampleData, calibration, errors)
            'Close the file
            filemgr.CloseFile(calSampleData)
        End If
    End Sub

    Private Sub SetCalibrationAndError(dataSet As IImageDataSet, waveLengths As Double(), errors As Double())
        'Get the text file
        Dim xmlText As String = LightFieldApplication.FileManager.GetXml(dataSet)
        'Create a new XML document
        Dim xDoc As New XmlDocument
        'Convert to proper encoding buffer
        Dim byteArray(xmlText.Length) As Byte
        Dim encoding As Object = System.Text.Encoding.UTF8
        byteArray = encoding.GetBytes(xmlText)
        'Convert to memory stream
        Dim memoryStream As MemoryStream = New MemoryStream(byteArray)
        memoryStream.Seek(0, SeekOrigin.Begin)
        'Load The XmlDocument
        xDoc.Load(memoryStream)
        'Create an XmlNamespaceManager to resolve the default namespace.
        Dim nsmgr As New XmlNamespaceManager(xDoc.NameTable)
        nsmgr.AddNamespace("pi", "http://www.princetoninstruments.com/spe/2009")
        'Find calibrations
        Dim calRoot As XmlNode = xDoc.SelectSingleNode("//pi:Calibrations", nsmgr)
        If calRoot IsNot Nothing Then
            'Get WavelengthMapping
            Dim waveMapping As XmlNode = calRoot.SelectSingleNode("//pi:WavelengthMapping", nsmgr)
            'Create if it is non existing
            If waveMapping Is Nothing Then
                waveMapping = xDoc.CreateNode(XmlNodeType.Element, "WavelengthMapping", "http://www.princetoninstruments.com/spe/2009")
                calRoot.AppendChild(waveMapping)
            End If
            If waveMapping IsNot Nothing Then
                'Set Wavelength errors (wave0,error0 wave1,error1 wave2,error2 ....)
                If errors IsNot Nothing Then
                    'Get Wavelength errors
                    Dim waveErrors As XmlNode = waveMapping.SelectSingleNode("//pi:WavelengthError", nsmgr)
                    'Create if it is non existing and needed
                    If waveErrors Is Nothing Then
                        waveErrors = xDoc.CreateNode(XmlNodeType.Element, "WavelengthError", "http://www.princetoninstruments.com/spe/2009")
                        waveMapping.AppendChild(waveErrors)
                    End If
                    If waveErrors IsNot Nothing Then
                        Dim errorString As String = String.Empty
                        For i As Integer = 0 To errors.Length - 1
                            errorString += waveLengths(i).ToString() + "," + errors(i).ToString()
                            'Space for next pair if not last one
                            If i <> errors.Length - 1 Then
                                errorString += " "
                            End If
                        Next
                        waveErrors.InnerText = errorString
                    End If
                Else
                    Dim waves As XmlNode = waveMapping.SelectSingleNode("//pi:Wavelength", nsmgr)
                    'Create if it is not existing
                    If waves Is Nothing Then
                        waves = xDoc.CreateNode(XmlNodeType.Element, "Wavelength", "http://www.princetoninstruments.com/spe/2009")
                        waveMapping.AppendChild(waves)
                    End If
                    If waves IsNot Nothing Then
                        Dim waveString As String = String.Empty
                        For i As Integer = 0 To waveLengths.Length - 1
                            waveString += waveLengths(i).ToString()
                            If i <> waveLengths.Length - 1 Then
                                waveString += ","
                            End If

                        Next
                        waves.InnerText = waveString
                    End If
                End If
            End If
        End If
        'Update the document with the new xml
        LightFieldApplication.FileManager.SetXml(dataSet, xDoc.InnerXml)
    End Sub

End Class