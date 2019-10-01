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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''' This sample hooks into the data stream when data is being acquired or displayed,               ''''''''''
'''''''''' and modifies the data by performing a sobel edge detection on the buffer(s).                   ''''''''''
'''''''''' This is a menu driven addin and sets up a check box menu item as its source of control.        ''''''''''
'''''''''' Notes: It will only sobel transform the first region of interest.                              ''''''''''
''''''''''        It must be connected before acquiring or focusing.                                      ''''''''''
''''''''''        Turning it on after the acquisition is started will do nothing.                         ''''''''''
'''''''''' This sample shows how to inject your code into the LightField data stream and modify the data. ''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Public Class OnlineSobelSample
    Inherits AddInBase

    Private menuEnabled_ As Boolean
    Private processEnabled_ As Boolean?
    Private sobelTransformer_ As RemotingSobelTransformation
    Private experiment_ As IExperiment

    Public ReadOnly Property UISupport As UISupport
        Get
            Return UISupport.Menu
        End Get
    End Property

    Public Sub Activate(ByVal app As ILightFieldApplication)
        LightFieldApplication = app 'Capture interface
        experiment_ = app.Experiment
        menuEnabled_ = CheckSystem()
        processEnabled_ = False

        If (menuEnabled_) Then
            CreateTransformationObject()
        End If

        'Listen to region of interest result changed and re-compute the buffers to match the region
        Dim settings As New List(Of String)
        settings.Add(CameraSettings.ReadoutControlRegionsOfInterestResult)
        experiment_.FilterSettingChanged(settings)
        AddHandler experiment_.SettingChanged, AddressOf experiment__SettingChanged
        'Connect to experiment device changed event
        'When camera is added, this add-in is active. If a camera is removed then this add-in is disabled.
        AddHandler experiment_.ExperimentUpdated, AddressOf experiment__ExperimentUpdated
        'Connect to the data received event
        AddHandler experiment_.ImageDataSetReceived, AddressOf experimentDataReady
    End Sub

    Public Sub Deactivate()
        'Stop listening to device changes
        RemoveHandler experiment_.ExperimentUpdated, AddressOf experiment__ExperimentUpdated
        'Stop snooping settings
        experiment_.FilterSettingChanged(New List(Of String)())
        RemoveHandler experiment_.SettingChanged, AddressOf experiment__SettingChanged
        'Disconnect data received event            
        RemoveHandler experiment_.ImageDataSetReceived, AddressOf experimentDataReady
    End Sub

    Public Shadows ReadOnly Property UIMenuISEnabled As Boolean
        Get
            Return menuEnabled_
        End Get
    End Property

    Public Overrides ReadOnly Property UIMenuTitle As String
        Get
            Return "Online Sobel Sample"
        End Get
    End Property

    Public Overrides Property UIMenuIsChecked As Nullable(Of Boolean)
        Get
            Return processEnabled_
        End Get
        Set(value As Nullable(Of Boolean))
            processEnabled_ = value
        End Set
    End Property

    Private Function CheckSystem() As Boolean
        For Each device As IDevice In LightFieldApplication.Experiment.ExperimentDevices
            If device.Type = DeviceType.Camera Then
                Return True
            End If
        Next
        'No camera return false
        Return False
    End Function

    Private Sub experiment__ExperimentUpdated(sender As Object, e As ExperimentUpdatedEventArgs)
        Dim hasCamera As Boolean = CheckSystem()
        'Update on change only
        If menuEnabled_ <> hasCamera Then
            menuEnabled_ = hasCamera
            RequestUIRefresh(UISupport.Menu)
        End If
        'Building a system can change the sensor dimensions 
        If hasCamera Then
            CreateTransformationObject()
        End If
    End Sub
    Private Sub CreateTransformationObject()
        'Initialize online process and create transformation class if the system is ready
        Dim rois As RegionOfInterest() = experiment_.SelectedRegions
        sobelTransformer_ = New RemotingSobelTransformation(rois)
    End Sub

    Private Sub experiment__SettingChanged(sender As Object, e As SettingChangedEventArgs)
        If CheckSystem() Then
            CreateTransformationObject()
        End If
    End Sub

    'With all of the data in the block, transform it all        
    Public Sub experimentDataReady(sender As Object, e As ImageDataSetReceivedEventArgs)
        If processEnabled_ = False Then 'Do nothing
            Exit Sub
        End If
        'Transform all frames in the package           
        For i As Integer = 0 To e.ImageDataSet.Frames - 1
            For roi As Integer = 0 To e.ImageDataSet.Regions.Length - 1
                sobelTransformer_.Transform(e.ImageDataSet.GetFrame(roi, i), roi)
            Next
        Next
    End Sub
End Class

'Perform a Sobel transformation on all regions of interest. 
Public Class RemotingSobelTransformation
    Shared indexBuffers_ As Integer()(,,)
    Shared retDataUs_ As UShort()()
    Shared retDataI_ As Integer()()
    Shared retDataF_ As Single()()

    'Matrices
    Private gy_ As Double() = {-1, -2, -1, 0, 0, 0, 1, 2, 1}
    Private gx_ As Double() = {-1, 0, 1, -2, 0, 2, -1, 0, 1}
    Private xs As Integer() = {-1, 0, 1, -1, 0, 1, -1, 0, 1}
    Private ys As Integer() = {-1, -1, -1, 0, 0, 0, 1, 1, 1}

    'Build buffers of indexes on construction for speed
    Public Sub New(rois As RegionOfInterest())
        'Allocate outer buffers
        indexBuffers_ = New Integer(rois.Length - 1)(,,) {}
        retDataUs_ = New UShort(rois.Length - 1)() {}
        retDataI_ = New Integer(rois.Length - 1)() {}
        retDataF_ = New Single(rois.Length - 1)() {}

        For roiIndex As Integer = 0 To rois.Length - 1
            Dim dW As Integer = rois(roiIndex).Width / rois(roiIndex).XBinning
            Dim dH As Integer = rois(roiIndex).Height / rois(roiIndex).YBinning
            'Static computed once upon starting or roi changing
            'Compute all of the indexes ahead of time, this makes the code to do the process faster.
            If (indexBuffers_(roiIndex) Is Nothing) OrElse (indexBuffers_(roiIndex).Length <> dW * dH * 9) Then
                indexBuffers_(roiIndex) = New Integer(dW - 1, dH - 1, 8) {}
                For xx As Integer = 2 To dW - 3
                    For yy As Integer = 2 To dH - 3
                        For i As Integer = 0 To 8
                            Dim index As Integer = (xx + xs(i)) + (yy + ys(i)) * dW
                            indexBuffers_(roiIndex)(xx, yy, i) = index
                        Next
                    Next
                Next

            End If

            'Output data buffers
            ReDim retDataUs_(roiIndex)(dW * dH)
            ReDim retDataI_(roiIndex)(dW * dH)
            ReDim retDataF_(roiIndex)(dW * dH)
        Next
    End Sub

    'Perform the actual transformation
    Public Sub Transform(data As IImageData, roi As Integer)
        'Hint use locals (accessing on Interface forces boundary crossing) that will be unbearably slow.
        Dim dW As Integer = data.Width 'Boundary crossing
        Dim dH As Integer = data.Height 'Boundary crossing

        Select (data.Format)
            Case ImageDataFormat.MonochromeUnsigned16
                Dim ptr As UShort() = data.GetData()     'Input data
                'Loop Width & Height (Quick and Dirty Padding Of 2)
                'This Avoids alot of boundary checking and increases speed
                For xx As Integer = 2 To dW - 3
                    For yy As Integer = 2 To dH - 3
                        Dim GY As Double = 0
                        Dim GX As Double = 0
                        'Compute the X and Y components
                        For i As Integer = 0 To 8
                            Dim idx As Integer = indexBuffers_(roi)(xx, yy, i)
                            GY += ptr(idx) * gy_(i)
                            GX += ptr(idx) * gx_(i)
                        Next
                        'Magnitude
                        Dim G As Double = Math.Sqrt(GX * GX + GY * GY)
                        'Put the Magnitude into the output buffer
                        retDataUs_(roi)(yy * dW + xx) = G
                    Next
                Next
                'Write the output buffer to the IImageData Boundary Crossing
                data.SetData(retDataUs_(roi))

            Case ImageDataFormat.MonochromeUnsigned32
                Dim ptr As Integer() = data.GetData()     'Input data
                'Loop Width & Height (Quick and Dirty Padding Of 2)
                'This Avoids alot of boundary checking and increases speed
                For xx As Integer = 2 To dW - 3
                    For yy As Integer = 2 To dH - 3
                        Dim GY As Double = 0
                        Dim GX As Double = 0
                        'Compute the X and Y components
                        For i As Integer = 0 To 8
                            Dim idx As Integer = indexBuffers_(roi)(xx, yy, i)
                            GY += ptr(idx) * gy_(i)
                            GX += ptr(idx) * gx_(i)
                        Next
                        'Magnitude
                        Dim G As Double = Math.Sqrt(GX * GX + GY * GY)
                        'Put the Magnitude into the output buffer
                        retDataI_(roi)(yy * dW + xx) = G
                    Next
                Next
                'Write the output buffer to the IImageData Boundary Crossing
                data.SetData(retDataI_(roi))

            Case ImageDataFormat.MonochromeFloating32
                Dim ptr As Single() = data.GetData()     'Input data
                'Loop Width & Height (Quick and Dirty Padding Of 2)
                'This Avoids alot of boundary checking and increases speed
                For xx As Integer = 2 To dW - 3
                    For yy As Integer = 2 To dH - 3
                        Dim GY As Double = 0
                        Dim GX As Double = 0
                        'Compute the X and Y components
                        For i As Integer = 0 To 8
                            Dim idx As Integer = indexBuffers_(roi)(xx, yy, i)
                            GY += ptr(idx) * gy_(i)
                            GX += ptr(idx) * gx_(i)
                        Next
                        'Magnitude
                        Dim G As Double = Math.Sqrt(GX * GX + GY * GY)
                        'Put the Magnitude into the output buffer
                        retDataF_(roi)(yy * dW + xx) = G
                    Next
                Next
                'Write the output buffer to the IImageData Boundary Crossing
                data.SetData(retDataF_(roi))
        End Select
    End Sub
End Class