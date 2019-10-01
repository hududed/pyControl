using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.IO;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Markup;

namespace LightFieldAddInSamples.Composite_Sample
{
    /// <summary>
    /// Interaction logic for ExperimentView.xaml
    /// </summary>
    public partial class ExperimentView : UserControl
    {
        CompositeSample example_;

        public ExperimentView(CompositeSample sample)
        {
            InitializeComponent();

            example_ = sample;
        }
        
        private bool? conversion(ComboBox box)
        {
            bool? retVal = false;
            string selection = box.Text;

            if (selection == "NULL")
                retVal = null;
            else if (selection == "TRUE")
                retVal = true;

            return retVal;
        }   
        private void UpdateButton_Click(object sender, RoutedEventArgs e)
        {           
            // Menu
            example_.Menu = new Component(MenuTitle.Text, MenuTip.Text, (bool)MenuExec.IsChecked, conversion(MenuToggle), (bool)MenuVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.Menu);
            
            // App Toolbar
            example_.AppToolBar = new Component(AppTitle.Text, AppTip.Text, (bool)AppExec.IsChecked, conversion(AppToggle), (bool)AppVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.ApplicationToolBar);
            
            // Data Tool Bar
            example_.DataToolBar = new Component(DataTitle.Text, DataTip.Text, (bool)DataExec.IsChecked, conversion(DataToggle), (bool)DataVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.DataToolBar);
            
            // Experiment
            example_.ExperimentSetting = new Component(ExpTitle.Text, ExpTip.Text, (bool)ExpExec.IsChecked, conversion(ExpToggle), (bool)ExpVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.ExperimentSetting);

            example_.DingEvent();                                               
        }       
    }
}
