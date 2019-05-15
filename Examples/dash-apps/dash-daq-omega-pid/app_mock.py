import time
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scipy.integrate as integrate
from dash.dependencies import State, Input, Output

app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True

df = pd.read_csv("control_curves.csv")



# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
]


for css in external_css:
    app.css.append_css({"external_url": css})


app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#119DFF"},
            children=[
                html.H2("Dash DAQ: Omega Platinum Controller"),
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
                                html.Div(
                                    [
                                        daq.Indicator(
                                            id="graph-on-off",
                                            label="",
                                            value=True,
                                            color="#00cc96",
                                            className="one columns",
                                            labelPosition="top",
                                            style={
                                                "position": "absolute",
                                                "left": "20%",
                                                "top": "33%",
                                            },
                                        ),
                                        html.H4(
                                            "Temperature vs. Time Graph",
                                            className=" three columns",
                                            style={
                                                "textAlign": "center",
                                                "width": "41%",
                                            },
                                        ),
                                        daq.StopButton(
                                            id="reset-button",
                                            buttonText="Reset",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "width": "10%",
                                            },
                                            n_clicks=0,
                                            className="three columns",
                                        ),
                                    ],
                                    className="row",
                                    style={
                                        "marginTop": "1%",
                                        "marginBottom": "2%",
                                        "justify-content": "center",
                                        "align-items": "center",
                                        "display": "flex",
                                        "position": "relative",
                                    },
                                ),
                                dcc.Graph(
                                    id="graph-data",
                                    style={"height": "254px", "marginBottom": "1%"},
                                    figure={
                                        "data": [
                                            go.Scatter(
                                                x=[],
                                                y=[],
                                                mode="lines",
                                                marker={"size": 6},
                                                name="Temperature (C°)",
                                            ),
                                            go.Scatter(
                                                x=[],
                                                y=[],
                                                mode="lines",
                                                marker={"size": 6},
                                                name="Set Point (C°)",
                                            ),
                                        ],
                                        "layout": go.Layout(
                                            xaxis={
                                                "title": "Time (s)",
                                                "autorange": True,
                                            },
                                            yaxis={"title": "Temperature (C)"},
                                            margin={"l": 70, "b": 100, "t": 0, "r": 25},
                                        ),
                                    },
                                ),
                            ],
                            className="twelve columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "marginBottom": "2%",
                            },
                        )
                    ],
                    className="row",
                    style={"marginTop": "3%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Control Panel", 
                                    style={"textAlign": "center"}),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="action",
                                                    options=[
                                                        {
                                                            "label": "Reverse",
                                                            "value": "reverse",
                                                        }
                                                    ],
                                                    value="reverse",
                                                )
                                            ],
                                            className="four columns",
                                            style={
                                                "marginLeft": "14%",
                                                "marginRight": "9%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="outputs-mode",
                                                    options=[
                                                        {"label": "PID", "value": "pid"}
                                                    ],
                                                    value="pid",
                                                )
                                            ],
                                            className="four columns",
                                            style={"zIndex": "50"},
                                        ),
                                    ],
                                    className="row",
                                    style={"marginTop": "5%", "marginBottom": "4%"},
                                ),
                                html.Div(
                                    [
                                        daq.Knob(
                                            id="filter-rate",
                                            label="Filter Rate",
                                            labelPosition="bottom",
                                            size=65,
                                            value=0,
                                            scale={
                                                "custom": {
                                                    "0": "1X",
                                                    "1": "2X",
                                                    "2": "X4",
                                                    "3": "X8",
                                                    "4": "X16",
                                                    "5": "X32",
                                                    "6": "X64",
                                                    "7": "X128",
                                                }
                                            },
                                            color="#FF5E5E",
                                            max=7,
                                            className="six columns",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                        ),
                                        daq.Knob(
                                            id="thermo-type",
                                            label="Couple",
                                            labelPosition="bottom",
                                            size=65,
                                            value=0,
                                            scale={
                                                "custom": {
                                                    "0": "J",
                                                    "1": "K",
                                                    "2": "T",
                                                    "3": "E",
                                                    "4": "N",
                                                    "5": "RES",
                                                    "6": "R",
                                                    "7": "S",
                                                    "8": "B",
                                                    "9": "C",
                                                }
                                            },
                                            color="#FF5E5E",
                                            max=9,
                                            className="six columns",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                            },
                                        ),
                                    ],
                                    className="row",
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "align-items": "center",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        daq.StopButton(
                                                            id="start-button",
                                                            buttonText="Start",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                                "paddingBottom": "22%",
                                                            },
                                                            n_clicks=0,
                                                        ),
                                                        daq.StopButton(
                                                            id="stop-button",
                                                            buttonText="Stop",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                            },
                                                            n_clicks=0,
                                                        ),
                                                    ],
                                                    className="three columns",
                                                    style={"marginLeft": "13%"},
                                                ),
                                                daq.Knob(
                                                    id="refresh-rate",
                                                    label="Refresh",
                                                    labelPosition="bottom",
                                                    size=65,
                                                    value=1,
                                                    scale={"interval": 1},
                                                    color="#FF5E5E",
                                                    max=10,
                                                    className="six columns",
                                                    style={
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center",
                                                        "marginLeft": "17%",
                                                        "marginTop": "-11%",
                                                    },
                                                ),
                                            ],
                                            className="row",
                                        )
                                    ]
                                ),
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "height": "434px",
                            },
                        ),
                        html.Div(
                            [
                                html.H3("PID Control", style={"textAlign": "center"}),
                                daq.ToggleSwitch(  # SWITCH Modes
                                    id="PID-man-auto",
                                    label=["Manual", "Autotune"],
                                    color="#FF5E5E",
                                    size=32,
                                    style={"justify-content": "center"},
                                    value=False,
                                ),
                                html.Div(
                                    id="autotune-box",
                                    children=[
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        daq.BooleanSwitch(
                                                            id="adaptive-switch",
                                                            label="Adaptive Control",
                                                            labelPosition="bottom",
                                                            on=True,
                                                            style={
                                                                "paddingTop": "8.5%",
                                                                "paddingBottom": "13%",
                                                            },
                                                        ),
                                                        daq.NumericInput(
                                                            id="max-rate",
                                                            label="Max Rate (/min)",
                                                            value=10,
                                                            max=10,
                                                            min=10,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "25%"
                                                            },
                                                            disabled=True,
                                                        ),
                                                        daq.StopButton(
                                                            id="autotune-button",
                                                            buttonText="Autotune",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                                "paddingBottom": "34%",
                                                            },
                                                            n_clicks=0,
                                                        ),
                                                    ],
                                                    className="five columns",
                                                ),
                                                html.Div(
                                                    [
                                                        daq.NumericInput(
                                                            id="PID-setpoint-auto",
                                                            label="PID Setpoint (C°)",
                                                            value=26,
                                                            max=27,
                                                            min=25,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "5%"
                                                            },
                                                        ),
                                                        daq.NumericInput(
                                                            id="autotune-timeout",
                                                            label="Autotune Timeout (s)",
                                                            value=5,
                                                            max=10,
                                                            min=5,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "8%"
                                                            },
                                                        ),
                                                        html.Div(
                                                            [
                                                                daq.Indicator(
                                                                    id="output-1-auto",
                                                                    label="Out 1",
                                                                    value=True,
                                                                    color="#EF553B",
                                                                    className="eight columns",
                                                                    labelPosition="bottom",
                                                                    size=20,
                                                                    style={
                                                                        "paddingLeft": "19%"
                                                                    },
                                                                )
                                                            ],
                                                            className="row",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="row",
                                            style={
                                                "marginLeft": "12%",
                                                "marginBottom": "9%",
                                            },
                                        )
                                    ],
                                    style={
                                        "marginTop": "5%",
                                        "position": "absolute",
                                        "height": "100%",
                                        "width": "100%",
                                    },
                                ),
                                html.Div(
                                    id="manual-box",
                                    children=[
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        daq.BooleanSwitch(
                                                            id="adaptive-switch",
                                                            label="Adaptive Control",
                                                            labelPosition="bottom",
                                                            on=True,
                                                            style={
                                                                "paddingTop": "8.5%",
                                                                "paddingBottom": "13%",
                                                            },
                                                        ),
                                                        daq.NumericInput(
                                                            id="max-rate",
                                                            label="Max Rate (/min)",
                                                            value=10,
                                                            max=10,
                                                            min=10,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "13%"
                                                            },
                                                            disabled=True,
                                                        ),
                                                        daq.NumericInput(
                                                            id="dev-gain",
                                                            label="Derivative Gain",
                                                            value=0.00,
                                                            max=300,
                                                            min=0,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "21%"
                                                            },
                                                            disabled=True,
                                                        ),
                                                        daq.StopButton(
                                                            id="manual-button",
                                                            buttonText="Set PID",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                            },
                                                            n_clicks=0,
                                                            disabled=False,
                                                        ),
                                                    ],
                                                    className="five columns",
                                                ),
                                                html.Div(
                                                    [
                                                        daq.NumericInput(
                                                            id="PID-setpoint",
                                                            label="PID Setpoint (C°)",
                                                            value=26,
                                                            max=27,
                                                            min=25,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "5%"
                                                            },
                                                        ),
                                                        daq.NumericInput(
                                                            id="pro-gain",
                                                            label="Propotional Gain",
                                                            value=0.00,
                                                            max=300,
                                                            min=0,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "5%"
                                                            },
                                                            disabled=True,
                                                        ),
                                                        daq.NumericInput(
                                                            id="int-gain",
                                                            label="Integral Gain",
                                                            value=0.00,
                                                            max=300,
                                                            min=0,
                                                            size=75,
                                                            labelPosition="bottom",
                                                            style={
                                                                "paddingBottom": "6%"
                                                            },
                                                            disabled=True,
                                                        ),
                                                        html.Div(
                                                            [
                                                                daq.Indicator(
                                                                    id="output-1",
                                                                    label="Out 1",
                                                                    value=True,
                                                                    color="#EF553B",
                                                                    className="eight columns",
                                                                    labelPosition="bottom",
                                                                    size=20,
                                                                    style={
                                                                        "paddingLeft": "20%"
                                                                    },
                                                                )
                                                            ],
                                                            className="row",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="row",
                                            style={
                                                "marginLeft": "12%",
                                                "marginBottom": "9%",
                                            },
                                        )
                                    ],
                                    style={
                                        "marginTop": "5%",
                                        "position": "absolute",
                                        "height": "100%",
                                        "width": "100%",
                                    },
                                ),
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "position": "relative",
                                "height": "435px",
                            },
                        ),
                        html.Div(
                            [
                                html.H3("Data Response", style={"textAlign": "center"}),
                                html.Div(
                                    [
                                        daq.LEDDisplay(
                                            id="omega-display",
                                            value="0.12345",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "paddingTop": "1.7%",
                                                "paddingLeft": "20.5%",
                                                "marginLeft": "-7%",
                                                "marginRight": "2%",
                                            },
                                            className="eight columns",
                                            size=36,
                                        ),
                                        html.Div(
                                            id="unit-holder",
                                            children=[
                                                html.H5(
                                                    "C°",
                                                    id="unit",
                                                    style={
                                                        "border-radius": "3px",
                                                        "border-width": "5px",
                                                        "border": "1px solid rgb(216, 216, 216)",
                                                        "font-size": "47px",
                                                        "color": "#2a3f5f",
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center",
                                                        "width": "27%",
                                                        "marginLeft": "3%",
                                                    },
                                                    className="four columns",
                                                )
                                            ],
                                        ),
                                    ],
                                    className="row",
                                    style={"marginBottom": "2%"},
                                ),
                                html.Div(
                                    [
                                        daq.LEDDisplay(
                                            id="PID-display",
                                            value="0.12",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "paddingTop": "1.6%",
                                                "paddingLeft": "30.5%",
                                                "marginLeft": "1%",
                                            },
                                            className="four columns",
                                            size=36,
                                        ),
                                        html.Div(
                                            id="unit-holder",
                                            children=[
                                                html.H5(
                                                    "PID%",
                                                    id="unit",
                                                    style={
                                                        "border-radius": "3px",
                                                        "border-width": "5px",
                                                        "border": "1px solid rgb(216, 216, 216)",
                                                        "font-size": "47px",
                                                        "color": "#2a3f5f",
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center",
                                                        "width": "36%",
                                                        "marginLeft": "23%",
                                                    },
                                                    className="six columns",
                                                )
                                            ],
                                        ),
                                    ],
                                    className="row",
                                    style={"marginBottom": "4%"},
                                ),
                                dcc.Textarea(
                                    id="status-monitor",
                                    placeholder=" ",
                                    value="",
                                    style={
                                        "width": "89%",
                                        "height": "157px",
                                        "marginLeft": "5.7%",
                                        "marginBottom": "6%",
                                    },
                                ),
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "height": "436px",
                            },
                        ),
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Div(id="stop-timestamp"),
                        html.Div(id="start-timestamp"),
                        html.Div(id="reset-timestamp"),
                        html.Div(id="autotune-timestamp"),
                        html.Div(id="manual-timestamp"),
                        html.Div(id="graph-data-send"),
                        html.Div(id="temperature-store"),
                        html.Div(id="command-string"),
                        html.Div(id="thermotype-hold"),
                        html.Div(id="filter-hold"),
                        html.Div(id="autotune-start"),
                        html.Div(id="autotune-setpoint"),
                        html.Div(id="autotune-adapt"),
                        html.Div(id="manual-start"),
                        html.Div(id="pid-action"),
                        html.Div(id="output-mode"),
                        html.Div(id="data-set"),
                        dcc.Interval(
                            id="graph-interval", interval=100000, n_intervals=0
                        ),
                    ],
                    style={"visibility": "hidden"},
                ),
            ],
            style={"padding": "0px 30px 0px 30px"},
        ),
    ],
    style={
        "padding": "0px 10px 0px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "1180px",
        "height": "955px",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
    },
)

# Manual and Auto
@app.callback(
    Output("manual-box", "style"),
    [Input("PID-man-auto", "value")],
    [State("manual-box", "style")],
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
    Output("autotune-box", "style"),
    [Input("PID-man-auto", "value")],
    [State("autotune-box", "style")],
)
def sweep_components(value, style):
    if value:
        style["visibility"] = "visible"
        style["zIndex"] = "20"
    else:
        style["visibility"] = "hidden"
        style["zIndex"] = "-10"
    return style


# Filter Rate
@app.callback(
    Output("filter-hold", "children"), 
    [Input("filter-rate", "value")]
)
def filter_hold(filter_knob):
    filter_knob = int(filter_knob)
    return filter_knob


# Thermocouple
@app.callback(
    Output("thermotype-hold", "children"), 
    [Input("thermo-type", "value")]
)
def thermotype_hold(thermo_knob):
    thermo_knob = int(thermo_knob)
    return thermo_knob


# Buttons
@app.callback(
    Output("start-timestamp", "children"), 
    [Input("start-button", "n_clicks")]
)
def start_time(start):
    if start >= 1:
        return time.time()
    return 0.0


@app.callback(
    Output("stop-timestamp", "children"), 
    [Input("stop-button", "n_clicks")]
)
def start_time(stop):
    return time.time()


@app.callback(
    Output("reset-timestamp", "children"), 
    [Input("reset-button", "n_clicks")]
)
def reset_time(reset):
    return time.time()


@app.callback(
    Output("autotune-timestamp", "children"), 
    [Input("autotune-button", "n_clicks")]
)
def autotune_time(autotune):
    return time.time()


@app.callback(
    Output("manual-timestamp", "children"), 
    [Input("manual-button", "n_clicks")]
)
def manual_time(autotune):
    return time.time()


# Button Control Panel
@app.callback(
    Output("command-string", "children"),
    [Input("start-timestamp", "children"),
    Input("stop-timestamp", "children"),
    Input("reset-timestamp", "children"),
    Input("autotune-timestamp", "children"),
    Input("manual-timestamp", "children")]
)
def command_string(
    start_button, 
    stop_button, 
    reset_button, 
    autotune_button, 
    manual_button
    ):

    master_command = {
        "START": start_button,
        "STOP": stop_button,
        "RESET": reset_button,
        "AUTO": autotune_button,
        "MANUAL": manual_button,
    }
    recent_command = max(master_command, key=master_command.get)
    return recent_command


# Rate
@app.callback(
    Output("graph-interval", "interval"),
    [Input("command-string", "children"), 
    Input("refresh-rate", "value")],
)
def graph_control(command, rate):
    if command == "START":
        rate = int(rate) * 1000
        return rate
    else:
        return 2500


# Temperature Store
@app.callback(
    Output("temperature-store", "children"),
    [Input("command-string", "children"), 
    Input("graph-interval", "n_intervals")],
)
def graph_control(command, rate):
    if command == "START":
        return


# Graph LED
@app.callback(
    Output("graph-on-off", "color"), 
    [Input("command-string", "children")]
)
def graph_LED(command):
    if command == "START":
        return "#00cc96"

    return "#EF553B"


# Set Points Manual
@app.callback(
    Output("dev-gain", "value"),
    [Input("manual-button", "n_clicks"), 
    Input("autotune-button", "n_clicks")],
    [State("PID-setpoint", "value"),
    State("PID-setpoint-auto", "value"),
    State("PID-man-auto", "value")]
)
def set_point(
    set_pid_button, 
    autotune_button, 
    PID_setpoint, 
    PID_setpoint_auto, 
    PID_man_auto
):
    if PID_man_auto:
        if PID_setpoint_auto == 25:
            return 0.5
        elif PID_setpoint_auto == 26:
            return 0.3
        elif PID_setpoint_auto == 27:
            return 0.1
    else:
        if PID_setpoint == 25:
            return 0.65
        elif PID_setpoint == 26:
            return 0.25
        elif PID_setpoint == 27:
            return 0.1


@app.callback(
    Output("pro-gain", "value"),
    [Input("manual-button", "n_clicks"), 
    Input("autotune-button", "n_clicks")],
    [State("PID-setpoint", "value"),
    State("PID-setpoint-auto", "value"),
    State("PID-man-auto", "value")]
)
def set_point(
    set_pid_button, 
    autotune_button, 
    PID_setpoint, 
    PID_setpoint_auto, 
    PID_man_auto
):
    if PID_man_auto:
        if PID_setpoint_auto == 25:
            return 1
        elif PID_setpoint_auto == 26:
            return 5
        elif PID_setpoint_auto == 27:
            return 0.1
    else:
        if PID_setpoint == 25:
            return 1.6
        elif PID_setpoint == 26:
            return 5.3
        elif PID_setpoint == 27:
            return 0.1


@app.callback(
    Output("int-gain", "value"),
    [Input("manual-button", "n_clicks"), 
    Input("autotune-button", "n_clicks")],
    [State("PID-setpoint", "value"),
    State("PID-setpoint-auto", "value"),
    State("PID-man-auto", "value")]
)
def set_point(
    set_pid_button, 
    autotune_button, 
    PID_setpoint, 
    PID_setpoint_auto, 
    PID_man_auto
):
    if PID_man_auto:
        if PID_setpoint_auto == 25:
            return 0.5
        elif PID_setpoint_auto == 26:
            return 0.6
        elif PID_setpoint_auto == 27:
            return 0.1
    else:
        if PID_setpoint == 25:
            return 0.45
        elif PID_setpoint == 26:
            return 0.82
        elif PID_setpoint == 27:
            return 0.1


# Disable Setpoint Button
@app.callback(
    Output("manual-button", "disabled"), 
    [Input("command-string", "children")]
)
def set_point(command):
    if command == "START":
        return True
    return False


@app.callback(
    Output("autotune-button", "disabled"), 
    [Input("command-string", "children")]
)
def set_point(command):
    if command == "START":
        return True
    return False


# Serial Monitor
@app.callback(
    Output("status-monitor", "value"),
    [Input("graph-interval", "n_intervals"), 
    Input("autotune-button", "n_clicks")],
    [State("command-string", "children"),
    State("max-rate", "value"),
    State("dev-gain", "value"),
    State("pro-gain", "value"),
    State("int-gain", "value"),
    State("autotune-timestamp", "children"),
    State("autotune-timeout", "value")]
)
def serial_monitor(
    intervals,
    autotune_button,
    command,
    max_rate,
    dev_gain,
    pro_gain,
    int_gain,
    autotune_time,
    autotune_timeout,
):
    autotune_button_time = int(time.time() - autotune_time)
    if command == "START":
        state = "Running"
    elif command == "AUTO" and autotune_button_time < autotune_timeout:
        state = "Autotune in Progress"
    else:
        state = "Stop"

    
    dev_gain = str(dev_gain)
    pro_gain = str(pro_gain)
    int_gain = str(int_gain)
    

    status = (
        "----------------STATUS----------------\n"
        + "System Status: "
        + state
        + "\nProportional Gain: "
        + pro_gain
        + "\nIntegral Gain: "
        + int_gain
        + "\nDerivative Gain: "
        + dev_gain
        + "\n----------------READ ME---------------\n"
        + "This application is designed for the Omega Platinum PID CN32PT-440-DC controller. You are currently "
        + "viewing the mock application, with limited features. The mock app is designed to show the user "
        + "how this application would work if it was connected. All functions and features "
        + "are working and unlocked in the local version. For more information about how to create an "
        + "amazing app like this with Dash DAQ, check out the blog post by clicking on the Dash-DAQ logo."
    )
    return status


# Data_set
@app.callback(
    Output("data-set", "children"),
    [Input("temperature-store", "children")],
    [State("command-string", "children"),
    State("start-timestamp", "children"),
    State("start-button", "n_clicks"),
    State("PID-setpoint", "value"),
    State("dev-gain", "value"),
    State("pro-gain", "value"),
    State("int-gain", "value")]
)
def data_set(
    temperature,
    command,
    start,
    start_button,
    PID_setpoint,
    dev_gain,
    pro_gain,
    int_gain,
):
    if command == "START":
        diff = int(time.time() - start)
        PID_setpoint = int(PID_setpoint)
        if diff > 99:
            return PID_setpoint
        PID_setpoint = float(PID_setpoint)
        PID_setpoint = str(PID_setpoint)

        measured_value = df.loc[diff, PID_setpoint]
        return measured_value


# LED Control Panel
@app.callback(
    Output("omega-display", "value"),
    [Input("temperature-store", "children")],
    [State("command-string", "children"), 
    State("data-set", "children")]
)
def graph_control(temperature, command, data_set):
    if command == "START" and data_set is not None:
        data_set = "%.4f" % data_set
        data_set = f"{data_set:{6}.{6}}"
        return data_set
    data_set = 0
    data_set = "%.4f" % data_set
    data_set = f"{data_set:{6}.{6}}"
    return data_set


@app.callback(
    Output("PID-display", "value"),
    [Input("temperature-store", "children")],
    [State("command-string", "children"),
    State("start-timestamp", "children"),
    State("PID-setpoint", "value"),
    State("dev-gain", "value"),
    State("pro-gain", "value"),
    State("int-gain", "value")]
)
def PID_percent(
    n_intervals, 
    command, 
    start, 
    PID_setpoint, 
    dev_gain, 
    pro_gain, 
    int_gain
):  
    previous_error = 0
    if command == "START":

        diff = int(time.time() - start)
        PID_setpoint = int(PID_setpoint)
        PID_int = PID_setpoint

        PID_setpoint = float(PID_setpoint)
        PID_setpoint = str(PID_setpoint)

        if diff > 99:
            output = 0
            output = "%.3f" % output
            output = f"{output:{5}.{5}}"
            return output
        measured_value = df.loc[diff, PID_setpoint]
        if measured_value > PID_int:
            output = 0
            output = "%.3f" % output
            output = f"{output:{5}.{5}}"
            return output
        if diff >= 1:
            previous_value = df.loc[(diff - 1), PID_setpoint]
            previous_error = PID_int - previous_value

        error = PID_int - measured_value
        integral = integrate.quad(lambda t: error, 0, diff)
        derivative = error - previous_error
        output = abs(pro_gain * error + int_gain * integral[0] + dev_gain * derivative)
        if output > 100:
            output = 100
        output = "%.3f" % output
        output = f"{output:{5}.{5}}"
        return output
    output = 0
    output = "%.3f" % output
    output = f"{output:{5}.{5}}"
    return output


# OUT LED 1 Manual


@app.callback(
    Output("output-1", "color"),
    [Input("temperature-store", "children")],
    [State("PID-display", "value")],
)
def led_out(temp_store, PID_display):
    if PID_display == "0.000":
        return "#EF553B"
    return "#00cc96"


# OUT LED 1 Auto
@app.callback(
    Output("output-1-auto", "color"),
    [Input("temperature-store", "children")],
    [State("PID-display", "value")],
)
def led_out(temp_store, PID_display):
    if PID_display == "0.000":
        return "#EF553B"
    return "#00cc96"


# Graph


@app.callback(
    Output("graph-data", "figure"),
    [Input("temperature-store", "children")],
    [State("graph-data", "figure"),
    State("command-string", "children"),
    State("start-timestamp", "children"),
    State("start-button", "n_clicks"),
    State("PID-setpoint", "value"),
    State("data-set", "children")],
)
def graph_data(temperature, figure, command, start, start_button, PID, data_set):
    if command == "START":
        x = figure["data"][0]["x"]
        y = figure["data"][0]["y"]
        set_point = figure["data"][1]["y"]

        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        x.append(time_now)
        y.append(data_set)
        set_point.append(PID)
    elif command == "RESET":
        x = []
        y = []
        set_point = []
        time_now = 0
    else:
        x = figure["data"][0]["x"]
        y = figure["data"][0]["y"]
        set_point = figure["data"][1]["y"]
    return {
        "data": [
            go.Scatter(
                x=x, 
                y=y, 
                mode="lines", 
                marker={"size": 6}, 
                name="Temperature (C°)"
            ),
            go.Scatter(
                x=x,
                y=set_point,
                mode="lines",
                marker={"size": 6},
                name="Set Point (C°)",
            ),
        ],
        "layout": go.Layout(
            autosize=True,
            showlegend=True,
            xaxis={"title": "Time (s)", "autorange": True},
            yaxis={"title": "Temperature(C°)", "autorange": True},
            margin={"l": 70, "b": 100, "t": 0, "r": 25},
        ),
    }

if __name__ == "__main__":

    app.run_server(debug=True)
