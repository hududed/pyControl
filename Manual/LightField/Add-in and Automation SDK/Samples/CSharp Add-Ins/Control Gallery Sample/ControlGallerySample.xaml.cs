using System;
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
using System.Windows.Threading;
using System.Timers;

using System.Collections.ObjectModel;


namespace LightFieldAddInSamples.Control_Gallery_Sample
{
    /// <summary>
    /// Interaction logic for ControlGallerySample.xaml
    /// </summary>
    /// 
    public class BookData
    {
        public string Book { get; set; }
        public string Author { get; set; }
        public string Year { get; set; }
    }

    public partial class ControlGallerySample : UserControl
    {
        int progress1Value_ = 0;
       
        DispatcherTimer timer_;
        ObservableCollection<BookData> _BookCollection = new ObservableCollection<BookData>();

        public ControlGallerySample()
        {
            _BookCollection.Add(new BookData{
                  Book   = "The Sun Also Rises", 
                  Author = "Earnest Hemingway", 
                  Year   = "1926" });
            _BookCollection.Add(new BookData{
                  Book   = "Tom Sawyer",
                  Author = "Mark Twain",
                  Year   = "1885"
            });
               
            InitializeComponent();

            // Fill in the combo box so we can really see it.
            comboBox.Items.Add("Fred");
            comboBox.Items.Add("Susan");
            comboBox.Items.Add("Alice");
            comboBox.Items.Add("Rupert");

            // List Box
            listBox.Items.Add("Dasher");
            listBox.Items.Add("Dancer");
            listBox.Items.Add("Prancer");
            listBox.Items.Add("Vixen");
            listBox.Items.Add("Comet");
            listBox.Items.Add("Cupid");
            listBox.Items.Add("Donner");
            listBox.Items.Add("Blitzen");            
            listBox.Items.Add("Rudolf");

            progressBar1.Minimum = 0;
            progressBar1.Maximum = 19;
            progressBar2.IsIndeterminate = true;

            timer_ = new DispatcherTimer();
            timer_.Interval = new TimeSpan(0, 0, 0, 0, 200);
            timer_.Tick += new EventHandler(timer_Tick);
            timer_.Start();            
        }

        public ObservableCollection<BookData> BookCollection
        { get { return _BookCollection; } }

        private void AddRow_Click(object sender, RoutedEventArgs e)
        {
            _BookCollection.Add(new BookData
            {
                Book = "A New Book",
                Author = "A New Author",
                Year = "A New Year"
            });
        }

        void  timer_Tick(object sender, EventArgs e)      
        {
            progressBar1.Value = progress1Value_;
            progress1Value_++;
            if (progress1Value_ > progressBar1.Maximum)
                progress1Value_ = (int)progressBar1.Minimum;
        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {                                  
        }
    }
}
