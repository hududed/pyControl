Imports System.Windows.Threading
Imports System.Timers
Imports System.Collections.ObjectModel

'Interaction logic for ControlGallerySample.xaml
Public Class GalleryControlSample
    Public progress1Value_ As Integer = 0
    Public timer_ As DispatcherTimer
    Public _BookCollection As ObservableCollection(Of BookData) = New ObservableCollection(Of BookData)()

    Public Sub New()
        _BookCollection.Add(New BookData("The Sun Also Rises", "Earnest Hemingway", "1926"))
        _BookCollection.Add(New BookData("Tom Sawyer", "Mark Twain", "1885"))

        ' This call is required by the designer.
        InitializeComponent()

        ' Add any initialization after the InitializeComponent() call.
        'ComboBox
        comboBox.Items.Add("Fred")
        comboBox.Items.Add("Susan")
        comboBox.Items.Add("Alice")
        comboBox.Items.Add("Rupert")
        'ListBox
        listBox.Items.Add("Dasher")
        listBox.Items.Add("Dancer")
        listBox.Items.Add("Prancer")
        listBox.Items.Add("Vixen")
        listBox.Items.Add("Comet")
        listBox.Items.Add("Cupid")
        listBox.Items.Add("Donner")
        listBox.Items.Add("Blitzen")
        listBox.Items.Add("Rudolf")
        'ProgressBar
        progressBar1.Minimum = 0
        progressBar1.Maximum = 19
        progressBar2.IsIndeterminate = True
        'Timer
        timer_ = New DispatcherTimer()
        timer_.Interval = New TimeSpan(0, 0, 0, 0, 200)
        AddHandler timer_.Tick, AddressOf timer_Tick
        timer_.Start()
    End Sub

    Public Sub timer_Tick(ByVal sender As Object, ByVal e As EventArgs)
        progressBar1.Value = progress1Value_
        progress1Value_ += 1
        If progress1Value_ > progressBar1.Maximum Then
            progress1Value_ = progressBar1.Minimum
        End If
    End Sub

    Private Sub AddRow_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        _BookCollection.Add(New BookData("A New Book", "A New Author", "A New Year"))
    End Sub

    Private Sub button1_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)

    End Sub
     
    Public ReadOnly Property BookCollection As ObservableCollection(Of BookData)
        Get
            Return _BookCollection
        End Get
    End Property
End Class

Public Class BookData
    Private Book_ As String
    Private Author_ As String
    Private Year_ As String

    Public Sub New(ByVal book As String, ByVal author As String, ByVal year As String)
        Book_ = book
        Author_ = author
        Year_ = year
    End Sub

    Public Property Book As String
        Get
            Return Book_
        End Get
        Set(value As String)
            Book_ = value
        End Set
    End Property

    Public Property Author As String
        Get
            Return Author_
        End Get
        Set(value As String)
            Author_ = value
        End Set
    End Property

    Public Property Year As String
        Get
            Return Year_
        End Get
        Set(value As String)
            Year_ = value
        End Set
    End Property
End Class