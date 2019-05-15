import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output


app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True


# CSS Imports, Add CSS style sheets together
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
    "https://rawgit.com/matthewchan15/dash-css-style-sheets/master/pop-up.css",
]


for css in external_css:
    app.css.append_css({"external_url": css})

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    id="dash-daq-remote-banner",
                    style={"position": "absolute", "top": "70px", "right": "-45px"},
                    children=[
                        html.A(
                            html.Img(
                                src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-stripe.png",
                                style={"width": "45%"},
                            ),
                            href="http://www.dashdaq.io",
                        )
                    ],
                ),
                html.P(
                    "Robotic Arm Edge",
                    style={
                        "position": "absolute",
                        "top": "118px",
                        "left": "307px",
                        "color": "#506784",
                        "font-size": "17px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "LED On",
                                    style={
                                        "textAlign": "center",
                                        "font-size": "1.1rem",
                                        "position": "relative",
                                        "right": "19px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Base Left",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "paddingLeft": "14%",
                                                "top": "30px",
                                                "paddingTop": "8%",
                                            },
                                            className="three columns",
                                        ),
                                        daq.Joystick(
                                            id="LED-base-move",
                                            force=0,
                                            className="four columns",
                                        ),
                                        html.H6(
                                            "Base Right",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "left": "9px",
                                                "top": "24px",
                                                "width": "9%",
                                                "position": "relative",
                                            },
                                            className="three columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.H6(
                                    "LED Off",
                                    style={
                                        "textAlign": "center",
                                        "font-size": "1.1rem",
                                        "position": "relative",
                                        "right": "21px",
                                    },
                                ),
                            ],
                            className="six columns",
                            style={"paddingTop": "3%"},
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "Wrist Up",
                                    style={
                                        "textAlign": "center",
                                        "font-size": "1.1rem",
                                        "position": "relative",
                                        "right": "20px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Open Grip",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "paddingLeft": "13%",
                                                "paddingTop": "8.5%",
                                            },
                                            className="three columns",
                                        ),
                                        daq.Joystick(
                                            id="wrist-grip-move",
                                            force=0,
                                            className="four columns",
                                        ),
                                        html.H6(
                                            "Close Grip",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "left": "6px",
                                                "top": "26.5px",
                                                "width": "9%",
                                                "position": "relative",
                                            },
                                            className="three columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.H6(
                                    "Wrist Down",
                                    style={
                                        "textAlign": "center",
                                        "font-size": "1.1rem",
                                        "position": "relative",
                                        "right": "19px",
                                    },
                                ),
                            ],
                            className="six columns",
                            style={"paddingTop": "3%"},
                        ),
                    ],
                    className="row",
                    style={
                        "width": "86%",
                        "top": "26%",
                        "right": "4%",
                        "position": "absolute",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                daq.Indicator(
                                    id="LED-state",
                                    label="LED ON/OFF",
                                    value=True,
                                    className="two columns",
                                    color="#EF553B",
                                    style={
                                        "textAlign": "center",
                                        "marginLeft": "12%",
                                        "paddingTop": "13%",
                                        "marginRight": "6%",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Elbow Up",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "position": "relative",
                                                "left": "19px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H6(
                                                    "Shoulder Up",
                                                    style={
                                                        "textAlign": "center",
                                                        "font-size": "1.1rem",
                                                        "position": "relative",
                                                        "top": "21px",
                                                        "width": "26%",
                                                        "left": "-6px",
                                                    },
                                                    className="three columns",
                                                ),
                                                daq.Joystick(
                                                    id="elbow-shoulder-move",
                                                    force=0,
                                                    className="four columns",
                                                ),
                                                html.H6(
                                                    "Shoulder Down",
                                                    style={
                                                        "textAlign": "center",
                                                        "font-size": "1.1rem",
                                                        "position": "relative",
                                                        "top": "22px",
                                                        "left": "54px",
                                                        "width": "26%",
                                                    },
                                                    className="three columns",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                        html.H6(
                                            "Elbow Down",
                                            style={
                                                "textAlign": "center",
                                                "font-size": "1.1rem",
                                                "left": "19px",
                                                "position": "relative",
                                            },
                                        ),
                                    ],
                                    className="six columns",
                                    style={"paddingTop": "3%"},
                                ),
                            ],
                            className="row",
                            style={
                                "marginTop": "3%",
                                "position": "absolute",
                                "left": "32.5%",
                            },
                        )
                    ]
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "border": "11px solid #A2B1C6",
                "border-radius": "150px",
                "height": "75%",
                "width": "75%",
                "marginLeft": "11%",
                "marginTop": "8%",
                "box-shadow": "16px 10px 8px 0px #506784",
            },
        ),
        html.Div(
            [
                html.A(
                    href="#open-modal",
                    children=[
                        html.Div(
                            [html.H1(" ")],
                            style={
                                "width": "30px",
                                "height": "7px",
                                "background-color": "#A2B1C6",
                                "border": "1px solid #A2B1C6",
                                "border-radius": "20px",
                                "position": "absolute",
                                "top": "232px",
                                "left": "345px",
                            },
                        )
                    ],
                ),
                html.Div(
                    id="open-modal",
                    className="modal-window",
                    style={"background-color": "rgba(162,177,198, 0.75)"},
                    children=[
                        html.A(
                            "Close",
                            href="#modal-close",
                            title="Close",
                            className="modal-close",
                            style={"font-size": "125%"},
                        ),
                        html.Div(
                            style={
                                "border": "2px solid #2a3f5f",
                                "border-radius": "10px",
                                "color": "#2a3f5f",
                            },
                            children=[
                                html.H1(
                                    "Read Me",
                                    style={
                                        "textAlign": "left",
                                        "text-decoration": "underline",
                                        "font-size": "2em",
                                    },
                                ),
                                html.H6(
                                    "This application was made to \
                                    control the Robotic Arm Edge using \
                                    the USB interface package. This \
                                    application can be controlled \
                                    wirelessly using WI-FI. See it \
                                    in action, by clicking \
                                    on the Dash DAQ logo and reading the \
                                    blog post titled, '\
                                    Robotic Arm Edge'."
                                ),
                            ],
                        ),
                    ],
                ),
                html.H6(
                    "Read Me",
                    style={
                        "position": "absolute",
                        "top": "238px",
                        "left": "339px",
                        "font-size": "1.1rem",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(id="wrist-grip-hold"),
                html.Div(id="elbow-shoulder-hold"),
                html.Div(id="LED-base-hold"),
            ],
            style={"visibility": "hidden"},
        ),
    ],
    style={
        "padding": "0px 10px 0px 10px",
        "margin": "auto",
        "width": "693px",
        "height": "560px",
        "position": "absolute",
        "top": "0",
        "bottom": "0",
        "left": "0",
        "right": "0",
        "border": "5px solid #A2B1C6",
    },
)

# Base Led move
@app.callback(
    Output("LED-base-hold", "children"),
    [Input("LED-base-move", "angle"), 
    Input("LED-base-move", "force")],
)
def elbow_shoulder_move(angle, force):
    if angle is None:
        return None
    elif angle < 135 and angle > 45:  # UP
        led_color = "#00cc96"
        return led_color
    elif angle < 315 and angle > 225:  # DOWN
        led_color = "#EF553B"
        return led_color
    


@app.callback(
    Output("LED-state", "color"), 
    [Input("LED-base-hold", "children")]
)
def LED_ON_OFF(LED_color):
    if LED_color is None:
        return None
    return LED_color


if __name__ == "__main__":
    app.run_server(debug=True)
