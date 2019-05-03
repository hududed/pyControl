import serial
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output
from dash_daq import DarkThemeProvider as DarkThemeProvider
import numpy as np
import random

# Button Color on Press
def button_color_press():
    style = {"background-color": "#119DFF", "border-color": "#506784", "color": "white"}
    return style

# Button Color on Release
def button_color_press_release():
    style = {"background-color": "", "border-color": "", "color": ""}
    return style


app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True


# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    "https://cdn.rawgit.com/matthewchan15/dash-css-icon-sheet/fe23ccd6/css/dash-hp-multimeter-icon.css",
]


for css in external_css:
    app.css.append_css({"external_url": css})

root_layout = html.Div(
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
            id="banner-daq",
            style={"background-color": "#119DFF"},
            children=[
                html.H2("Dash DAQ: Agilient 34401A Multimeter"),
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
                daq.LEDDisplay(
                    id="meter-display",
                    label="",
                    value="0.000000000",
                    size=60,
                    className="six columns",
                    style={"marginLeft": "1%", "width": "66%"},
                ),
                html.Div(
                    id="unit-holder",
                    children=[
                        html.H5(
                            "V",
                            id="unit",
                            style={
                                "border-radius": "3px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "font-size": "68px",
                                "color": "#2a3f5f",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                                "marginLeft": "-15%",
                                "width": "110%",
                            },
                        )
                    ],
                    className="three columns",
                ),
            ],
            className="row",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "marginTop": "2%",
            },
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            "DC V",
                            id="dc-voltage",
                            className="button button2",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                                "marginLeft": "1px",
                            },
                        ),
                        html.Button(
                            "AC V",
                            id="ac-voltage",
                            className="button button1",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "DC I",
                            id="dc-current",
                            className="button button1",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "AC I",
                            id="ac-current",
                            className="button button1",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "2W",
                            id="2W-resistance",
                            className="resistor resistor1 icon-ohm",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "4W",
                            id="4W-resistance",
                            className="resistor resistor1 icon-ohm",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "",
                            id="frequency",
                            className="frequency frequency1 icon-frequency",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "",
                            id="period",
                            className="period period1 icon-period",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "",
                            id="continuity",
                            className="continuity continuity1 icon-continuity",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
                            },
                        ),
                        html.Button(
                            "",
                            id="diode",
                            className="diode diode1 icon-diode",
                            n_clicks_timestamp="0",
                            style={
                                "background-color": "",
                                "border-color": "",
                                "color": "",
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
                                html.H5(
                                    "Range",
                                    style={
                                        "borderBottom": "1px solid rgb(216, 216, 216)",
                                        "textAlign": "center",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="range-mode",
                                                    options=[
                                                        {
                                                            "label": "Auto",
                                                            "value": "auto",
                                                        },
                                                        {
                                                            "label": "Manual",
                                                            "value": "manual",
                                                        },
                                                    ],
                                                    value="auto",
                                                    className="colorfix"
                                                )
                                            ],
                                            style={
                                                "width": "57%",
                                                "marginTop": "10%",
                                                "marginLeft": "22%",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="range-select",
                                                    options=[
                                                        {
                                                            "label": "Auto Range",
                                                            "value": "DEF",
                                                        },
                                                        {
                                                            "label": "Min Range",
                                                            "value": "MIN",
                                                        },
                                                        {
                                                            "label": "Max Range",
                                                            "value": "MAX",
                                                        },
                                                    ],
                                                    value="DEF",
                                                    disabled=False,
                                                    className="colorfix"
                                                )
                                            ],
                                            style={
                                                "marginTop": "10%",
                                                "width": "57%",
                                                "marginLeft": "22%",
                                                "marginBottom": "10%",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "width": "28%",
                                "marginLeft": "4.5%",
                            },
                        ),
                        html.Div(
                            [
                                html.H5(
                                    "Connections",
                                    style={
                                        "textAlign": "center",
                                        "borderBottom": "1px solid rgb(216, 216, 216)",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "HI",
                                                    className="one columns",
                                                    style={"marginRight": "8.5%"},
                                                ),
                                                html.Div(
                                                    id="left-hi",
                                                    style={
                                                        "background": "#0D76BF",
                                                        "border-radius": "50%",
                                                        "height": "25px",
                                                        "width": "25px",
                                                        "position": "relative",
                                                        "box-shadow": "0 0 0 6px black",
                                                        "marginTop": "4%",
                                                        "marginRight": "6%",
                                                    },
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    id="right-hi",
                                                    style={
                                                        "background": "#0D76BF",
                                                        "border-radius": "50%",
                                                        "height": "25px",
                                                        "width": "25px",
                                                        "position": "relative",
                                                        "box-shadow": "0 0 0 6px black",
                                                        "marginTop": "4%",
                                                        "marginRight": "4%",
                                                    },
                                                    className="six columns",
                                                ),
                                                html.H5("HI", className="one columns"),
                                            ],
                                            className="row",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginRight": "3%",
                                                "marginTop": "2%",
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H5(
                                                    "LO",
                                                    className="one columns",
                                                    style={"marginRight": "8.5%"},
                                                ),
                                                html.Div(
                                                    id="left-lo",
                                                    style={
                                                        "background": "#0D76BF",
                                                        "border-radius": "50%",
                                                        "height": "25px",
                                                        "width": "25px",
                                                        "position": "relative",
                                                        "box-shadow": "0 0 0 6px black",
                                                        "marginTop": "4%",
                                                        "marginRight": "6%",
                                                    },
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    id="right-lo",
                                                    style={
                                                        "background": "#0D76BF",
                                                        "border-radius": "50%",
                                                        "height": "25px",
                                                        "width": "25px",
                                                        "position": "relative",
                                                        "box-shadow": "0 0 0 6px black",
                                                        "marginTop": "4%",
                                                        "marginRight": "4%",
                                                    },
                                                    className="six columns",
                                                ),
                                                html.H5("LO", className="one columns"),
                                            ],
                                            className="row",
                                            style={
                                                "display": "flex",
                                                "justify-content": "center",
                                                "align-items": "center",
                                                "marginRight": "3%",
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                daq.Indicator(
                                                    id="green-good",
                                                    color="#00cc96",
                                                    label="Plug in",
                                                    labelPosition="bottom",
                                                    value=True,
                                                    className="one columns",
                                                    style={
                                                        "paddingLeft": "19%",
                                                        "paddingRight": "11%",
                                                        "textAlign": "center",
                                                    },
                                                ),
                                                html.Div(
                                                    id="bottom-I",
                                                    style={
                                                        "background": "#0D76BF",
                                                        "border-radius": "50%",
                                                        "height": "25px",
                                                        "width": "25px",
                                                        "position": "relative",
                                                        "box-shadow": "0 0 0 6px black",
                                                        "marginRight": "5%",
                                                        "marginBottom": "14%",
                                                    },
                                                    className="four columns",
                                                ),
                                                html.H5(
                                                    "I",
                                                    className="one columns",
                                                    style={"paddingBottom": "14%"},
                                                ),
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
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                            },
                        ),
                        html.Div(
                            [
                                html.H5(
                                    "Acquisition",
                                    style={
                                        "textAlign": "center",
                                        "borderBottom": "1px solid rgb(216, 216, 216)",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="acq-select",
                                                    options=[
                                                        {
                                                            "label": "Manual",
                                                            "value": "manual",
                                                        },
                                                        {
                                                            "label": "Continuous",
                                                            "value": "cont",
                                                        },
                                                    ],
                                                    value="manual",
                                                    className="colorfix Select1"
                                                )
                                            ],
                                            style={
                                                "width": "66%",
                                                "marginLeft": "17.5%",
                                                "marginTop": "10%",
                                                "marginBottom": "10%",
                                            },
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        daq.StopButton(
                                            id="measure-button",
                                            buttonText="Measure",
                                            style={
                                                "marginBottom": "10%",
                                                "marginLeft": "28.5%",
                                            },
                                        )
                                    ]
                                ),
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "width": "24.5%",
                            },
                        ),
                    ],
                    className="row",
                    style={"marginTop": "5%"},
                ),
            ]
        ),
        html.Div(
            [
                html.Div(id="color-jack"),
                html.Div(id="button-press"),
                html.Div(id="dc-volt"),
                dcc.Interval(id="cont-measure", interval=1000000000, n_intervals=0),
            ],
            style={"visibility": "hidden"},
        ),
    ],
    style={
        "padding": "0px 10px 10px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "850",
        "height": "100vh",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
        "height": "640px",
    },
)

light_layout = html.Div(id="container", children=[base_layout])

dark_layout = DarkThemeProvider(
    [
        html.Link(
            href="https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/e84db719/dash-dark-hp-multimeter.css",
            rel="stylesheet",
        ),
        html.Div([base_layout]),
    ]
)

app.layout = root_layout


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
        return dark_layout
    else:
        return light_layout


# Button Press
@app.callback(
    Output("button-press", "children"),
    [Input("dc-voltage", "n_clicks_timestamp"),
    Input("ac-voltage", "n_clicks_timestamp"),
    Input("dc-current", "n_clicks_timestamp"),
    Input("ac-current", "n_clicks_timestamp"),
    Input("2W-resistance", "n_clicks_timestamp"),
    Input("4W-resistance", "n_clicks_timestamp"),
    Input("frequency", "n_clicks_timestamp"),
    Input("period", "n_clicks_timestamp"),
    Input("continuity", "n_clicks_timestamp"),
    Input("diode", "n_clicks_timestamp")]
)
def button_press(
    dc_voltage,
    ac_voltage,
    dc_current,
    ac_current,
    two_resistance,
    four_resistance,
    frequency,
    period,
    continuity,
    diode,
):
    x = np.array(
        [
            0,
            dc_voltage,
            ac_voltage,
            dc_current,
            ac_current,
            two_resistance,
            four_resistance,
            frequency,
            period,
            continuity,
            diode,
        ]
    )
    y = np.array(
        [
            "empty",
            "dc_voltage",
            "ac_voltage",
            "dc_current",
            "ac_current",
            "two_resistance",
            "four_resistance",
            "frequency",
            "period",
            "continuity",
            "diode",
        ]
    )
    x = np.argmax(x)
    return y[x]


# Connections
@app.callback(
    Output("right-hi", "style"),
    [Input("button-press", "children")],
    [State("right-hi", "style"), 
    State("toggleTheme", "value")]
)
def jack_select(button_press, style, theme):
    if theme is False:
        if (
            button_press != "dc_current"
            and button_press != "ac_current"
            and button_press != "empty"
            and button_press != "four_resistance"
        ):
            style["background"] = "#00cc96"
            return style
        else:
            style["background"] = "#0D76BF"
            return style
    elif theme is True:
        if (
            button_press != "dc_current"
            and button_press != "ac_current"
            and button_press != "empty"
            and button_press != "four_resistance"
        ):
            style["background"] = "#00cc96"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style
        else:
            style["background"] = "#0D76BF"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style


@app.callback(
    Output("right-lo", "style"),
    [Input("button-press", "children")],
    [State("right-lo", "style"), 
    State("toggleTheme", "value")]
)
def jack_select(button_press, style, theme):
    if theme == False:
        if button_press != "empty" and button_press != "four_resistance":
            style["background"] = "#00cc96"
            return style
        else:
            style["background"] = "#0D76BF"
            return style
    elif theme == True:
        if button_press != "empty" and button_press != "four_resistance":
            style["background"] = "#00cc96"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style
        else:
            style["background"] = "#0D76BF"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style


@app.callback(
    Output("left-hi", "style"),
    [Input("button-press", "children")],
    [State("left-hi", "style"), 
    State("toggleTheme", "value")]
)
def jack_select(button_press, style, theme):
    if theme is False:
        if button_press != "empty" and button_press == "four_resistance":
            style["background"] = "#00cc96"
            return style
        else:
            style["background"] = "#0D76BF"
            return style
    elif theme is True:
        if button_press != "empty" and button_press == "four_resistance":
            style["background"] = "#00cc96"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style
        else:
            style["background"] = "#0D76BF"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style


@app.callback(
    Output("left-lo", "style"),
    [Input("button-press", "children")],
    [State("left-lo", "style"), 
    State("toggleTheme", "value")]
)
def jack_select(button_press, style, theme):
    if theme is False:
        if button_press != "empty" and button_press == "four_resistance":
            style["background"] = "#00cc96"
            return style
        else:
            style["background"] = "#0D76BF"
            return style
    elif theme is True:
        if button_press != "empty" and button_press == "four_resistance":
            style["background"] = "#00cc96"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style
        else:
            style["background"] = "#0D76BF"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style


@app.callback(
    Output("bottom-I", "style"),
    [Input("button-press", "children")],
    [State("bottom-I", "style"), 
    State("toggleTheme", "value")]
)
def jack_select(button_press, style, theme):
    if theme is False:
        if button_press != "empty" and (
            button_press == "ac_current" or button_press == "dc_current"
        ):
            style["background"] = "#00cc96"
            return style
        else:
            style["background"] = "#0D76BF"
            return style
    elif theme is True:
        if button_press != "empty" and (
            button_press == "ac_current" or button_press == "dc_current"
        ):
            style["background"] = "#00cc96"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style
        else:
            style["background"] = "#0D76BF"
            style["box-shadow"] = "0 0 0 6px #2a3f5f"
            return style


# ClassName
@app.callback(
    Output("dc-voltage", "className"),
    [Input("toggleTheme", "value")],
    [State("dc-voltage", "className")],
)
def class_change(theme, className):
    if theme:
        className = "buttondark buttondark2"
        return className
    else:
        className = "button button2"
        return className


@app.callback(
    Output("ac-voltage", "className"),
    [Input("toggleTheme", "value")],
    [State("ac-voltage", "className")],
)
def class_change(theme, className):
    if theme:
        className = "buttondark buttondark1"
        return className
    else:
        className = "button button1"
        return className


@app.callback(
    Output("dc-current", "className"),
    [Input("toggleTheme", "value")],
    [State("dc-current", "className")],
)
def class_change(theme, className):
    if theme:
        className = "buttondark buttondark1"
        return className
    else:
        className = ("button button1",)
        return className


@app.callback(
    Output("ac-current", "className"),
    [Input("toggleTheme", "value")],
    [State("ac-current", "className")],
)
def class_change(theme, className):
    if theme:
        className = "buttondark buttondark1"
        return className
    else:
        className = ("button button1",)
        return className


@app.callback(
    Output("2W-resistance", "className"),
    [Input("toggleTheme", "value")],
    [State("2W-resistance", "className")],
)
def class_change(theme, className):
    if theme:
        className = "resistordark resistordark1 icon-ohm"
        return className
    else:
        className = "resistor resistor1 icon-ohm"
        return className


@app.callback(
    Output("4W-resistance", "className"),
    [Input("toggleTheme", "value")],
    [State("4W-resistance", "className")],
)
def class_change(theme, className):
    if theme:
        className = "resistordark resistordark1 icon-ohm"
        return className
    else:
        className = "resistor resistor1 icon-ohm"
        return className


@app.callback(
    Output("frequency", "className"),
    [Input("toggleTheme", "value")],
    [State("frequency", "className")],
)
def class_change(theme, className):
    if theme:
        className = "frequencydark frequencydark1 icon-frequency"
        return className
    else:
        className = "frequency frequency1 icon-frequency"
        return className


@app.callback(
    Output("period", "className"),
    [Input("toggleTheme", "value")],
    [State("period", "className")],
)
def class_change(theme, className):
    if theme:
        className = "perioddark perioddark1 icon-period"
        return className
    else:
        className = "period period1 icon-period"
        return className


@app.callback(
    Output("continuity", "className"),
    [Input("toggleTheme", "value")],
    [State("continuity", "className")],
)
def class_change(theme, className):
    if theme:
        className = "continuitydark continuitydark1 icon-continuity"
        return className
    else:
        className = "continuity continuity1 icon-continuity"
        return className


@app.callback(
    Output("diode", "className"),
    [Input("toggleTheme", "value")],
    [State("diode", "className")],
)
def class_change(theme, className):
    if theme:
        className = "diodedark diodedark1 icon-diode"
        return className
    else:
        className = "diode diode1 icon-diode"
        return className


# Button Sticky
@app.callback(
    Output("dc-voltage", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "dc_voltage":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("ac-voltage", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "ac_voltage":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("dc-current", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "dc_current":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("ac-current", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "ac_current":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("2W-resistance", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "two_resistance":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("4W-resistance", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "four_resistance":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("frequency", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "frequency":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("period", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "period":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("continuity", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "continuity":
        return button_color_press()
    else:
        return button_color_press_release()


@app.callback(
    Output("diode", "style"), 
    [Input("button-press", "children")]
)
def button_select(button_press):
    if button_press == "diode":
        return button_color_press()
    else:
        return button_color_press_release()


# Disable
@app.callback(
    Output("range-select", "disabled"), 
    [Input("range-mode", "value")]
)
def button_select(range_mode):
    if range_mode == "auto":
        return True
    else:
        return False


def disable_acquisition(range_mode):
    if range_mode == "manual":
        return True
    else:
        return False


# Box Fix
@app.callback(
    Output("range-select", "value"), 
    [Input("range-mode", "value")]
)
def button_select(range_mode):
    if range_mode == "auto":
        return "DEF"


# Data Collect
@app.callback(
    Output("meter-display", "value"),
    [Input("measure-button", "n_clicks"), 
    Input("cont-measure", "n_intervals")],
    [State("range-select", "value"), 
    State("button-press", "children")]
)
def display_values(measure_button, cont_intervals, range_select, button_press):
    try:

        if button_press == "dc_voltage":
            response = random.uniform(4.7, 5)
        elif button_press == "ac_voltage":
            response = random.uniform(242, 244)
        elif button_press == "ac_current":
            response = random.uniform(10, 12)
        elif button_press == "dc_current":
            response = random.uniform(0.2, 0.3)
        elif button_press == "two_resistance":
            response = random.uniform(500, 501)
        elif button_press == "four_resistance":
            response = random.uniform(500000, 500001)
        elif button_press == "frequency":
            response = random.uniform(220, 221)
        elif button_press == "period":
            response = random.uniform(0.5, 0.8)
        elif button_press == "continuity":
            response = random.uniform(0.1, 0.5)
        elif button_press == "diode":
            response = random.uniform(0.0001, 0.0008)

        if range_select == "MIN":
            response = response * 1000
            check = int(round(response))
            response = "%.11f" % response
            response = f"{response:{11}.{11}}"

            if check > 500000:
                response = 9999999999
            return response
        elif range_select == "MAX":
            response = response * (1 / 1000)

        response = "%.11f" % response
        response = f"{response:{11}.{11}}"
        return response

    except UnboundLocalError:
        response = 0
        response = "%.11f" % response
        response = f"{response:{11}.{11}}"
        return response


# Unit Box
@app.callback(
    Output("unit", "children"),
    [Input("button-press", "children"),
    Input("meter-display", "value"),
    Input("measure-button", "n_clicks")],
    [State("range-select", "value")],
)
def unit_box(button_press, meter_display, measure_button, range_select):
    try:
        if range_select == "DEF":
            range_select = ""
        elif range_select == "MAX":
            range_select = "k"
        elif range_select == "MIN":
            range_select = "m"

        meter_display = float(meter_display)
        meter_display = int(round(meter_display))
        if meter_display > 99999999:
            response = "OVLD"
            return response

        if button_press == "empty":
            response = "V"
            return response
        elif button_press == "dc_voltage" or button_press == "ac_voltage":
            response = range_select + "V"
            return response
        elif button_press == "dc_current" or button_press == "ac_current":
            response = range_select + "A"
            return response
        elif button_press == "two_resistance" or button_press == "four_resistance":
            response = range_select + "Ω"
            return response
        elif button_press == "frequency":
            response = range_select + "Hz"
            return response
        elif button_press == "period":
            response = range_select + "S"
            return response
        elif button_press == "continuity":
            response = range_select + "Ω"
            return response
        elif button_press == "diode":
            response = range_select + "V"
            return response
    except TypeError:
        return "ERR"


# Data Collect Continuous Button
@app.callback(
    Output("cont-measure", "interval"),
    [Input("measure-button", "n_clicks"), 
    Input("acq-select", "value")]
)
def data_collect_continuous(measure_button, acq_select):
    if acq_select == "cont":
        delay = 1000
        return delay
    else:
        delay = 1000000000
        return delay


if __name__ == "__main__":

    app.run_server(debug=True)
