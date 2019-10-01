'Enum of control types to be dynamically constructed
Public Enum ControlWidgetType
    SliderBar
    CheckBox
    EditBox
    ComboBox
    ReadOnlyEditBox
    Button
    Expander
    SubExpander
    SubEnd
End Enum

'ControlWidget class
Public Class ControlWidget
    Private name_ As String
    Private value_ As Object
    Private type_ As ControlWidgetType
    Private sliderMin_ As Double
    Private sliderMax_ As Double
    Private item_ As Object

    'The real physical control
    Public Property ControlItem As Object
        Get
            Return item_
        End Get
        Set(value As Object)
            item_ = value
        End Set
    End Property

    'Constructor non-slider
    Public Sub New(name As String, type As ControlWidgetType, value As Object)
        name_ = name
        type_ = type
        value_ = value
    End Sub

    'Constructor slider
    Public Sub New(name As String, type As ControlWidgetType, value As Object, min As Double, max As Double)
        name_ = name
        type_ = type
        value_ = value
        sliderMin_ = min
        sliderMax_ = max
    End Sub

    Public Function GetWidgetType() As ControlWidgetType
        Return type_
    End Function

    Public Function GetName() As String
        Return name_
    End Function

    Public Function GetValue() As Object
        Return value_
    End Function

    Public Function SliderMin() As Double
        Return sliderMin_
    End Function

    Public Function SliderMax() As Double
        Return sliderMax_
    End Function
End Class