using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Windows;

namespace Custom_Acquire_Sample_Automation_
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {        
        protected override void OnSessionEnding(SessionEndingCancelEventArgs e)
        {
            // Cancelling because we can't guarantee proper cleanup of automated LF's 
            // unless the automating application is closed directly.
            e.Cancel = true;
            base.OnSessionEnding(e);
        }
    }
}
