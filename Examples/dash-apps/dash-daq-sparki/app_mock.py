import time
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import json
import serial



app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True



def rgb_convert_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    "https://rawgit.com/matthewchan15/dash-sparki-icon-sheet/master/css/sparkibot.css",
]


for css in external_css:
    app.css.append_css({"external_url": css})


app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#119DFF"},
            children=[
                html.H2("Dash DAQ: Sparki Control Panel"),
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
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5(
                                    "LED Color",
                                    id="led-title",
                                    style={
                                        "textAlign": "center", 
                                        "paddingTop": "5%"
                                    },
                                ),
                                html.Div(
                                    [
                                        daq.ColorPicker(
                                            id="led-control",
                                            label=" ",
                                            size=130,
                                            value={
                                                "rgb": {
                                                    "r": 17,
                                                    "g": 157,
                                                    "b": 255,
                                                    "a": 1,
                                                }
                                            },
                                        )
                                    ]
                                ),
                            ],
                            style={
                                "border": "1px solid #2a3f5f",
                                "border-radius": "5px",
                                "marginBottom": "5%",
                                "paddingBottom": "19%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H5(
                                            "Noise",
                                            id="noise-title",
                                            style={
                                                "textAlign": "center",
                                                "paddingTop": "5%",
                                                "paddingBottom": "3%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                daq.Knob(
                                                    id="knob-pitch",
                                                    label=" ",
                                                    size=100,
                                                    value=261,
                                                    color="#FF5E5E",
                                                    max=440,
                                                    min=261,
                                                    scale={
                                                        "custom": {
                                                            "440": "A",
                                                            "415": "G#",
                                                            "392": "G",
                                                            "370": "F#",
                                                            "349": "F",
                                                            "330": "E",
                                                            "311": "D#",
                                                            "294": "D",
                                                            "277": "C#",
                                                            "261": "C",
                                                        }
                                                    },
                                                ),
                                                daq.StopButton(
                                                    id="stop-beep",
                                                    buttonText="Beep",
                                                    style={
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center",
                                                        "paddingBottom": "19.5%",
                                                    },
                                                    n_clicks=0,
                                                    size=100,
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "border": "1px solid #2a3f5f",
                                        "border-radius": "5px",
                                        "paddingBottom": "5%",
                                    },
                                )
                            ]
                        ),
                    ],
                    className="three columns",
                    style={"width": "18%", 
                           "marginLeft": "3.5%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5(
                                    "Motion",
                                    id="motion-title",
                                    style={
                                        "textAlign": "center", 
                                        "paddingTop": "3%"
                                    },
                                ),
                                daq.ToggleSwitch(
                                    id="free-box",
                                    label=["Box", "Free"],
                                    color="#FF5E5E",
                                    value=True,
                                    size=32,
                                    style={
                                        "marginBottom": "-1%",
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                daq.Joystick(
                                                    id="joystick", angle=0, force=0
                                                )
                                            ],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [
                                                daq.Knob(
                                                    id="ultrasonic-angle",
                                                    label=" ",
                                                    value=0,
                                                    size=60,
                                                    color="#FF5E5E",
                                                    min=0,
                                                    max=180,
                                                    scale={
                                                        "custom": {
                                                            "0": 0,
                                                            "90": 90,
                                                            "180": 180,
                                                        }
                                                    },
                                                )
                                            ],
                                            className="four columns",
                                        ),
                                    ],
                                    className="row",
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "marginBottom": "-6%",
                                    },
                                ),
                                html.H6("Gripper", style={"textAlign": "center"}),
                                html.Div(
                                    [
                                        daq.StopButton(
                                            id="start-grip",
                                            buttonText="Open",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                            className="three columns",
                                            size=65,
                                            n_clicks=0,
                                        ),
                                        daq.StopButton(
                                            id="close-grip",
                                            buttonText="Close",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                            className="three columns",
                                            size=65,
                                            n_clicks=0,
                                        ),
                                        daq.StopButton(
                                            id="stop-grip",
                                            buttonText="Stop",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                            className="three columns",
                                            size=65,
                                            n_clicks=1,
                                        ),
                                    ],
                                    className="row",
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "marginBottom": "3%",
                                        "paddingBottom": "1%",
                                    },
                                ),
                            ],
                            style={
                                "border": "1px solid #2a3f5f",
                                "border-radius": "5px",
                                "marginBottom": "3%",
                            },
                        ),
                        html.Div(
                            [
                                html.H5(
                                    "Ultrasonic Data",
                                    id="data-title",
                                    style={"textAlign": "center"},
                                ),
                                daq.ToggleSwitch(
                                    id="capture-sweep",
                                    label=["Capture", "Sweep"],
                                    value=True,
                                    color="#FF5E5E",
                                    size=32,
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                    },
                                ),
                                html.Div(
                                    id="capture",
                                    children=[
                                        html.Div(
                                            [
                                                daq.LEDDisplay(
                                                    id="ultra-sonic-data",
                                                    label=" ",
                                                    value="0.00",
                                                    size=35,
                                                ),
                                                html.Div(
                                                    [
                                                        html.H5(
                                                            "cm",
                                                            id="unit-holder",
                                                            style={
                                                                "border-radius": "3px",
                                                                "border-width": "5px",
                                                                "border": "1px solid rgb(216, 216, 216)",
                                                                "font-size": "46px",
                                                                "color": "#2a3f5f",
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                                "width": "110%",
                                                                "marginRight": "2%",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "paddingTop": "2.5%",
                                                        "paddingLeft": "1%",
                                                        "width": "22%",
                                                    },
                                                ),
                                            ],
                                            className="row",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "paddingRight": "3%",
                                                "marginTop": "9%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                daq.Indicator(
                                                    id="ultrasonic-light",
                                                    color="#EF553B",
                                                    label="Detected",
                                                    value=True,
                                                    style={
                                                        "marginTop": "5%",
                                                        "paddingBottom": "8%",
                                                        "width": "31%",
                                                    },
                                                ),
                                                daq.StopButton(
                                                    id="ultrasonic-capture",
                                                    buttonText="Capture",
                                                    n_clicks=0,
                                                ),
                                            ],
                                            className="row",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "position": "absolute",
                                        "width": "100%",
                                        "height": "100%",
                                    },
                                ),
                                html.Div(
                                    id="sweep",
                                    style={
                                        "paddingTop": "1%",
                                        "position": "absolute",
                                        "width": "100%",
                                        "height": "100%",
                                    },
                                    children=[
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H6(
                                                            "Sweep Data (CM)",
                                                            style={
                                                                "textAlign": "center"
                                                            },
                                                        ),
                                                        dcc.Graph(
                                                            id="sweep-graph",
                                                            style={
                                                                "width": "310px",
                                                                "height": "210px",
                                                            },
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                            figure={
                                                                "data": [
                                                                    go.Scatterpolar(
                                                                        theta=[""],
                                                                        r=[""],
                                                                        mode="markers",
                                                                        marker={
                                                                            "size": 6
                                                                        },
                                                                    )
                                                                ],
                                                                "layout": go.Layout(
                                                                    polar={
                                                                        "sector": [
                                                                            0,
                                                                            180,
                                                                        ],
                                                                        "radialaxis": {
                                                                            "visible": False
                                                                        },
                                                                    },
                                                                    margin={
                                                                        "l": 40,
                                                                        "b": 50,
                                                                        "t": 40,
                                                                        "r": 40,
                                                                    },
                                                                ),
                                                            },
                                                        ),
                                                    ]
                                                ),
                                                daq.StopButton(
                                                    id="ultrasonic-sweep",
                                                    buttonText="Sweep",
                                                    n_clicks=0,
                                                    size=55,
                                                    style={
                                                        "position": "absolute",
                                                        "top": "16px",
                                                        "left": "265px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                        )
                                    ],
                                ),
                            ],
                            style={
                                "paddingTop": "3%",
                                "width": "100%",
                                "border": "1px solid #2a3f5f",
                                "border-radius": "5px",
                                "position": "relative",
                                "paddingBottom": "80%",
                            },
                        ),
                    ],
                    className="four columns",
                ),
                html.Div(
                    [
                        html.Div(
                            id="sparki-box",
                            children=[
                                html.H5(
                                    " ",
                                    id="sparki-icon",
                                    style={
                                        "font-size": "50px",
                                        "color": "",
                                        "paddingLeft": "10px",
                                        "paddingTop": "10px",
                                    },
                                    className="icon-sparki",
                                )
                            ],
                            style={
                                "border-width": "5px",
                                "border": "1px solid #2a3f5f",
                                "height": "350px",
                                "width": "400px",
                                "position": "absolute",
                            },
                        ),
                        html.Div(
                            id="sparki-arrow",
                            children=[
                                html.H5(
                                    " ",
                                    id="sparki-up",
                                    style={
                                        "font-size": "75px",
                                        "color": "#EF553B",
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "marginTop": "4%",
                                    },
                                    className="icon-up",
                                ),
                                html.Div(
                                    [
                                        html.H5(
                                            " ",
                                            id="sparki-left",
                                            style={
                                                "font-size": "75px",
                                                "color": "#EF553B",
                                            },
                                            className="icon-left four columns",
                                        ),
                                        html.H5(
                                            " ",
                                            id="sparki-icon-arrow",
                                            style={"font-size": "80px", "color": ""},
                                            className="icon-sparki four columns",
                                        ),
                                        html.H5(
                                            " ",
                                            id="sparki-right",
                                            style={
                                                "font-size": "75px",
                                                "color": "#EF553B",
                                            },
                                            className="icon-right four columns",
                                        ),
                                    ],
                                    className="row",
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "marginTop": "7%",
                                        "marginLeft": "9%",
                                    },
                                ),
                                html.H5(
                                    " ",
                                    id="sparki-down",
                                    style={
                                        "font-size": "75px",
                                        "color": "#EF553B",
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                    },
                                    className="icon-down",
                                ),
                            ],
                            style={
                                "height": "350px",
                                "width": "400px",
                                "position": "absolute",
                                "border": "1px solid #2a3f5f",
                                "border-radius": "5px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Textarea(
                                    id="object-detection",
                                    placeholder="",
                                    value=" ",
                                    style={
                                        "width": "93%",
                                        "height": "291px",
                                        "border": "1px solid #2a3f5f",
                                        "border-radius": "5px",
                                        "position": "absolute",
                                        "top": "363px",
                                    },
                                )
                            ]
                        ),
                    ],
                    className="five columns",
                    style={"position": "relative"},
                ),
            ],
            className="row",
            style={"marginTop": "4%"},
        ),
        html.Div(
            [
                html.Div(id="command-string"),
                html.Div(id="color-hold"),
                html.Div(id="beep-hold"),
                html.Div(id="grip-hold"),
                html.Div(id="motor-hold"),
                html.Div(id="case-hold"),
                html.Div(id="grip-start"),
                html.Div(id="grip-close"),
                html.Div(id="grip-stop"),
                html.Div(id="up-move"),
                html.Div(id="down-move"),
                html.Div(id="left-move"),
                html.Div(id="right-move"),
                html.Div(id="stop-move"),
                html.Div(id="ultrasonic-hold"),
                html.Div(id="free-box-hold"),
                html.Div(id="sweep-capture-hold"),
                html.Div(id="indv-ultra"),
                html.Div(id="capture-hold"),
                html.Div(id="sweep-hold"),
                html.Div(id="head-hold"),
            ],
            style={"visibility": "hidden"},
        ),
    ],
    style={
        "padding": "0px 10px 0px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "1100",
        "height": "825",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
        "position": "absolute",
        "top": "0",
        "bottom": "0",
        "left": "0",
        "right": "0",
    },
)


# Sweep Capture Hold Value
@app.callback(
    Output("sweep-capture-hold", "children"), 
    [Input("capture-sweep", "value")]
)
def sweep_capture(value):
    if value:
        return "1"  # Sweep
    else:
        return "2"  # Capture

# Free Box Hold Value
@app.callback(
    Output("free-box-hold", "children"), 
    [Input("free-box", "value")]
)
def free_box(value):
    if value:
        return "2"  # Free
    else:
        return "1"  # Box


# Sweep and Capture Boolean Switch
@app.callback(
    Output("capture", "style"),
    [Input("capture-sweep", "value")],
    [State("capture", "style")]
)
def capture_components(value, style):
    if value:
        style["visibility"] = "hidden"
        style["zIndex"] = "-10"
    else:
        style["visibility"] = "visible"
        style["zIndex"] = "20"
    return style


@app.callback(
    Output("sweep", "style"),
    [Input("capture-sweep", "value")],
    [State("sweep", "style")]
)
def sweep_components(value, style):
    if value:
        style["visibility"] = "visible"
        style["zIndex"] = "20"
    else:
        style["visibility"] = "hidden"
        style["zIndex"] = "-10"
    return style


# Box and Free Boolean Switch
@app.callback(
    Output("sparki-box", "style"),
    [Input("free-box", "value")],
    [State("sparki-box", "style")]
)
def sparki_box(value, style):
    if value:
        style["visibility"] = "hidden"
    else:
        style["visibility"] = "visible"
    return style


@app.callback(
    Output("sparki-arrow", "style"),
    [Input("free-box", "value")],
    [State("sparki-arrow", "style")]
)
def sparki_arrow(value, style):
    if value:
        style["visibility"] = "visible"
    else:
        style["visibility"] = "hidden"
    return style


# Banner Color Select Color Picker
@app.callback(
    Output("container", "style"), 
    [Input("led-control", "value")]
)
def color_sparki(RGB_color):
    r = RGB_color["rgb"]["r"]
    g = RGB_color["rgb"]["g"]
    b = RGB_color["rgb"]["b"]
    hex_color = rgb_convert_hex(r, g, b)
    return {"background-color": hex_color}

# Pick Sparki's Color With Color Picker
@app.callback(
    Output("sparki-icon-arrow", "style"),
    [Input("led-control", "value")],
    [State("sparki-icon-arrow", "style")],
)
def color_sparki(RGB_color, style):
    r = RGB_color["rgb"]["r"]
    g = RGB_color["rgb"]["g"]
    b = RGB_color["rgb"]["b"]
    hex_color = rgb_convert_hex(r, g, b)
    style["color"] = hex_color
    return style


# Button Timestamp (Know which button is pressed last)
@app.callback(
    Output("beep-hold", "children"), 
    [Input("stop-beep", "n_clicks")]
)
def case_beep(beep_case):
    if beep_case < 1:
        return 0
    return time.time()


@app.callback(
    Output("grip-start", "children"), 
    [Input("start-grip", "n_clicks")]
)
def grip_start(grip):
    return time.time()


@app.callback(
    Output("grip-close", "children"), 
    [Input("close-grip", "n_clicks")]
)
def grip_close(grip):
    return time.time()


@app.callback(
    Output("grip-stop", "children"), 
    [Input("stop-grip", "n_clicks")]
)
def grip_close(grip):
    return time.time()


@app.callback(
    Output("stop-move", "children"),
    [Input("joystick", "force")],
    [State("joystick", "angle")]
)
def move_right(move, angle):
    if move == 0:
        return time.time()
    return 0.0


@app.callback(
    Output("up-move", "children"), 
    [Input("joystick", "angle")]
)
def move_up(move):
    if move < 135 and move > 45:
        return time.time()
    return 0.0


@app.callback(
    Output("down-move", "children"), 
    [Input("joystick", "angle")]
)
def move_down(move):
    if move < 315 and move > 225:
        return time.time()
    return 0.0


@app.callback(
    Output("left-move", "children"), 
    [Input("joystick", "angle")]
)
def move_left(move):
    if move > 135 and move < 225:
        return time.time()
    return 0.0


@app.callback(
    Output("right-move", "children"), 
    [Input("joystick", "angle")]
)
def move_right(move):
    if move < 45 or move > 345:
        return time.time()
    return 0.0


# Based on Button Time Stamp Select Button Pressed Last
@app.callback(
    Output("motor-hold", "children"),
    [Input("up-move", "children"),
    Input("left-move", "children"),
    Input("right-move", "children"),
    Input("down-move", "children"),
    Input("stop-move", "children")]
)
def case_motor(
    motor_case_up, 
    motor_case_down, 
    motor_case_left, 
    motor_case_right, 
    motor_case_stop
):
    return time.time()


@app.callback(
    Output("grip-hold", "children"),
    [Input("start-grip", "n_clicks"),
    Input("close-grip", "n_clicks"),
    Input("stop-grip", "n_clicks")]
)
def case_gripper(grip_case, close_case, stop_case):
    return time.time()


@app.callback(
    Output("color-hold", "children"), 
    [Input("led-control", "value")]
)
def case_LED(color_case):
    return time.time()


@app.callback(
    Output("ultrasonic-hold", "children"),
    [Input("ultrasonic-capture", "n_clicks"), 
    Input("ultrasonic-sweep", "n_clicks")]
)
def ultrasonic_case(capture, sweep):
    return time.time()


@app.callback(
    Output("indv-ultra", "children"), 
    [Input("ultrasonic-angle", "value")]
)
def ultrasonic_move_head(angle):
    return time.time()


# Head Hold Value of Ultrasonic Angle
@app.callback(
    Output("head-hold", "children"), 
    [Input("ultrasonic-angle", "value")]
)
def ultrasonic_case(value):
    value = int(value)
    value = str(value)
    return value

# Case Value for Switch Case on Arduino Side
@app.callback(
    Output("case-hold", "children"),
    [Input("color-hold", "children"),
    Input("grip-hold", "children"),
    Input("beep-hold", "children"),
    Input("motor-hold", "children"),
    Input("ultrasonic-hold", "children")]
)
def case_master(color_case, grip_case, beep_case, motor_case, ultra_case):
    master_case = {
        "1": motor_case,
        "2": grip_case,
        "3": color_case,
        "4": beep_case,
        "5": ultra_case,
    }
    recent_case = max(master_case, key=master_case.get)
    return recent_case


# Sweep Ultrasonic Sensor
@app.callback(
    Output("sweep-hold", "children"), 
    [Input("ultrasonic-sweep", "n_clicks")]
)
def ultrasonic_sweep(sweep):
    df = pd.DataFrame(np.random.randint(-1, 150, size=(20, 1)), columns=list("D"))
    return df.to_json(date_format="iso", orient="split")


# Sweep Graph
@app.callback(
    Output("sweep-graph", "figure"), 
    [Input("sweep-hold", "children")]
)
def ultrasonic_sweep_graph(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient="split")
    return {
        "data": [
            go.Scatterpolar(
                theta=[
                    0,
                    10,
                    20,
                    30,
                    40,
                    50,
                    60,
                    70,
                    80,
                    90,
                    100,
                    110,
                    120,
                    130,
                    140,
                    150,
                    160,
                    170,
                    180,
                ],
                r=dff["D"],
                mode="markers",
                marker={"size": 6},
            )
        ],
        "layout": go.Layout(
            polar={"sector": [0, 180], "radialaxis": {"visible": False}},
            margin={"l": 40, "b": 50, "t": 40, "r": 40},
        ),
    }


# Ultrasonic Capture
@app.callback(
    Output("capture-hold", "children"), 
    [Input("ultrasonic-capture", "n_clicks")]
)
def ultrasonic_response(clicks):
    response = random.uniform(-1, 150)
    response = int(response)
    return response


# Ultrasonic LED Display
@app.callback(
    Output("ultra-sonic-data", "value"), 
    [Input("capture-hold", "children")]
)
def ultrasonic_display(response):
    if response == -1:
        return "999"
    elif response >= 100:
        return response
    response = float(response)
    response = "%.2f" % response
    response = f"{response:{4}.{4}}"
    response = str(response)
    return response


# Ultrasonic Light Indicator
@app.callback(
    Output("ultrasonic-light", "color"), 
    [Input("capture-hold", "children")]
)
def ultrasonic_indicator(response):
    if response == "-1":
        return "#EF553B"
    return "#00cc96"


# Based on Button Time Stamp Select Button Pressed Last
@app.callback(
    Output("command-string", "children"),
    [Input("up-move", "children"),
    Input("left-move", "children"),
    Input("down-move", "children"),
    Input("right-move", "children"),
    Input("stop-move", "children"),
    Input("grip-start", "children"),
    Input("grip-close", "children"),
    Input("grip-stop", "children"),
    Input("beep-hold", "children"),
    Input("color-hold", "children"),
    Input("ultrasonic-hold", "children"),
    Input("indv-ultra", "children")]
)
def command_string(
    move_up,
    move_left,
    move_down,
    move_right,
    move_stop,
    grip_open,
    grip_close,
    grip_stop,
    beep_hold,
    color_hold,
    ultra_hold,
    ultra_ind,
):
    master_command = {
        "UP": move_up,
        "LEFT": move_left,
        "RIGHT": move_right,
        "DOWN": move_down,
        "STOPM": move_stop,
        "OPEN": grip_open,
        "CLOSE": grip_close,
        "STOP": grip_stop,
        "BEEP": beep_hold,
        "LED": color_hold,
        "ULTRA": ultra_hold,
        "ULTRAF": ultra_ind,
    }
    recent_command = max(master_command, key=master_command.get)
    return recent_command


# Write Command to Sparki and Serial Monitor
@app.callback(
    Output("object-detection", "value"),
    [Input("command-string", "children"),
    Input("case-hold", "children"),
    Input("head-hold", "children")],
    [State("knob-pitch", "value"),
    State("led-control", "value"),
    State("sweep-capture-hold", "children"),
    State("free-box-hold", "children")]
)
def central_command(command, case_master, head, beep_freq, RGB_color, ultra, box):
    R = RGB_color["rgb"]["r"]
    G = RGB_color["rgb"]["g"]
    B = RGB_color["rgb"]["b"]

    beep_freq = int(beep_freq)

    command = "<{},{},{},{},{},{},{},{},{}>".format(
        command, case_master, beep_freq, R, G, B, box, ultra, head
    )
    send = command.encode("ASCII")
    readme = (
        "------------------------READ ME!----------------------\n"
        + "This app was made to control Sparki, an arduino powered."
        + "robot. Sparki is controlled wirelessly via the bluetooth"
        + " HC-05 module and a laptop. With this app you can control"
        + " Sparki's: head, movement, piezometer, ultrasonic sensor, and RGB LED.\n\n"
        + "-------------------COMMAND STRING----------------\n\n"
    )
    command_string = "Command: " + command
    modes = (
        "\n\n------------------------MODES!!!----------------------\n"
        "The motion of Sparki has two modes, where free mode allow"
        + "s sparki to move anywhere. Box mode is designed to show "
        + "Sparki's movements, if a tracking system were installed. "
        + "Box mode is intended for the mock application, and has been left for the user, "
        + "to modify if they want Sparki to respond with the the GUI. "
        + "The sweep mode, sweeps a 180 degree area in 10 degree "
        + "increments, and graphs the distance at each angle. Capture mode,"
        + " records a single data point and displays the distance of that object."
    )

    return readme + command_string + modes

# Move Sparki in Box and Change Sparki Color
@app.callback(
    Output("sparki-icon", "style"),
    [Input("led-control", "value"), 
    Input("command-string", "children")],
    [State("sparki-icon", "style"), 
    State("free-box-hold", "children")],
)
def move_sparki_box_led_color(
    RGB_color, 
    move, 
    style, 
    box
):
    if move == "LED":
        r = RGB_color["rgb"]["r"]
        g = RGB_color["rgb"]["g"]
        b = RGB_color["rgb"]["b"]
        hex_color = rgb_convert_hex(r, g, b)
        style["color"] = hex_color
        return style

    x = style["paddingLeft"][:4]
    x = x.split("p")[0]
    x = int(x)

    y = style["paddingTop"][:4]
    y = y.split("p")[0]
    y = int(y)
    
    if box == "1":
        if move == "UP" and y > 0:
            y = y - 50
            style["paddingTop"] = "{}px".format(y)
        elif move == "DOWN" and y < 260:
            y = y + 50
            style["paddingTop"] = "{}px".format(y)
        elif move == "LEFT" and x > 0:
            x = x - 50
            style["paddingLeft"] = "{}px".format(x)
        elif move == "RIGHT" and x < 280:
            x = x + 50
            style["paddingLeft"] = "{}px".format(x)

    return style


# Sparki Arrow Colors
@app.callback(
    Output("sparki-up", "style"),
    [Input("command-string", "children")],
    [State("sparki-up", "style"), 
    State("free-box-hold", "children")],
)
def sparki_arrow_up(command, style, box):
    if command == "UP" and box == "2":
        style["color"] = "#00cc96"
    else:
        style["color"] = "#EF553B"
    return style


@app.callback(
    Output("sparki-down", "style"),
    [Input("command-string", "children")],
    [State("sparki-down", "style"), 
    State("free-box-hold", "children")],
)
def sparki_arrow_down(command, style, box):
    if command == "DOWN" and box == "2":
        style["color"] = "#00cc96"
    else:
        style["color"] = "#EF553B"
    return style


@app.callback(
    Output("sparki-right", "style"),
    [Input("command-string", "children")],
    [State("sparki-right", "style"), 
    State("free-box-hold", "children")],
)
def sparki_arrow_right(command, style, box):
    if command == "RIGHT" and box == "2":
        style["color"] = "#00cc96"
    else:
        style["color"] = "#EF553B"
    return style


@app.callback(
    Output("sparki-left", "style"),
    [Input("command-string", "children")],
    [State("sparki-left", "style"), 
    State("free-box-hold", "children")],
)
def sparki_arrow_left(command, style, box):
    if command == "LEFT" and box == "2":
        style["color"] = "#00cc96"
    else:
        style["color"] = "#EF553B"
    return style


if __name__ == "__main__":

    app.run_server(debug=True)
