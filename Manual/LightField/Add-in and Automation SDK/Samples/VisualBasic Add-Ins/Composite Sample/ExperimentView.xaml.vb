'Interaction logic for ExperimentView.xaml
Public Class ExperimentView

    Public example_ As CompositeSample

    Public Sub New(ByVal sample As CompositeSample)
        InitializeComponent()
        example_ = sample
    End Sub

    Private Function Conversion(ByVal box As System.Windows.Controls.ComboBox) As Nullable(Of Boolean)
        Dim retVal As Nullable(Of Boolean) = False
        Dim selection As String = box.Text

        If selection = "NULL" Then
            retVal = Nothing
        ElseIf selection = "TRUE" Then
            retVal = True
        End If
        Return retVal
    End Function

    Private Sub UpdateButton_Click(sender As System.Object, e As System.Windows.RoutedEventArgs)
        'Menu
        example_.Menu = New Component(MenuTitle.Text, MenuTip.Text, MenuExec.IsChecked, Conversion(MenuToggle), MenuVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.Menu)

        'App Toolbar
        example_.AppToolBar = New Component(AppTitle.Text, AppTip.Text, AppExec.IsChecked, Conversion(AppToggle), AppVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.ApplicationToolBar)

        'Data Tool Bar
        example_.DataToolBar = New Component(DataTitle.Text, DataTip.Text, DataExec.IsChecked, Conversion(DataToggle), DataVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.DataToolBar)

        'Experiment
        example_.ExperimentSetting = New Component(ExpTitle.Text, ExpTip.Text, ExpExec.IsChecked, Conversion(ExpToggle), ExpVis.IsChecked, PrincetonInstruments.LightField.AddIns.UISupport.ExperimentSetting)

        example_.DingEvent()
    End Sub
End Class
