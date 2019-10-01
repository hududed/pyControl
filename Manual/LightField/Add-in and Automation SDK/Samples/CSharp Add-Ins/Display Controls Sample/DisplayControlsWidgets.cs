using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace LightFieldAddInSamples
{
    // Enum of Control Types To Be Dynamically Constructed
    public enum ControlWidgetType
    {
        SliderBar,
        CheckBox,
        EditBox,
        ComboBox,
        ReadOnlyEditBox,
        Button,
        Expander,
        SubExpander,
        SubEnd
    };
    // Control Widget class
    public class ControlWidget
    {
        string name_;
        object value_;
        ControlWidgetType type_;

        double sliderMin_;
        double sliderMax_;

        // The real physical control
        public object ControlItem { get; set; }

        // Constructor Non-Slider
        public ControlWidget(string name,
                                    ControlWidgetType type,
                                    object value)
        {
            name_ = name;
            type_ = type;
            value_ = value;
        }
        // Constructor Slider
        public ControlWidget(string name,
                             ControlWidgetType type,
                             object value,
                             double min,
                             double max)
        {
            name_ = name;
            type_ = type;
            value_ = value;
            sliderMin_ = min;
            sliderMax_ = max;
        }
        public ControlWidgetType GetWidgetType() { return type_; }
        public string GetName() { return name_; }
        public object GetValue() { return value_; }
        public double SliderMin() { return sliderMin_; }
        public double SliderMax() { return sliderMax_; }
    }
}
