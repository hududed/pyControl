import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash_daq import DarkThemeProvider as DarkThemeProvider
from dash.dependencies import State, Input, Output
from blinkstick import blinkstick

# Convert Hex to RGB
def hex_convert_rgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2 ,4))

app = dash.Dash()

server = app.server

app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True


# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
]

# Blinkstick Open Port
bstick = blinkstick.find_first()


for css in external_css:
    app.css.append_css({"external_url": css})

theme_choose = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                daq.ToggleSwitch(
                    id="toggleTheme",
                    style={"position": "absolute", "transform": "translate(-50%, 20%)"},
                    size=25,
                )
            ],
            id="toggleDiv",
            style={"width": "fit-content", "margin": "0 auto"},
        ),
        html.Div(id="page-content"),
    ]
)

base_layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": ""},
            children=[
                html.H2("Dash DAQ: Blinkstick Control Panel"),
                html.A(
                    html.Img(
                        src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png"
                    ),
                    href="http://www.dashdaq.io",
                ),
            ],
            className="banner",
        ),
        html.Div(
            [
                html.H2(
                    "LED PANEL",
                    id="LED-PANEL",
                    style={"textAlign": "center", "marginTop": "5%", "color": ""},
                ),
                html.Br(),
            ]
        ),
        html.Div(
            [
                daq.Indicator(
                    id="led-1",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-2",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-3",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-4",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-5",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-6",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-7",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
                daq.Indicator(
                    id="led-8",
                    label="",
                    labelPosition="bottom",
                    value=True,
                    className="one columns",
                    style={"textAlign": "center", "width": "0%", "marginRight": "2%"},
                    color="#72D1F8",
                    width=16,
                    height=40,
                ),
            ],
            className="row",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
        html.Br(),
        html.Div(
            [
                daq.PowerButton(
                    id="power",
                    label="On/Off",
                    labelPosition="top",
                    on=True,
                    className="one columns",
                    style={"width": "8%", "paddingBottom": "1%"},
                    color="",
                ),
                daq.NumericInput(
                    id="led-select",
                    label="Led Select",
                    className="one columns",
                    style={
                        "width": "5%",
                        "textAlign": "center",
                        "marginLeft": "3%",
                        "paddingBottom": "1%",
                    },
                    value=0,
                    max=8,
                    disabled=False,
                ),
                daq.BooleanSwitch(
                    id="all-switch",
                    on=False,
                    label="All",
                    vertical=True,
                    labelPosition="top",
                    className="one columns",
                    style={"width": "3%"},
                    disabled=False,
                    color="",
                ),
                daq.BooleanSwitch(
                    id="rainbow-switch",
                    on=False,
                    label="Rainbow",
                    vertical=True,
                    labelPosition="top",
                    className="one columns",
                    style={"width": "6%"},
                    disabled=False,
                    color="",
                ),
                html.Div(
                    [
                        daq.ColorPicker(
                            id="color-picker",
                            size=164,
                            value={"hex": "#19AC51"},
                            label="Color Picker",
                            style={"textAlign": "right"},
                        )
                    ],
                    className="two columns",
                    style={"width": "18.333%"},
                ),
            ],
            className="row",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
        html.Br(),
        html.P(
            "LED Slider",
            style={"textAlign": "left", "marginBottom": "1%", "paddingLeft": "11.5%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        daq.Slider(
                            id="led-slide",
                            color="",
                            handleLabel={"showCurrentValue": "True", "label": "LED"},
                            size=638,
                            min=0,
                            max=8,
                            marks={
                                "0": "OFF",
                                "1": "1",
                                "2": "2",
                                "3": "3",
                                "4": "4",
                                "5": "5",
                                "6": "6",
                                "7": "7",
                                "8": "8",
                            },
                            value=0,
                            disabled=False,
                        )
                    ],
                    className="row",
                    style={"width": "75%"},
                )
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "marginTop": "5%",
            },
        ),
        html.Div(
            children=[
                html.Div(id="color-send"),
                html.Div(id="color-individual"),
                html.Div(id="color-off"),
                html.Div(id="color-rainbow"),
                html.Div(id="color-slide"),
                html.Div(id="color-one"),
                html.Div(id="color-two"),
                html.Div(id="color-return"),
            ],
            style={"visibility": "hidden"},
        ),
    ],
    style={
        "padding": "0px 10px 10px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "850",
        "height": "685",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
    },
)

light_theme = html.Div(id="light-theme", children=[base_layout])

dark_theme = DarkThemeProvider(
    [
        html.Link(
            href="https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/94fdb056/dash-daq-dark.css",
            rel="stylesheet",
        ),
        html.Div([base_layout]),
    ]
)

app.layout = theme_choose

# Theme Toggle
@app.callback(
    Output("toggleTheme", "value"), 
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/dark":
        return True
    else:
        return False


@app.callback(
    Output("page-content", "children"), 
    [Input("toggleTheme", "value")]
)
def page_layout(value):
    if value:
        return dark_theme
    else:
        return light_theme


# Color Picker LED
@app.callback(
    Output('color-send', 'children'),
    [Input('color-picker', 'value'),
     Input("all-switch", 'on')]
)

def colorpick_all(value, all_switch):
    if all_switch == True:
        value = value["hex"]
        hex_color = hex_convert_rgb(value)
        r = int(hex_color[0])
        b = int(hex_color[1])
        g = int(hex_color[2])
        for i in range(0, 8):
            bstick.set_color(0, i, r, b, g)
        return value


# Led Select Color Picker
@app.callback(
    Output('color-individual', 'children'),
    [Input('color-picker', 'value'),
     Input("led-select", 'value')]
)
def colorpick_individual(value, led_select):
    if led_select >= 1:
        value = value["hex"]
        hex_color = hex_convert_rgb(value)
        r = int(hex_color[0])
        b = int(hex_color[1])
        g = int(hex_color[2])
        led_select = led_select - 1  
        bstick.set_color(0, led_select, r, b, g)
        return value


# Led Rainbow Switch
@app.callback(
    Output('color-rainbow', 'children'),
    [Input("rainbow-switch", "on")]
)

def rainbow_switch(rainbow):
    if rainbow == True:
        bstick.set_color(0, 0, 255, 0, 0)
        bstick.set_color(0, 1, 226, 87, 30)
        bstick.set_color(0, 2, 255, 127, 0)
        bstick.set_color(0, 3, 255, 249, 3)
        bstick.set_color(0, 4, 0, 255, 0)
        bstick.set_color(0, 5, 0, 0, 255)
        bstick.set_color(0, 6, 75, 0, 130)
        bstick.set_color(0, 7, 255, 255, 255)   


# Slider Led
@app.callback(
    Output('color-slide', 'children'),
    [Input('led-slide', 'value'),
    Input('color-picker', 'value')],
    [State('all-switch', 'on'),
     State("rainbow-switch", "on"),
     State("led-select", "value")]
)
def led_slide(
    slide, 
    value, 
    all_switch, 
    rainbow_switch, 
    led_select
    ):

    if all_switch == False and rainbow_switch == False and led_select == 0:
        value = value["hex"]
        hex_color = hex_convert_rgb(value)
        r = int(hex_color[0])
        b = int(hex_color[1])
        g = int(hex_color[2])
        
        for i in range (slide, 9):
            bstick.set_color(0, i, 0, 0, 0)
        for i in range (0, slide):
            bstick.set_color(0, i, r, b, g) 
        return value
    


# Default Off
@app.callback(
    Output('color-off', 'children'),
    [Input('rainbow-switch', 'on'),
     Input('all-switch', 'on'),
     Input('led-select', 'value'),
     Input('led-slide', 'value')],
     [State('power', 'on')]
)
def color_off(
    rainbow_switch, 
    all_switch, 
    led_select, 
    led_slide, 
    power
    ):

    if rainbow_switch == False and all_switch == False and led_select == 0 and led_slide == 0:
        bstick.set_color(0, 0, 0, 0, 0)
        bstick.set_color(0, 1, 0, 0, 0)
        bstick.set_color(0, 2, 0, 0, 0)
        bstick.set_color(0, 3, 0, 0, 0)
        bstick.set_color(0, 4, 0, 0, 0)
        bstick.set_color(0, 5, 0, 0, 0)
        bstick.set_color(0, 6, 0, 0, 0)
        bstick.set_color(0, 7, 0, 0, 0)


#Color Picker
@app.callback(
    Output("led-slide", "color"),
    [Input("color-picker", "value")]
)
def color_picker(value):
    value = value["hex"]
    return value


@app.callback(
    Output("power", "color"),
    [Input("color-picker", "value")]
)
def color_picker(value):
    value = value["hex"]
    return value


@app.callback(
    Output("rainbow-switch", "color"),
    [Input("color-picker", "value")]
)
def color_picker(value):
    value = value["hex"]
    return value


@app.callback(
    Output("all-switch", "color"),
    [Input("color-picker", "value")]
)
def color_picker(value):
    value = value["hex"]
    return value


@app.callback(
    Output("color-return", "children"),
    [Input("color-picker", "value")]
)
def color_picker(value):
    value = value["hex"]
    return value


@app.callback(
    Output("container", "style"),
    [Input("color-return", "children")]
)
def color_picker(color):
    style = {"background-color": ""}
    style["background-color"] = color
    return style


@app.callback(
    Output("LED-PANEL", "style"),
    [Input("color-return", "children")]
)
def color_picker(color):
    style = {"color": "", "textAlign":"center", "marginTop":"5%"}
    style["color"] = color
    return style


# LED Color Change All
@app.callback(
    Output('led-1', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]
)


def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 0, 0, 0, 0)
        return "#ACC7D9"
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#FF0000'
    elif led_slide >= 1:
        return color_slide
    elif led_select == 1:
        return value_individual
    

@app.callback(
    Output('led-2', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 1, 0, 0, 0)
        return "#ACC7D9"
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#E2571E'
    elif led_slide >= 2:
        return color_slide    
    elif led_select == 2:
        return value_individual
    

@app.callback(
    Output('led-3', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 2, 0, 0, 0)
        return "#ACC7D9"
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#FF7F00'
    elif led_slide >= 3:
        return color_slide    
    elif led_select == 3:
        return value_individual


@app.callback(
    Output('led-4', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 3, 0, 0, 0)
        return "#ACC7D9"  
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#FFF903'
    elif led_slide >= 4:
        return color_slide    
    elif led_select == 4:
        return value_individual


@app.callback(
    Output('led-5', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual,
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 4, 0, 0, 0)
        return "#ACC7D9"
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#00FF00'
    elif led_slide >= 5:
        return color_slide    
    elif led_select == 5:
        return value_individual


@app.callback(
    Output('led-6', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 5, 0, 0, 0)
        return "#ACC7D9"
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#0000FF'
    elif led_slide >= 6:
        return color_slide    
    elif led_select == 6:
        return value_individual


@app.callback(
    Output('led-7', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 6, 0, 0, 0)
        return "#ACC7D9"    
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#8B00FF'
    elif led_slide >= 7:
        return color_slide    
    elif led_select == 7:
        return value_individual


@app.callback(
    Output('led-8', 'color'),
    [Input('color-send', 'children'),
     Input('color-individual', 'children'),
     Input('power', 'on'),
     Input('rainbow-switch', 'on'),
     Input('led-slide', 'value'),
     Input('all-switch', 'on')],
     [State("led-select", 'value'),
     State('color-slide', 'children')]

)
def colorpick(
    value_all, 
    value_individual, 
    power, 
    rainbow, 
    led_slide, 
    all_switch, 
    led_select, 
    color_slide
    ):

    if power == False:
        bstick.set_color(0, 7, 0, 0, 0)
        return "#ACC7D9" 
    elif all_switch == True:
        return value_all
    elif rainbow == True:
        return '#EEE7E7'
    elif led_slide >= 8:
        return color_slide    
    elif led_select == 8:
        return value_individual 


# Disabler
@app.callback(
    Output('all-switch', 'on'),
    [Input('led-slide', 'value'),
    Input("led-select", 'value')]
)
def disabler(led_slide, led_select):
        return False


@app.callback(
    Output('rainbow-switch', 'on'),
    [Input('led-slide', 'value'),
    Input("led-select", 'value')]
)
def disabler(led_slide, led_select):
        return False


@app.callback(
    Output('all-switch', 'disabled'),
    [Input('led-slide', 'value'),
    Input("led-select", 'value'),
    Input("rainbow-switch", 'on')]
)
def disabler(led_slide, led_select, rainbow_switch):
    if led_slide >= 1 or led_select >= 1 or rainbow_switch == True:
        return True
    else:
        return False


@app.callback(
    Output('rainbow-switch', 'disabled'),
    [Input('led-slide', 'value'),
    Input("led-select", 'value'),
    Input("all-switch", 'on')]
)
def disabler(led_slide, led_select, all_switch):
    if led_slide >= 1 or led_select >= 1 or all_switch == True:
        return True
    else:
        return False


@app.callback(
    Output('led-slide', 'disabled'),
    [Input('led-select', 'value')]
)
def disabler(led_select):
    if led_select >= 1:
        return True
    else:
        return False


@app.callback(
    Output('led-select', 'disabled'),
    [Input('led-slide', 'value')]
)
def disabler(led_slide):
    if led_slide >= 1:
        return True
    else:
        return False


if __name__ == "__main__":

    app.run_server(debug=False)
