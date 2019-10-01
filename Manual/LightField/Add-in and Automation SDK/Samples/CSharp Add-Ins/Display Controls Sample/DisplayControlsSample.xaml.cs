using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Reflection;
using System.Text.RegularExpressions;
using System.IO;
using System.Windows.Markup;
using System.Threading;

using PrincetonInstruments.LightField.AddIns;

namespace LightFieldAddInSamples
{
    public enum GraphSources
    {
        Source1,
        Source2,
        Source3,
        Source4,
        Source5
    }

    /// <summary>
    /// Interaction logic for DisplayControlsSample.xaml
    /// </summary>
    public partial class DisplayControlsSample : Window
    {
        ILightFieldApplication application_;
        List<ControlWidget> controls_;
        IDisplayViewer currentViewer_;
        IDisplay display_;
        DisplayLocation selectedLocation_;
        int selectedIndex_;
        DisplayLayout selectedLayout_;

        // Converters
        public GraphSources FromSource(int source)
        {
            switch (source)
            {
                case 0:  return GraphSources.Source1;
                case 1:  return GraphSources.Source2;
                case 2:  return GraphSources.Source3;
                case 3:  return GraphSources.Source4;
                case 4:  return GraphSources.Source5;
                default: return GraphSources.Source1;
            }
        }
        public int ToSource(GraphSources source)
        {
            switch (source)
            {
                case GraphSources.Source1:  return 0;
                case GraphSources.Source2:  return 1;
                case GraphSources.Source3:  return 2;
                case GraphSources.Source4:  return 3;
                case GraphSources.Source5:  return 4;
                default:                    return 0;
            }
        }

        // Determine if a new grid is needed.
        public Grid NewGridNeeded(Grid oldGrid)
        {
            // Current Grid Being Processed
            if (oldGrid != null)
                return oldGrid;

            // Begin the grid
            Grid grid = new Grid();

            // Always Text & Control nothing more so 2 cols suffice
            for (int col = 0; col < 2; col++)
                grid.ColumnDefinitions.Add(new ColumnDefinition());

            // Apply a margin
            grid.SetValue(Grid.MarginProperty, new Thickness(20, 2, 2, 2));

            // Return
            return grid;
        }
        // Find a control by name
        public object GetControl(string name)
        {
            for (int i = 0; i < controls_.Count(); i++)
            {
                if (name == controls_[i].GetName())
                    return controls_[i].ControlItem;
            }
            return 0;
        }
        // Find a Control (Integer)
        public int GetControlInt(string name)
        {
            for (int i = 0; i < controls_.Count(); i++)
            {
                if (name == controls_[i].GetName())
                    return Convert.ToInt32(((TextBox)controls_[i].ControlItem).Text);
            }
            return 0;
        }
        // Find a Control (Double)
        public double GetControlDouble(string name)
        {
            for (int i = 0; i < controls_.Count(); i++)
            {
                if (name == controls_[i].GetName())
                    return Convert.ToDouble(((TextBox)controls_[i].ControlItem).Text);
            }
            return 0;
        }
        // Handle Buttons
        public void btn_Click(object sender, RoutedEventArgs e)
        {
            if (currentViewer_ != null)
            {
                Button btn = (Button)sender;

                if (btn.Name == "Zoom_In")
                    currentViewer_.ZoomIn();
                if (btn.Name == "Zoom_Out")
                    currentViewer_.ZoomOut();
                if (btn.Name == "Set_Cursor")
                {
                    Point p = new Point(GetControlInt("Point X"),GetControlInt("Point Y")); 
                    currentViewer_.CursorPosition = p;                    
                }
                if (btn.Name == "Set_Region")
                {
                    Rect rect = new Rect(GetControlInt("Box X"), GetControlInt("Box Y"), GetControlInt("Box Width"), GetControlInt("Box Height"));
                    currentViewer_.DataSelection = rect;
                }

                if (btn.Name == "ZoomToBestFit")
                    currentViewer_.ZoomToBestFit();

                // Image only buttons
                if (currentViewer_.ActualDisplayType == DisplayType.Image)
                {
                    if (btn.Name == "OptimizeContrast")
                        currentViewer_.OptimizeContrast(AutoScaleContrastMethod.Default);
                    if (btn.Name == "AutoScaleIntensity")
                        currentViewer_.AutoScaleIntensity();
                    if (btn.Name == "SetIntensityLevels")
                        currentViewer_.SetIntensityLevels(GetControlDouble("BlackLevel"), GetControlDouble("WhiteLevel"));
                }                                
                // Graph only buttons
                if (currentViewer_.ActualDisplayType == DisplayType.Graph)
                {
                    if (btn.Name == "ZoomXAxisToBestFit")
                        currentViewer_.ZoomXAxisToBestFit();
                    if (btn.Name == "ZoomYAxisToBestFit")
                        currentViewer_.ZoomYAxisToBestFit();
                }

                if (btn.Name == "ZoomToActualSize")
                    currentViewer_.ZoomToActualSize();
            }
        }
        // Handle Combo Boxes
        void cb_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (currentViewer_ != null)
            {
                ComboBox cb = (ComboBox)sender;                

                if (cb.Name.Contains("CrossSections"))
                    currentViewer_.CrossSections = (DisplayCrossSections)Enum.Parse(typeof(DisplayCrossSections), cb.SelectedItem.ToString());
                if (cb.Name.Contains("View_Type"))
                    currentViewer_.DisplayType = (DisplayType)Enum.Parse(typeof(DisplayType), cb.SelectedItem.ToString());

                // Image only selection box
                if (currentViewer_.ActualDisplayType == DisplayType.Image)
                {
                    if (cb.Name.Contains("CursorStyle"))
                        currentViewer_.CursorStyle = (DataCursorStyle)Enum.Parse(typeof(DataCursorStyle), cb.SelectedItem.ToString());
                }
                // Graph only controls
                if (currentViewer_.ActualDisplayType == DisplayType.Graph)
                {
                    if (cb.Name.Contains("GraphGridLines"))
                        currentViewer_.GraphGridLines = (GraphGridLines)Enum.Parse(typeof(GraphGridLines), cb.SelectedItem.ToString());
                    if (cb.Name.Contains("PlottingStyle"))
                        currentViewer_.PlottingStyle = (PlottingStyle)Enum.Parse(typeof(PlottingStyle), cb.SelectedItem.ToString());
                    if (cb.Name.Contains("PeaksIndicated"))
                        currentViewer_.PeaksIndicated = (PeaksIndicated)Enum.Parse(typeof(PeaksIndicated), cb.SelectedItem.ToString());
                    if (cb.Name.Contains("GraphZoomMode"))
                        currentViewer_.GraphZoomMode = (GraphZoomMode)Enum.Parse(typeof(GraphZoomMode), cb.SelectedItem.ToString());
                }
                
                if (cb.Name.Contains("PseudoColorPalette"))
                    currentViewer_.PseudoColorPalette = (PseudoColorPalette)Enum.Parse(typeof(PseudoColorPalette), cb.SelectedItem.ToString());
                
                // Changing The Source Effects Other Controls
                if (cb.Name.Contains("CurrentSource"))
                {
                    currentViewer_.DisplaySourceIndex = ToSource((GraphSources)Enum.Parse(typeof(GraphSources), cb.SelectedItem.ToString()));

                    // Reset The Sliders 
                    Slider frames = (Slider)GetControl("Frame");
                    Slider regions = (Slider)GetControl("Region");
                    Slider rows = (Slider)GetControl("Row");

                    frames.Minimum = 0;
                    frames.Maximum = currentViewer_.Frames - 1;
                    frames.IsEnabled = (frames.Maximum == frames.Minimum) ? false : true;

                    regions.Minimum = 0;
                    regions.Maximum = currentViewer_.Regions - 1;
                    regions.IsEnabled = (regions.Maximum == regions.Minimum) ? false : true;

                    rows.Minimum = 0;
                    rows.Maximum = currentViewer_.Rows - 1;
                    rows.IsEnabled = (rows.Maximum == rows.Minimum) ? false : true;
                }
            }
        }
        // Handle Edit Boxes
        void cb_LostFocus(object sender, RoutedEventArgs e)
        {
            if (currentViewer_ != null)
            {
                TextBox b = (TextBox)sender;

                if (b.Name.Contains("PlaybackFrameRate"))
                    currentViewer_.PlaybackFrameRate = GetControlDouble("PlaybackFrameRate");
            }
        }
        // Handle Check Boxes
        void cb_Click(object sender, RoutedEventArgs e)
        {
            if (currentViewer_ != null)
            {
                CheckBox b = (CheckBox)sender;

                if (b.Name.Contains("GateTracking_Delay"))
                    currentViewer_.ShowGateTrackingDelay = (bool)b.IsChecked;
                if (b.Name.Contains("GateTracking_Width"))
                    currentViewer_.ShowGateTrackingWidth = (bool)b.IsChecked;
                if (b.Name.Contains("Exposure_Start"))
                    currentViewer_.ShowExposureStartedTimeStamp = (bool)b.IsChecked;
                if (b.Name.Contains("Exposure_End"))
                    currentViewer_.ShowExposureEndedTimeStamp = (bool)b.IsChecked;
                if (b.Name.Contains("Frame_Tracking_Number"))
                    currentViewer_.ShowFrameTrackingNumber = (bool)b.IsChecked;
                if (b.Name.Contains("Absolute_Time"))
                    currentViewer_.ShowTimeStampsInAbsoluteTime = (bool)b.IsChecked;
                if (b.Name.Contains("IsPlaybackRunning"))
                    currentViewer_.IsPlaybackRunning = (bool)b.IsChecked;
                if (b.Name.Contains("RepeatPlayback"))
                    currentViewer_.RepeatPlayback = (bool)b.IsChecked;

                // Image only buttons
                if (currentViewer_.ActualDisplayType == DisplayType.Image)
                {
                    if (b.Name.Contains("AlwaysAutoScaleIntensity"))
                        currentViewer_.AlwaysAutoScaleIntensity = (bool)b.IsChecked;
                }
                // Graph only Check boxes
                if (currentViewer_.ActualDisplayType == DisplayType.Graph)
                {
                    if (b.Name.Contains("PlotsStacked"))
                        currentViewer_.PlotsStacked = (bool)b.IsChecked;
                    if (b.Name.Contains("DataPointsVisible"))
                        currentViewer_.DataPointsVisible = (bool)b.IsChecked;
                }

                if (b.Name.Contains("Phase_Modulation"))
                    currentViewer_.ShowModulationTrackingPhase = (bool)b.IsChecked;
            }
        }
        // Handle Slider Changes
        void sld_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (currentViewer_ != null)
            {
                if (((Slider)sender).Name == "Zoom")
                    currentViewer_.Zoom = e.NewValue;
                if (((Slider)sender).Name == "Frame")
                    currentViewer_.FrameIndex = (long)e.NewValue;
                if (((Slider)sender).Name == "Region")
                {
                    currentViewer_.RegionIndex = (int)e.NewValue;

                    // Change The Row Slider to zero during a region change
                    // also recheck the maximum different regions will have 
                    // different height in some cases.
                    Slider sld = (Slider) GetControl("Row");
                    if ((sld != null) && (currentViewer_.ActualDisplayType == DisplayType.Graph))
                    {
                        sld.Value = 0;
                        sld.Maximum = currentViewer_.Rows;
                    }
                }
                // We can not set a row index if the actual display type is a graph
                if ((((Slider)sender).Name == "Row") && (currentViewer_.ActualDisplayType == DisplayType.Graph))
                    currentViewer_.RowIndex = (int)e.NewValue;
            }
        }
        ////////////////////////////////////////////////////////////////////////////////////
        // Loaded 
        ////////////////////////////////////////////////////////////////////////////////////
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {            
        }
        ////////////////////////////////////////////////////////////////////////////////////
        // Control Builder
        ////////////////////////////////////////////////////////////////////////////////////
        public void BuildDisplayControls(IDisplayViewer view)
        {
            // Nuke the children!
            dockPanel1.Children.Clear();
            
            // Can't create controls for a view if one does not exist
            if (view == null)
                return;

            // the current viewer is used in the callback handlers for the controls
            currentViewer_ = view;

            // Build Controls From Viable Settings
            ScrollViewer rootScroller = new ScrollViewer();
            StackPanel rootStack = new StackPanel();

            controls_ = new List<ControlWidget>();

            // Build Controls Up & Set the Current Value to Match the chosen view(Argument)

            // General
            controls_.Add(new ControlWidget("General", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("View Type", ControlWidgetType.ComboBox, view.DisplayType));

            // Zooming
            controls_.Add(new ControlWidget("Zooming", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("Zoom Out", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("Zoom In", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("Zoom", ControlWidgetType.SliderBar, view.Zoom, view.MinimumZoom, view.MaximumZoom));
            controls_.Add(new ControlWidget("ZoomToBestFit", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("ZoomToActualSize", ControlWidgetType.Button, 0));

            // Stamping
            controls_.Add(new ControlWidget("Stamping", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("Exposure Start", ControlWidgetType.CheckBox, view.ShowExposureStartedTimeStamp));
            controls_.Add(new ControlWidget("Exposure End", ControlWidgetType.CheckBox, view.ShowExposureEndedTimeStamp));
            controls_.Add(new ControlWidget("Frame Tracking Number", ControlWidgetType.CheckBox, view.ShowFrameTrackingNumber));
            controls_.Add(new ControlWidget("Absolute Time", ControlWidgetType.CheckBox, view.ShowTimeStampsInAbsoluteTime));
            controls_.Add(new ControlWidget("GateTracking Delay", ControlWidgetType.CheckBox, view.ShowGateTrackingDelay));
            controls_.Add(new ControlWidget("GateTracking Width", ControlWidgetType.CheckBox, view.ShowGateTrackingWidth));
            controls_.Add(new ControlWidget("Phase Modulation", ControlWidgetType.CheckBox, view.ShowModulationTrackingPhase));

            // Regions, Frames & Rows
            controls_.Add(new ControlWidget("Source,Frames,Regions,Rows", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("CurrentSource", ControlWidgetType.ComboBox, FromSource(view.DisplaySourceIndex)));
            controls_.Add(new ControlWidget("Frame", ControlWidgetType.SliderBar, view.FrameIndex, 0, view.Frames - 1));
            controls_.Add(new ControlWidget("Region", ControlWidgetType.SliderBar, view.RegionIndex, 0, view.Regions - 1));
            controls_.Add(new ControlWidget("Row", ControlWidgetType.SliderBar, view.RowIndex, 0, view.Rows - 1));

            // Playback
            controls_.Add(new ControlWidget("Playback", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("IsPlaybackRunning", ControlWidgetType.CheckBox, view.IsPlaybackRunning));
            controls_.Add(new ControlWidget("RepeatPlayback", ControlWidgetType.CheckBox, view.RepeatPlayback));
            controls_.Add(new ControlWidget("PlaybackFrameRate", ControlWidgetType.EditBox, view.PlaybackFrameRate));

            // Scaling 
            controls_.Add(new ControlWidget("Scaling", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("OptimizeContrast", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("AutoScaleIntensity", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("AlwaysAutoScaleIntensity", ControlWidgetType.CheckBox, view.AlwaysAutoScaleIntensity));            
            controls_.Add(new ControlWidget("BlackLevel", ControlWidgetType.EditBox, 0));
            controls_.Add(new ControlWidget("WhiteLevel", ControlWidgetType.EditBox, 0));
            controls_.Add(new ControlWidget("SetIntensityLevels", ControlWidgetType.Button, 0));

            // Graph Controls
            controls_.Add(new ControlWidget("Graph", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("GraphGridLines", ControlWidgetType.ComboBox, view.GraphGridLines));
            controls_.Add(new ControlWidget("PlottingStyle", ControlWidgetType.ComboBox, view.PlottingStyle));
            controls_.Add(new ControlWidget("PeaksIndicated", ControlWidgetType.ComboBox, view.PeaksIndicated));
            controls_.Add(new ControlWidget("PlotsStacked", ControlWidgetType.CheckBox, view.PlotsStacked));
            controls_.Add(new ControlWidget("DataPointsVisible", ControlWidgetType.CheckBox, view.DataPointsVisible));
            controls_.Add(new ControlWidget("GraphZoomMode", ControlWidgetType.ComboBox, view.GraphZoomMode));
            controls_.Add(new ControlWidget("ZoomXAxisToBestFit", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("ZoomYAxisToBestFit", ControlWidgetType.Button, 0));            

            // Pseudo Color 
            controls_.Add(new ControlWidget("PseudoColor", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("PseudoColorPalette", ControlWidgetType.ComboBox, view.PseudoColorPalette));           

            // Cursors (Single Position)
            int x = 0, y = 0;
            Point? p = view.CursorPosition;
            if (p != null)
            {
                x = (int)((Point)p).X;
                y = (int)((Point)p).Y;
            }

            // Cursor Box
            int bx, by, bw, bh;
            Rect rect = view.DataSelection;
            bx = (int)rect.X;
            by = (int)rect.Y;
            bw = (int)rect.Width;
            bh = (int)rect.Height;
            
            if (bx < 0) bx = 0;
            if (by < 0) by = 0;
            if (bw < 0) bw = 0;
            if (bh < 0) bh = 0;

            controls_.Add(new ControlWidget("Cursors", ControlWidgetType.Expander, 0));
            controls_.Add(new ControlWidget("CursorStyle", ControlWidgetType.ComboBox, view.CursorStyle));
            controls_.Add(new ControlWidget("CrossSections", ControlWidgetType.ComboBox, view.CrossSections));
            controls_.Add(new ControlWidget("Point X", ControlWidgetType.EditBox, x));
            controls_.Add(new ControlWidget("Point Y", ControlWidgetType.EditBox, y));
            controls_.Add(new ControlWidget("Set Cursor", ControlWidgetType.Button, 0));
            controls_.Add(new ControlWidget("Box X", ControlWidgetType.EditBox, bx));
            controls_.Add(new ControlWidget("Box Y", ControlWidgetType.EditBox, by));
            controls_.Add(new ControlWidget("Box Width", ControlWidgetType.EditBox, bw));
            controls_.Add(new ControlWidget("Box Height", ControlWidgetType.EditBox, bh));
            controls_.Add(new ControlWidget("Set Region", ControlWidgetType.Button, 0));

            // Everything Else
            controls_.Add(new ControlWidget("Miscellaneous", ControlWidgetType.Expander, 0));

            // Start off Empty
            Stack<Expander> expanderStack = new Stack<Expander>();
            Stack<StackPanel> stackPanelStack = new Stack<StackPanel>();

            Grid grid = null;
            int rowIdx = 0;

            for (int i = 0; i < controls_.Count(); i++)
            {
                switch (controls_[i].GetWidgetType())
                {
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.Button:
                        {
                            if ((grid = NewGridNeeded(grid)) != null)
                            {
                                grid.RowDefinitions.Add(new RowDefinition());

                                Button btn = new Button();
                                controls_[i].ControlItem = btn;
                                btn.Name = controls_[i].GetName().Replace(' ', '_');
                                btn.Content = btn.Name;
                                btn.VerticalAlignment = VerticalAlignment.Center;
                                btn.Margin = new Thickness(2, 2, 2, 2);
                                grid.Children.Add(btn);
                                Grid.SetRow(btn, rowIdx);
                                Grid.SetColumn(btn, 1);

                                // Text Block is common
                                TextBlock tb = new TextBlock() { Text = btn.Name };
                                tb.TextWrapping = TextWrapping.Wrap;
                                grid.Children.Add(tb);
                                Grid.SetRow(tb, rowIdx);
                                Grid.SetColumn(tb, 0);

                                btn.Click += new RoutedEventHandler(btn_Click);

                                rowIdx++;
                            }
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.CheckBox:
                        {
                            if ((grid = NewGridNeeded(grid)) != null)
                            {
                                grid.RowDefinitions.Add(new RowDefinition());

                                CheckBox cb = new CheckBox();
                                controls_[i].ControlItem = cb;
                                cb.Margin = new Thickness(2, 2, 2, 2);
                                cb.IsChecked = (bool)controls_[i].GetValue();
                                cb.HorizontalAlignment = HorizontalAlignment.Center;
                                cb.VerticalAlignment = VerticalAlignment.Center;
                                cb.Name = controls_[i].GetName().Replace(' ', '_');
                                grid.Children.Add(cb);
                                Grid.SetRow(cb, rowIdx);
                                Grid.SetColumn(cb, 1);

                                cb.Click += new RoutedEventHandler(cb_Click);

                                // Text Block is common
                                TextBlock tb = new TextBlock() { Text = cb.Name };
                                tb.TextWrapping = TextWrapping.Wrap;
                                grid.Children.Add(tb);
                                Grid.SetRow(tb, rowIdx);
                                Grid.SetColumn(tb, 0);

                                rowIdx++;
                            }
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.ComboBox:
                        {
                            if ((grid = NewGridNeeded(grid)) != null)
                            {
                                grid.RowDefinitions.Add(new RowDefinition());
                                ComboBox cb = new ComboBox();
                                controls_[i].ControlItem = cb;
                                cb.VerticalAlignment = VerticalAlignment.Center;
                                cb.Margin = new Thickness(2, 2, 2, 2);
                                cb.Name = controls_[i].GetName().Replace(' ', '_');
                                grid.Children.Add(cb);
                                Grid.SetRow(cb, rowIdx);
                                Grid.SetColumn(cb, 1);

                                // Using reflection add all of the enums
                                string[] enumStrings = Enum.GetNames(controls_[i].GetValue().GetType());
                                foreach (string s in enumStrings)
                                {
                                    if (s!= "UninitializedEnum")
                                        cb.Items.Add(s);
                                }
                                cb.SelectedItem = controls_[i].GetValue().ToString();
                                cb.SelectionChanged += new SelectionChangedEventHandler(cb_SelectionChanged);

                                // Text Block is common
                                TextBlock tb = new TextBlock() { Text = cb.Name };
                                tb.TextWrapping = TextWrapping.Wrap;
                                grid.Children.Add(tb);
                                Grid.SetRow(tb, rowIdx);
                                Grid.SetColumn(tb, 0);

                                rowIdx++;
                            }
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.EditBox:
                        {
                            if ((grid = NewGridNeeded(grid)) != null)
                            {
                                grid.RowDefinitions.Add(new RowDefinition());
                                TextBox cb = new TextBox();
                                controls_[i].ControlItem = cb;
                                cb.Margin = new Thickness(2, 2, 2, 2);
                                cb.Text = controls_[i].GetValue().ToString();
                                cb.TextAlignment = TextAlignment.Right;
                                cb.VerticalAlignment = VerticalAlignment.Center;
                                cb.Height = 25;

                                grid.Children.Add(cb); // Right Before Global Calls
                                Grid.SetRow(cb, rowIdx);
                                Grid.SetColumn(cb, 1);
                                cb.LostFocus += new RoutedEventHandler(cb_LostFocus);
                                cb.Name = controls_[i].GetName().Replace(' ', '_');

                                // Text Block is common
                                TextBlock tb = new TextBlock() { Text = cb.Name };
                                tb.TextWrapping = TextWrapping.Wrap;
                                grid.Children.Add(tb);
                                Grid.SetRow(tb, rowIdx);
                                Grid.SetColumn(tb, 0);

                                rowIdx++;
                            }
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.Expander:
                        {
                            // Pop And Link
                            if ((stackPanelStack.Count() > 0) && (expanderStack.Count() > 0))
                            {
                                Expander expander = expanderStack.Pop();
                                StackPanel stackpanel = stackPanelStack.Pop();

                                expander.Content = grid;

                                // If Zero its added already
                                if (stackPanelStack.Count() != 0)
                                    stackpanel.Children.Add(expander);

                                // The Grid is done
                                grid = null;
                            }

                            var sp = new StackPanel();
                            var xp = new Expander();


                            stackPanelStack.Push(sp);
                            expanderStack.Push(xp);
                            
                            xp.Header = controls_[i].GetName();
                            xp.BorderThickness = new Thickness(1);
                            xp.BorderBrush = Brushes.Black;
                            xp.FlowDirection = FlowDirection.LeftToRight;

                            // Add To Root
                            if (stackPanelStack.Count == 1)
                                rootStack.Children.Add(xp);

                            // Reset Control Count For Grid
                            rowIdx = 0;
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.ReadOnlyEditBox:
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.SliderBar:
                        if ((grid = NewGridNeeded(grid)) != null)
                        {
                            grid.RowDefinitions.Add(new RowDefinition());
                            Slider sld = new Slider();
                            sld.Margin = new Thickness(2, 2, 2, 2);
                            controls_[i].ControlItem = sld;
                            sld.Name = controls_[i].GetName().Replace(' ', '_');
                            sld.VerticalAlignment = VerticalAlignment.Center;

                            grid.Children.Add(sld);
                            Grid.SetRow(sld, rowIdx);
                            Grid.SetColumn(sld, 1);

                            sld.Minimum = controls_[i].SliderMin();
                            sld.Maximum = controls_[i].SliderMax();
                            if (sld.Maximum == sld.Minimum)
                                sld.IsEnabled = false;

                            sld.Value = Convert.ToDouble(controls_[i].GetValue());                            
                            sld.ValueChanged += new RoutedPropertyChangedEventHandler<double>(sld_ValueChanged);

                            // Text Block is common
                            TextBlock tb = new TextBlock() { Text = sld.Name };
                            tb.TextWrapping = TextWrapping.Wrap;
                            grid.Children.Add(tb);
                            Grid.SetRow(tb, rowIdx);
                            Grid.SetColumn(tb, 0);

                            rowIdx++;
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.SubEnd:
                        {
                            // Pop And Link
                            if ((stackPanelStack.Count() > 0) && (expanderStack.Count() > 0))
                            {
                                Expander expander = expanderStack.Pop();
                                StackPanel stackpanel = stackPanelStack.Pop();

                                expander.Content = grid;

                                // If Zero its added already
                                if (stackPanelStack.Count() != 0)
                                    stackpanel.Children.Add(expander);

                                // The Grid is done
                                grid = null;
                            }
                        }
                        break;
                    ////////////////////////////////////////////////////////////////////////////////
                    case ControlWidgetType.SubExpander:
                        {
                            // Reset Control Count For Grid
                            rowIdx = 0;

                            var sp = new StackPanel();
                            var xp = new Expander();

                            stackPanelStack.Push(sp);
                            expanderStack.Push(xp);

                            xp.Header = controls_[i].GetName();
                            sp.Children.Add(xp);
                            sp.Background = Brushes.Beige;

                            xp.BorderThickness = new Thickness(1);
                            xp.BorderBrush = Brushes.Black;
                            xp.FlowDirection = FlowDirection.LeftToRight;

                            Thickness thickness = new Thickness(20, 2, 2, 2);
                            sp.SetValue(StackPanel.MarginProperty, thickness);
                        }
                        break;
                }
            }
            rootScroller.Content = rootStack;
            dockPanel1.Children.Add(rootScroller);
        }
        ////////////////////////////////////////////////////////////////////////////////////
        // Constructor
        ////////////////////////////////////////////////////////////////////////////////////
        public DisplayControlsSample(ILightFieldApplication app)
        {
            // Cache Some Members
            application_ = app;                        
            display_     = application_.DisplayManager;
            
            // Initialize the WPF component
            InitializeComponent();
           
            // Setup Layout Mode Combo Box
            LayoutCombo.Items.Add(DisplayLayout.One);
            LayoutCombo.Items.Add(DisplayLayout.TwoHorizontal);
            LayoutCombo.Items.Add(DisplayLayout.TwoVertical);
            LayoutCombo.Items.Add(DisplayLayout.ThreeTopFavored);
            LayoutCombo.Items.Add(DisplayLayout.ThreeVertical);
            LayoutCombo.Items.Add(DisplayLayout.FourEven);
            LayoutCombo.Items.Add(DisplayLayout.FourTopFavored);
            LayoutCombo.Items.Add(DisplayLayout.FourVertical);
            LayoutCombo.Items.Add(DisplayLayout.FourLeftFavored);
            LayoutCombo.Items.Add(DisplayLayout.FiveTopFavored);
            LayoutCombo.Items.Add(DisplayLayout.FiveLeftFavored);

            // Defaults from application
            selectedLocation_ = display_.Location;
            selectedLayout_   = display_.ExperimentWorkspaceLayout;            

            // Default Combo Boxes
            LayoutCombo.SelectedItem   = selectedLayout_;

            // Experiment
            if (selectedLocation_ == DisplayLocation.ExperimentWorkspace)
                LocationCombo.SelectedIndex = 0;
            // Data Workspace
            else
                LocationCombo.SelectedIndex = 1;

            IndexCombo.SelectedIndex   = 0;
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void DisplayButton_Click(object sender, RoutedEventArgs e)
        {
            // Display Test Code            
            if (display_ != null)
            {
                // Get The Views
                var view1_ = display_.GetDisplay(selectedLocation_, selectedIndex_);
                BuildDisplayControls(view1_);
            }
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void LocationCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {            
            switch (LocationCombo.SelectedIndex)
            {
                case 0:
                    selectedLocation_ = DisplayLocation.ExperimentWorkspace;
                    LayoutCombo.IsEnabled = true;
                    AddFileButton.IsEnabled = true;
                    break;
                case 1:                
                    selectedLocation_ = DisplayLocation.DataWorkspace;
                    LayoutCombo.IsEnabled = false;
                    AddFileButton.IsEnabled = false;
                    break;
            }
            // Show this one
            if (selectedLayout_ != DisplayLayout.UninitializedEnum)
                display_.Location = selectedLocation_;                
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void IndexCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {            
            selectedIndex_ = IndexCombo.SelectedIndex;

            // Display Test Code            
            if (display_ != null)
            {
                if (selectedLayout_ != DisplayLayout.UninitializedEnum)
                {
                    // Get The Views 
                    var view1_ = display_.GetDisplay(selectedLocation_, selectedIndex_);

                    // Could be empty data docs
                    if (view1_.DisplaySources.Count > 0)
                        BuildDisplayControls(view1_);
                }
            }
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void LayoutCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {         
            selectedLayout_ = (DisplayLayout)LayoutCombo.SelectedItem;

            // Show this one
            if (selectedLocation_ != DisplayLocation.UninitializedEnum)
                display_.ExperimentWorkspaceLayout = selectedLayout_;
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void LoadFileButton_Click(object sender, RoutedEventArgs e)
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            dlg.FileName    = "";                               // Default file name
            dlg.DefaultExt  = ".spe";                           // Default file extension
            dlg.Filter      = "LightField Data (*.spe)|*.spe";  // Filter files by extension

            // Show open file dialog box
            Nullable<bool> result = dlg.ShowDialog();

            // Process open file dialog box results
            if (result == true)
            {
                // Data Workspace 
                if (selectedLocation_ == DisplayLocation.DataWorkspace)
                    BuildDisplayControls(display_.DisplayFileInDataWorkspace(dlg.FileName));
                // Data Workspace Comparison + Experiment 
                else
                {
                    IDisplayViewer viewer = display_.GetDisplay(selectedLocation_, selectedIndex_);
                    viewer.Display(dlg.FileName);
                    BuildDisplayControls(viewer);
                }
            }                     
        }
        ////////////////////////////////////////////////////////////////////////////////////
        //
        ////////////////////////////////////////////////////////////////////////////////////
        private void AddFileButton_Click(object sender, RoutedEventArgs e)
        {
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            dlg.FileName    = "";                               // Default file name
            dlg.DefaultExt  = ".spe";                           // Default file extension
            dlg.Filter      = "LightField Data (*.spe)|*.spe";  // Filter files by extension

            // Show open file dialog box
            Nullable<bool> result = dlg.ShowDialog();

            // Process open file dialog box results
            if (result == true)
            {
                // Data Workspace 
                if (selectedLocation_ != DisplayLocation.DataWorkspace)                   
                {
                    // Get the viewer
                    IDisplayViewer viewer = display_.GetDisplay(selectedLocation_, selectedIndex_);
                   
                    // Must be a graph to add source
                    viewer.DisplayType = DisplayType.Graph;

                    // Only support a maximum of 5 sources
                    if (viewer.DisplaySources.Count < 5)
                    {
                        // Create the source and add it 
                        IDisplaySource source = display_.Create(dlg.FileName);
                        viewer.Add(source);
                    }
                }
            }                     
        }
        ////////////////////////////////////////////////////////////////////////////////////
        // Close the window
        ////////////////////////////////////////////////////////////////////////////////////
        private void DoneButton_Click(object sender, RoutedEventArgs e)
        {
            // Close the dialog
            Close();
        }
    }
}
