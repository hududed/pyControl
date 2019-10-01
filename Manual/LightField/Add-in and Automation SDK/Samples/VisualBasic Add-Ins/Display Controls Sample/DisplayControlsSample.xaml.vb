Imports System
Imports System.Collections
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
Imports System.Diagnostics
Imports System.Reflection
Imports System.Text.RegularExpressions
Imports System.IO
Imports System.Windows.Markup
Imports System.Threading
Imports PrincetonInstruments.LightField.AddIns

Public Enum GraphSources
    Source1
    Source2
    Source3
    Source4
    Source5
End Enum

'Interaction logic for DisplayControlsSample.xaml
Public Class DisplayControlsSample
    Private application_ As ILightFieldApplication
    Private controls_ As List(Of ControlWidget)
    Private currentViewer_ As IDisplayViewer
    Private display_ As IDisplay
    Private selectedLocation_ As DisplayLocation
    Private selectedIndex_ As Integer
    Private selectedLayout_ As DisplayLayout

     'Constructor
    Public Sub New(app As ILightFieldApplication)
        'Cache some members
        application_ = app
        display_ = application_.DisplayManager
        'Initialize the WPF component
        InitializeComponent()
        
        'Setup layout mode combo box
        LayoutCombo.Items.Add(DisplayLayout.One)
        LayoutCombo.Items.Add(DisplayLayout.TwoHorizontal)
        LayoutCombo.Items.Add(DisplayLayout.TwoVertical)
        LayoutCombo.Items.Add(DisplayLayout.ThreeTopFavored)
        LayoutCombo.Items.Add(DisplayLayout.ThreeVertical)
        LayoutCombo.Items.Add(DisplayLayout.FourEven)
        LayoutCombo.Items.Add(DisplayLayout.FourTopFavored)
        LayoutCombo.Items.Add(DisplayLayout.FourVertical)
        LayoutCombo.Items.Add(DisplayLayout.FourLeftFavored)
        LayoutCombo.Items.Add(DisplayLayout.FiveTopFavored)
        LayoutCombo.Items.Add(DisplayLayout.FiveLeftFavored)

        'Defaults from application
        selectedLocation_ = display_.Location
        selectedLayout_ = display_.ExperimentWorkspaceLayout

        'Default combo boxes
        LayoutCombo.SelectedItem = selectedLayout_

        'Experiment
        If (selectedLocation_ = DisplayLocation.ExperimentWorkspace) Then
            LocationCombo.SelectedIndex = 0
        Else 'Data Workspace
            LocationCombo.SelectedIndex = 1
        End If

        IndexCombo.SelectedIndex = 0

    End Sub

    'Loaded 
    Private Sub Window_Loaded(sender As System.Object, e As System.Windows.RoutedEventArgs)
    End Sub

    Private Sub IndexCombo_SelectionChanged(sender As System.Object, e As System.Windows.Controls.SelectionChangedEventArgs)
        selectedIndex_ = IndexCombo.SelectedIndex
        'Display test code            
        If display_ IsNot Nothing Then
            If selectedLayout_ <> DisplayLayout.UninitializedEnum Then
                'Get the views
                Dim view1_ As IDisplayViewer = display_.GetDisplay(selectedLocation_, selectedIndex_)

                If (view1_.DisplaySources.Count > 0) Then
                    BuildDisplayControls(view1_)
                End If
            End If
        End If
    End Sub

    Private Sub LocationCombo_SelectionChanged(sender As System.Object, e As System.Windows.Controls.SelectionChangedEventArgs)
        Select Case LocationCombo.SelectedIndex
            Case 0
                selectedLocation_ = DisplayLocation.ExperimentWorkspace
                LayoutCombo.IsEnabled = True
                AddFileButton.IsEnabled = True
            Case 1            
                selectedLocation_ = DisplayLocation.DataWorkspace
                LayoutCombo.IsEnabled = False
                AddFileButton.IsEnabled = False
        End Select
        'Show this one
        If selectedLayout_ <> DisplayLayout.UninitializedEnum Then
            display_.Location = selectedLocation_
        End If
    End Sub

    Private Sub LayoutCombo_SelectionChanged(sender As System.Object, e As System.Windows.Controls.SelectionChangedEventArgs)
        selectedLayout_ = LayoutCombo.SelectedItem
        'Show this one
        If selectedLocation_ <> DisplayLocation.UninitializedEnum Then
            display_.ExperimentWorkspaceLayout = selectedLayout_
        End If
    End Sub

    Private Sub DisplayButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Display test code            
        If display_ IsNot Nothing Then
            Dim view1_ As Object = display_.GetDisplay(selectedLocation_, selectedIndex_) 'Get the views
            BuildDisplayControls(view1_)
        End If
    End Sub

    Private Sub LoadFileButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim dlg As Microsoft.Win32.OpenFileDialog = New Microsoft.Win32.OpenFileDialog()
        dlg.FileName = "" 'Default file name
        dlg.DefaultExt = ".spe" 'Default file extension
        dlg.Filter = "LightField Data (*.spe)|*.spe" 'Filter files by extension
        'Show open file dialog box
        Dim result As Boolean? = dlg.ShowDialog()
        'Process open file dialog box results
        If result = True Then
            If selectedLocation_ = DisplayLocation.DataWorkspace Then 'Data Workspace
                BuildDisplayControls(display_.DisplayFileInDataWorkspace(dlg.FileName))
            Else 'Data Workspace Comparison or Experiment
                Dim viewer As IDisplayViewer = display_.GetDisplay(selectedLocation_, selectedIndex_)
                viewer.Display(dlg.FileName)
                BuildDisplayControls(viewer)
            End If
        End If
    End Sub
   
    Private Sub AddFileButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Dim dlg As Microsoft.Win32.OpenFileDialog = New Microsoft.Win32.OpenFileDialog()
        dlg.FileName = "" 'Default file name
        dlg.DefaultExt = ".spe" 'Default file extension
        dlg.Filter = "LightField Data (*.spe)|*.spe" 'Filter files by extension
        'Show open file dialog box
        Dim result As Nullable(Of Boolean) = dlg.ShowDialog()
        'Process open file dialog box results
        If result = True Then
            'Should not Data Workspace
            If selectedLocation_ <> DisplayLocation.DataWorkspace Then
                'Get the viewer
                Dim viewer As IDisplayViewer = display_.GetDisplay(selectedLocation_, selectedIndex_)
                'Must be a graph to add source
                viewer.DisplayType = DisplayType.Graph
                'Only support a maximum of 5 sources
                If viewer.DisplaySources.Count < 5 Then
                    'Create the source and add it 
                    Dim source As IDisplaySource = display_.Create(dlg.FileName)
                    viewer.Add(source)
                End If
            End If
        End If
    End Sub

    'Close the window
    Private Sub DoneButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        Close() 'Close the dialog
    End Sub

    'Control builder
    Private Sub BuildDisplayControls(view As IDisplayViewer)
        'Nuke the children
        dockPanel1.Children.Clear()
        'Can't create controls for a view if one does not exist
        If view Is Nothing Then
            Exit Sub
        End If

        'Current viewer is used in the callback handlers for the controls
        currentViewer_ = view
        'Build controls from viable settings
        Dim rootScroller As Windows.Controls.ScrollViewer = New Windows.Controls.ScrollViewer()
        Dim rootStack As Windows.Controls.StackPanel = New Windows.Controls.StackPanel()
        controls_ = New List(Of ControlWidget)()
        'Build controls up and set the current value to match the chosen view(argument)
        'General
        controls_.Add(New ControlWidget("General", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("View Type", ControlWidgetType.ComboBox, view.DisplayType))
        'Zooming
        controls_.Add(New ControlWidget("Zooming", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("Zoom Out", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("Zoom In", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("Zoom", ControlWidgetType.SliderBar, view.Zoom, view.MinimumZoom, view.MaximumZoom))
        controls_.Add(New ControlWidget("ZoomToBestFit", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("ZoomToActualSize", ControlWidgetType.Button, 0))
        'Stamping
        controls_.Add(New ControlWidget("Stamping", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("Exposure Start", ControlWidgetType.CheckBox, view.ShowExposureStartedTimeStamp))
        controls_.Add(New ControlWidget("Exposure End", ControlWidgetType.CheckBox, view.ShowExposureEndedTimeStamp))
        controls_.Add(New ControlWidget("Frame Tracking Number", ControlWidgetType.CheckBox, view.ShowFrameTrackingNumber))
        controls_.Add(New ControlWidget("Absolute Time", ControlWidgetType.CheckBox, view.ShowTimeStampsInAbsoluteTime))
        controls_.Add(New ControlWidget("GateTracking Delay", ControlWidgetType.CheckBox, view.ShowGateTrackingDelay))
        controls_.Add(New ControlWidget("GateTracking Width", ControlWidgetType.CheckBox, view.ShowGateTrackingWidth))
        controls_.Add(New ControlWidget("Phase Modulation", ControlWidgetType.CheckBox, view.ShowModulationTrackingPhase))
        'Regions, frames and rows
        controls_.Add(New ControlWidget("Source,Frames,Regions,Rows", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("CurrentSource", ControlWidgetType.ComboBox, FromSource(view.DisplaySourceIndex)))
        controls_.Add(New ControlWidget("Frame", ControlWidgetType.SliderBar, view.FrameIndex, 0, view.Frames - 1))
        controls_.Add(New ControlWidget("Region", ControlWidgetType.SliderBar, view.RegionIndex, 0, view.Regions - 1))
        controls_.Add(New ControlWidget("Row", ControlWidgetType.SliderBar, view.RowIndex, 0, view.Rows - 1))
        'Playback
        controls_.Add(New ControlWidget("Playback", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("IsPlaybackRunning", ControlWidgetType.CheckBox, view.IsPlaybackRunning))
        controls_.Add(New ControlWidget("RepeatPlayback", ControlWidgetType.CheckBox, view.RepeatPlayback))
        controls_.Add(New ControlWidget("PlaybackFrameRate", ControlWidgetType.EditBox, view.PlaybackFrameRate))
        'Scaling 
        controls_.Add(New ControlWidget("Scaling", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("OptimizeContrast", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("AutoScaleIntensity", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("AlwaysAutoScaleIntensity", ControlWidgetType.CheckBox, view.AlwaysAutoScaleIntensity))
        controls_.Add(New ControlWidget("BlackLevel", ControlWidgetType.EditBox, 0))
        controls_.Add(New ControlWidget("WhiteLevel", ControlWidgetType.EditBox, 0))
        controls_.Add(New ControlWidget("SetIntensityLevels", ControlWidgetType.Button, 0))
        'Graph controls
        controls_.Add(New ControlWidget("Graph", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("GraphGridLines", ControlWidgetType.ComboBox, view.GraphGridLines))
        controls_.Add(New ControlWidget("PlottingStyle", ControlWidgetType.ComboBox, view.PlottingStyle))
        controls_.Add(New ControlWidget("PeaksIndicated", ControlWidgetType.ComboBox, view.PeaksIndicated))
        controls_.Add(New ControlWidget("PlotsStacked", ControlWidgetType.CheckBox, view.PlotsStacked))
        controls_.Add(New ControlWidget("DataPointsVisible", ControlWidgetType.CheckBox, view.DataPointsVisible))
        controls_.Add(New ControlWidget("GraphZoomMode", ControlWidgetType.ComboBox, view.GraphZoomMode))
        controls_.Add(New ControlWidget("ZoomXAxisToBestFit", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("ZoomYAxisToBestFit", ControlWidgetType.Button, 0))
        'Pseudo color 
        controls_.Add(New ControlWidget("PseudoColor", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("PseudoColorPalette", ControlWidgetType.ComboBox, view.PseudoColorPalette))
        'Cursors (single position)
        Dim x As Integer = 0
        Dim y As Integer = 0
        Dim p As Windows.Point
        If view.CursorPosition IsNot Nothing Then
            p = view.CursorPosition
            x = p.x
            y = p.y
        End If
        'Cursor box
        Dim bx As Integer = 0
        Dim by As Integer = 0
        Dim bw As Integer = 0
        Dim bh As Integer = 0
        If Not view.DataSelection.IsEmpty Then
            Dim rect As Windows.Rect = view.DataSelection
            bx = rect.X
            by = rect.Y
            bw = rect.Width
            bh = rect.Height
            If bx < 0 Then
                bx = 0
            End If
            If by < 0 Then
                by = 0
            End If
            If bw < 0 Then
                bw = 0
            End If
            If bh < 0 Then
                bh = 0
            End If
        End If
        controls_.Add(New ControlWidget("Cursors", ControlWidgetType.Expander, 0))
        controls_.Add(New ControlWidget("CursorStyle", ControlWidgetType.ComboBox, view.CursorStyle))
        controls_.Add(New ControlWidget("CrossSections", ControlWidgetType.ComboBox, view.CrossSections))
        controls_.Add(New ControlWidget("Point X", ControlWidgetType.EditBox, x))
        controls_.Add(New ControlWidget("Point Y", ControlWidgetType.EditBox, y))
        controls_.Add(New ControlWidget("Set Cursor", ControlWidgetType.Button, 0))
        controls_.Add(New ControlWidget("Box X", ControlWidgetType.EditBox, bx))
        controls_.Add(New ControlWidget("Box Y", ControlWidgetType.EditBox, by))
        controls_.Add(New ControlWidget("Box Width", ControlWidgetType.EditBox, bw))
        controls_.Add(New ControlWidget("Box Height", ControlWidgetType.EditBox, bh))
        controls_.Add(New ControlWidget("Set Region", ControlWidgetType.Button, 0))
        'Everything Else
        controls_.Add(New ControlWidget("Miscellaneous", ControlWidgetType.Expander, 0))

        'Start off empty
        Dim expanderStack As System.Collections.Generic.Stack(Of Windows.Controls.Expander) = New System.Collections.Generic.Stack(Of Windows.Controls.Expander)()
        Dim stackPanelStack As System.Collections.Generic.Stack(Of Windows.Controls.StackPanel) = New System.Collections.Generic.Stack(Of Windows.Controls.StackPanel)()
        Dim grid As Windows.Controls.Grid = Nothing
        Dim rowIdx As Integer = 0
        'Create
        For i As Integer = 0 To controls_.Count() - 1
            Select Case controls_(i).GetWidgetType()
                Case ControlWidgetType.Button
                    grid = NewGridNeeded(grid)
                    If grid IsNot Nothing Then
                        grid.RowDefinitions.Add(New Windows.Controls.RowDefinition())
                        Dim btn As Windows.Controls.Button = New Windows.Controls.Button()
                        controls_(i).ControlItem = btn
                        btn.Name = (controls_(i).GetName()).Replace(" ", "_")
                        btn.Content = btn.Name
                        btn.VerticalAlignment = VerticalAlignment.Center
                        btn.Margin = New Windows.Thickness(2, 2, 2, 2)
                        grid.Children.Add(btn)
                        Windows.Controls.Grid.SetRow(btn, rowIdx)
                        Windows.Controls.Grid.SetColumn(btn, 1)
                        'Text block is common
                        Dim tb As Windows.Controls.TextBlock = New Windows.Controls.TextBlock()
                        tb.Text = btn.Name
                        tb.TextWrapping = Windows.TextWrapping.Wrap
                        grid.Children.Add(tb)
                        Windows.Controls.Grid.SetRow(tb, rowIdx)
                        Windows.Controls.Grid.SetColumn(tb, 0)
                        'Event
                        AddHandler btn.Click, AddressOf btn_Click
                        rowIdx += 1
                    End If
                Case ControlWidgetType.CheckBox
                    grid = NewGridNeeded(grid)
                    If grid IsNot Nothing Then
                        grid.RowDefinitions.Add(New Windows.Controls.RowDefinition())
                        Dim cb As Windows.Controls.CheckBox = New Windows.Controls.CheckBox()
                        controls_(i).ControlItem = cb
                        cb.Margin = New Windows.Thickness(2, 2, 2, 2)
                        cb.IsChecked = controls_(i).GetValue()
                        cb.HorizontalAlignment = Windows.HorizontalAlignment.Center
                        cb.VerticalAlignment = Windows.VerticalAlignment.Center
                        cb.Name = (controls_(i).GetName()).Replace(" ", "_")
                        grid.Children.Add(cb)
                        Windows.Controls.Grid.SetRow(cb, rowIdx)
                        Windows.Controls.Grid.SetColumn(cb, 1)
                        AddHandler cb.Click, AddressOf cb_Click 'Event
                        'Text(Block Is Common)
                        Dim tb As Windows.Controls.TextBlock = New Windows.Controls.TextBlock()
                        tb.Text = cb.Name
                        tb.TextWrapping = Windows.TextWrapping.Wrap
                        grid.Children.Add(tb)
                        Windows.Controls.Grid.SetRow(tb, rowIdx)
                        Windows.Controls.Grid.SetColumn(tb, 0)
                        rowIdx += 1
                    End If
                Case ControlWidgetType.ComboBox
                    grid = NewGridNeeded(grid)
                    If grid IsNot Nothing Then
                        grid.RowDefinitions.Add(New Windows.Controls.RowDefinition())
                        Dim cb As Windows.Controls.ComboBox = New Windows.Controls.ComboBox()
                        controls_(i).ControlItem = cb
                        cb.VerticalAlignment = Windows.VerticalAlignment.Center
                        cb.Margin = New Windows.Thickness(2, 2, 2, 2)
                        cb.Name = (controls_(i).GetName()).Replace(" ", "_")
                        grid.Children.Add(cb)
                        Windows.Controls.Grid.SetRow(cb, rowIdx)
                        Windows.Controls.Grid.SetColumn(cb, 1)
                        'Using reflection add all of the enums
                        Dim enumStrings As String() = System.Enum.GetNames(controls_(i).GetValue().GetType())
                        For Each s As String In enumStrings
                            If s <> "UninitializedEnum" Then
                                cb.Items.Add(s)
                            End If
                        Next
                        cb.SelectedItem = controls_(i).GetValue().ToString()
                        AddHandler cb.SelectionChanged, AddressOf cb_SelectionChanged
                        'Text block is common
                        Dim tb As Windows.Controls.TextBlock = New Windows.Controls.TextBlock()
                        tb.Text = cb.Name
                        tb.TextWrapping = Windows.TextWrapping.Wrap
                        grid.Children.Add(tb)
                        Windows.Controls.Grid.SetRow(tb, rowIdx)
                        Windows.Controls.Grid.SetColumn(tb, 0)
                        rowIdx += 1
                    End If
                Case ControlWidgetType.EditBox
                    grid = NewGridNeeded(grid)
                    If grid IsNot Nothing Then
                        grid.RowDefinitions.Add(New Windows.Controls.RowDefinition())
                        Dim cb As Windows.Controls.TextBox = New Windows.Controls.TextBox()
                        controls_(i).ControlItem = cb
                        cb.Margin = New Windows.Thickness(2, 2, 2, 2)
                        cb.Text = (controls_(i).GetValue()).ToString()
                        cb.TextAlignment = Windows.TextAlignment.Right
                        cb.VerticalAlignment = Windows.VerticalAlignment.Center
                        cb.Height = 25
                        grid.Children.Add(cb)
                        Windows.Controls.Grid.SetRow(cb, rowIdx)
                        Windows.Controls.Grid.SetColumn(cb, 1)
                        AddHandler cb.LostFocus, AddressOf cb_LostFocus
                        cb.Name = (controls_(i).GetName()).Replace(" ", "_")
                        'Text Block is common
                        Dim tb As Windows.Controls.TextBlock = New Windows.Controls.TextBlock()
                        tb.Text = cb.Name
                        tb.TextWrapping = Windows.TextWrapping.Wrap
                        grid.Children.Add(tb)
                        Windows.Controls.Grid.SetRow(tb, rowIdx)
                        Windows.Controls.Grid.SetColumn(tb, 0)
                        rowIdx += 1
                    End If
                Case ControlWidgetType.Expander
                    'Pop and link
                    If stackPanelStack.Count() > 0 And expanderStack.Count() > 0 Then
                        Dim expander As Windows.Controls.Expander = expanderStack.Pop()
                        Dim stackpanel As Windows.Controls.StackPanel = stackPanelStack.Pop()
                        expander.Content = grid
                        'If Zero its added already
                        If stackPanelStack.Count() <> 0 Then
                            stackpanel.Children.Add(expander)
                        End If
                        'The grid is done
                        grid = Nothing
                    End If
                    Dim sp As Object = New Windows.Controls.StackPanel()
                    Dim xp As Object = New Windows.Controls.Expander()
                    stackPanelStack.Push(sp)
                    expanderStack.Push(xp)
                    xp.Header = controls_(i).GetName()
                    xp.BorderThickness = New Windows.Thickness(1)
                    xp.BorderBrush = Brushes.Black
                    xp.FlowDirection = Windows.FlowDirection.LeftToRight
                    'Add to root
                    If stackPanelStack.Count = 1 Then
                        rootStack.Children.Add(xp)
                    End If
                    'Reset control count for grid
                    rowIdx = 0
                Case ControlWidgetType.ReadOnlyEditBox
                    Exit Select
                Case ControlWidgetType.SliderBar
                    grid = NewGridNeeded(grid)
                    If grid IsNot Nothing Then
                        grid.RowDefinitions.Add(New Windows.Controls.RowDefinition())
                        Dim sld As Windows.Controls.Slider = New Windows.Controls.Slider()
                        sld.Margin = New Windows.Thickness(2, 2, 2, 2)
                        controls_(i).ControlItem = sld
                        sld.Name = (controls_(i).GetName()).Replace(" ", "_")
                        sld.VerticalAlignment = Windows.VerticalAlignment.Center
                        grid.Children.Add(sld)
                        Windows.Controls.Grid.SetRow(sld, rowIdx)
                        Windows.Controls.Grid.SetColumn(sld, 1)
                        sld.Minimum = controls_(i).SliderMin()
                        sld.Maximum = controls_(i).SliderMax()
                        If sld.Maximum = sld.Minimum Then
                            sld.IsEnabled = False
                        End If
                        sld.Value = Convert.ToDouble(controls_(i).GetValue())
                        AddHandler sld.ValueChanged, AddressOf sld_ValueChanged
                        'Text block is common
                        Dim tb As Windows.Controls.TextBlock = New Windows.Controls.TextBlock()
                        tb.Text = sld.Name
                        tb.TextWrapping = Windows.TextWrapping.Wrap
                        grid.Children.Add(tb)
                        Windows.Controls.Grid.SetRow(tb, rowIdx)
                        Windows.Controls.Grid.SetColumn(tb, 0)
                        rowIdx += 1
                    End If
                Case ControlWidgetType.SubEnd
                    'Pop and link
                    If stackPanelStack.Count() > 0 And expanderStack.Count() > 0 Then
                        Dim expander As Windows.Controls.Expander = expanderStack.Pop()
                        Dim stackpanel As Windows.Controls.StackPanel = stackPanelStack.Pop()
                        expander.Content = grid
                        'If Zero its added already
                        If stackPanelStack.Count() <> 0 Then
                            stackpanel.Children.Add(expander)
                        End If
                        'The grid is done
                        grid = Nothing
                    End If
                Case ControlWidgetType.SubExpander
                    'Reset control count for grid
                    rowIdx = 0
                    Dim sp As Object = New Windows.Controls.StackPanel()
                    Dim xp As Object = New Windows.Controls.Expander()
                    stackPanelStack.Push(sp)
                    expanderStack.Push(xp)

                    xp.Header = controls_(i).GetName()
                    sp.Children.Add(xp)
                    sp.Background = Brushes.Beige

                    xp.BorderThickness = New Windows.Thickness(1)
                    xp.BorderBrush = Brushes.Black
                    xp.FlowDirection = Windows.FlowDirection.LeftToRight
                    Dim thickness As Windows.Thickness = New Windows.Thickness(20, 2, 2, 2)
                    sp.SetValue(Windows.Controls.StackPanel.MarginProperty, thickness)
            End Select
        Next
        rootScroller.Content = rootStack
        dockPanel1.Children.Add(rootScroller)
    End Sub

    'Handler: Button click 
    Private Sub btn_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If currentViewer_ IsNot Nothing Then
            Dim btn As Windows.Controls.Button = sender
            If btn.Name = "Zoom_In" Then
                currentViewer_.ZoomIn()
            ElseIf btn.Name = "Zoom_Out" Then
                currentViewer_.ZoomOut()
            ElseIf btn.Name = "Set_Cursor" Then
                Dim p As Windows.Point = New Windows.Point(GetControlInt("Point X"), GetControlInt("Point Y"))
                currentViewer_.CursorPosition = p
            ElseIf btn.Name = "Set_Region" Then
                Dim rect As Windows.Rect = New Windows.Rect(GetControlInt("Box X"), GetControlInt("Box Y"), GetControlInt("Box Width"), GetControlInt("Box Height"))
                currentViewer_.DataSelection = rect
            ElseIf btn.Name = "OptimizeContrast" Then
                If currentViewer_.ActualDisplayType = DisplayType.Image Then
                    currentViewer_.OptimizeContrast(AutoScaleContrastMethod.Default)
                End If
            ElseIf btn.Name = "AutoScaleIntensity" Then
                If currentViewer_.ActualDisplayType = DisplayType.Image Then
                    currentViewer_.AutoScaleIntensity()
                End If
            ElseIf btn.Name = "SetIntensityLevels" Then
                If currentViewer_.ActualDisplayType = DisplayType.Image Then
                    currentViewer_.SetIntensityLevels(GetControlDouble("BlackLevel"), GetControlDouble("WhiteLevel"))
                End If
            ElseIf btn.Name = "ZoomToBestFit" Then
                currentViewer_.ZoomToBestFit()
            ElseIf btn.Name = "ZoomXAxisToBestFit" Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.ZoomXAxisToBestFit()
                End If
            ElseIf btn.Name = "ZoomYAxisToBestFit" Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.ZoomYAxisToBestFit()
                End If
            ElseIf btn.Name = "ZoomToActualSize" Then
                currentViewer_.ZoomToActualSize()
            End If
        End If
    End Sub

    'Handler: ComboBox selection changed 
    Private Sub cb_SelectionChanged(sender As System.Object, e As SelectionChangedEventArgs)
        If currentViewer_ IsNot Nothing Then
            Dim cb As Windows.Controls.ComboBox = sender
            If cb.Name.Contains("CursorStyle") Then
                If currentViewer_.ActualDisplayType = DisplayType.Image Then
                    currentViewer_.CursorStyle = [Enum].Parse(GetType(DataCursorStyle), cb.SelectedItem.ToString())
                End If
            ElseIf cb.Name.Contains("CrossSections") Then
                currentViewer_.CrossSections = [Enum].Parse(GetType(DisplayCrossSections), cb.SelectedItem.ToString())
            ElseIf cb.Name.Contains("View_Type") Then
                currentViewer_.DisplayType = [Enum].Parse(GetType(DisplayType), cb.SelectedItem.ToString())
            ElseIf cb.Name.Contains("GraphGridLines") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.GraphGridLines = [Enum].Parse(GetType(GraphGridLines), cb.SelectedItem.ToString())
                End If
            ElseIf cb.Name.Contains("PlottingStyle") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.PlottingStyle = [Enum].Parse(GetType(PlottingStyle), cb.SelectedItem.ToString())
                End If
            ElseIf cb.Name.Contains("PeaksIndicated") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.PeaksIndicated = [Enum].Parse(GetType(PeaksIndicated), cb.SelectedItem.ToString())
                End If
            ElseIf cb.Name.Contains("PseudoColorPalette") Then
                currentViewer_.PseudoColorPalette = System.Enum.Parse(GetType(PseudoColorPalette), cb.SelectedItem.ToString())
            ElseIf cb.Name.Contains("GraphZoomMode") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.GraphZoomMode = System.Enum.Parse(GetType(GraphZoomMode), cb.SelectedItem.ToString())
                End If
            ElseIf cb.Name.Contains("CurrentSource") Then 'Changing the source effects other controls
                currentViewer_.DisplaySourceIndex = ToSource(System.Enum.Parse(GetType(GraphSources), cb.SelectedItem.ToString()))
                'Reset the sliders 
                Dim frames As Windows.Controls.Slider = GetControl("Frame")
                Dim regions As Windows.Controls.Slider = GetControl("Region")
                Dim rows As Windows.Controls.Slider = GetControl("Row")
                frames.Minimum = 0
                frames.Maximum = currentViewer_.Frames - 1
                frames.IsEnabled = IIf(frames.Maximum = frames.Minimum, False, True)
                regions.Minimum = 0
                regions.Maximum = currentViewer_.Regions - 1
                regions.IsEnabled = IIf(regions.Maximum = regions.Minimum, False, True)
                rows.Minimum = 0
                rows.Maximum = currentViewer_.Rows - 1
                rows.IsEnabled = IIf(rows.Maximum = rows.Minimum, False, True)
            End If
        End If
    End Sub

    'Handler: EditBox lost focus
    Private Sub cb_LostFocus(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If currentViewer_ IsNot Nothing Then
            Dim b As Windows.Controls.TextBox = sender
            If b.Name.Contains("PlaybackFrameRate") Then
                currentViewer_.PlaybackFrameRate = GetControlDouble("PlaybackFrameRate")
            End If
        End If
    End Sub

    'Handler: CheckBox click
    Private Sub cb_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        If currentViewer_ IsNot Nothing Then
            Dim b As Windows.Controls.CheckBox = sender
            If b.Name.Contains("GateTracking_Delay") Then
                currentViewer_.ShowGateTrackingDelay = b.IsChecked
            ElseIf b.Name.Contains("GateTracking_Width") Then
                currentViewer_.ShowGateTrackingWidth = b.IsChecked
            ElseIf b.Name.Contains("Exposure_Start") Then
                currentViewer_.ShowExposureStartedTimeStamp = b.IsChecked
            ElseIf b.Name.Contains("Exposure_End") Then
                currentViewer_.ShowExposureEndedTimeStamp = b.IsChecked
            ElseIf b.Name.Contains("Frame_Tracking_Number") Then
                currentViewer_.ShowFrameTrackingNumber = b.IsChecked
            ElseIf b.Name.Contains("Absolute_Time") Then
                currentViewer_.ShowTimeStampsInAbsoluteTime = b.IsChecked
            ElseIf b.Name.Contains("IsPlaybackRunning") Then
                currentViewer_.IsPlaybackRunning = b.IsChecked
            ElseIf b.Name.Contains("RepeatPlayback") Then
                currentViewer_.RepeatPlayback = b.IsChecked
            ElseIf b.Name.Contains("AlwaysAutoScaleIntensity") Then
                If currentViewer_.ActualDisplayType = DisplayType.Image Then
                    currentViewer_.AlwaysAutoScaleIntensity = b.IsChecked
                End If
            ElseIf b.Name.Contains("PlotsStacked") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.PlotsStacked = b.IsChecked
                End If
            ElseIf b.Name.Contains("DataPointsVisible") Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    currentViewer_.DataPointsVisible = b.IsChecked
                End If
            ElseIf b.Name.Contains("Phase_Modulation") Then
                currentViewer_.ShowModulationTrackingPhase = b.IsChecked
            End If
        End If
    End Sub

    'Handler: Slider value changed
    Private Sub sld_ValueChanged(sender As System.Object, e As System.Windows.RoutedPropertyChangedEventArgs(Of Double))
        If currentViewer_ IsNot Nothing Then
            If sender.Name = "Zoom" Then
                currentViewer_.Zoom = e.NewValue
            ElseIf sender.Name = "Frame" Then
                currentViewer_.FrameIndex = e.NewValue
            ElseIf sender.Name = "Region" Then
                currentViewer_.RegionIndex = e.NewValue
                'Change the row slider to zero during a region change
                'Also recheck the maximum different regions will have different height in some cases
                Dim sld As Windows.Controls.Slider = GetControl("Row")
                If sld IsNot Nothing And currentViewer_.ActualDisplayType = DisplayType.Graph Then
                    sld.Value = 0
                    sld.Maximum = currentViewer_.Rows
                End If
            ElseIf sender.Name = "Row" Then
                If currentViewer_.ActualDisplayType = DisplayType.Graph Then 'Can only be set in Graph display type
                    currentViewer_.RowIndex = e.NewValue
                End If
            End If
        End If
    End Sub

    'Converters
    Public Function FromSource(source As Integer) As GraphSources
        Select Case source
            Case 0
                Return GraphSources.Source1
            Case 1
                Return GraphSources.Source2
            Case 2
                Return GraphSources.Source3
            Case 3
                Return GraphSources.Source4
            Case 4
                Return GraphSources.Source5
            Case Else
                Return GraphSources.Source1
        End Select
    End Function

    Public Function ToSource(source As GraphSources) As Integer
        Select Case source
            Case GraphSources.Source1
                Return 0
            Case GraphSources.Source2
                Return 1
            Case GraphSources.Source3
                Return 2
            Case GraphSources.Source4
                Return 3
            Case GraphSources.Source5
                Return 4
            Case Else
                Return 0
        End Select
    End Function

    'Determine if a new grid is needed.
    Public Function NewGridNeeded(oldGrid As Windows.Controls.Grid) As Windows.Controls.Grid
        'Current grid being processed
        If oldGrid IsNot Nothing Then
            Return oldGrid
        End If
        'Begin the grid
        Dim grid As Windows.Controls.Grid = New Windows.Controls.Grid()
        'Always text & control nothing more so 2 cols suffice
        For col As Integer = 0 To 1
            grid.ColumnDefinitions.Add(New ColumnDefinition())
        Next
        'Apply a margin
        grid.SetValue(grid.MarginProperty, New Thickness(20, 2, 2, 2))
        'Return
        Return grid
    End Function

    'Find a control by name
    Public Function GetControl(name As String) As Object
        For i As Integer = 0 To controls_.Count() - 1
            If name = controls_(i).GetName() Then
                Return controls_(i).ControlItem
            End If
        Next
        Return 0
    End Function

    'Find a Control (Integer)
    Public Function GetControlInt(name As String) As Integer
        For i As Integer = 0 To controls_.Count() - 1
            If name = controls_(i).GetName() Then
                Return Convert.ToInt32((controls_(i).ControlItem).Text)
            End If
        Next
        Return 0
    End Function

    'Find a Control (Double)
    Public Function GetControlDouble(name As String) As Double
        For i As Integer = 0 To controls_.Count() - 1
            If name = controls_(i).GetName() Then
                Return Convert.ToDouble((controls_(i).ControlItem).Text)
            End If
        Next
        Return 0
    End Function
End Class