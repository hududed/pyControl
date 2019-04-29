import dash
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

from Phidget22.Devices.Accelerometer import Accelerometer
app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

server = app.server

ch = Accelerometer()

app.layout = html.Div([
    dcc.Interval(id="upon-load", interval=1000, n_intervals=0),
    dcc.Interval(id="stream", interval=500, n_intervals=0),
    html.Div([
        html.H2("Accelerometer Control Panel",
                style={'color': '#1d1d1d',
                       'margin-left': '2%',
                       'display': 'inline-block',
                       'text-align': 'center'}),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                     "excel/dash-daq/dash-daq-logo-by-plotly-stripe.png",
                 style={'position': 'relative',
                        'float': 'right',
                        'right': '10px',
                        'height': '75px'})
    ], className='banner', style={
        'height': '75px',
        'margin': '0px -10px 10px',
        'background-color': '#EBF0F8',
        }),
    html.Div([
        html.H3("Phidget Info", className="six columns"),
    ], className='row Title'),
    html.Div([
        html.Div([
            html.Div("Attached:", className="two columns"),
            html.Div("Disconnected",
                     id="device-attached",
                     className="nine columns"),
            daq.Indicator(
                id="connection-est",
                value=False,
                className="one columns",
                style={'margin': '6px'}
            )
        ], className="row attachment"),
        html.Hr(style={'marginBottom': '0', 'marginTop': '0'}),
        html.Div([
            html.Div("Version:", className="two columns"),
            html.Div("Disconnected",
                     id="device-version",
                     className="four columns"),
            html.Div("Serial Number:", className="two columns"),
            html.Div("Disconnected", id="device-serial")
        ], className="row version-serial"),
        html.Div([
            html.Div("Channel: ", className="two columns"),
            html.Div("Disconnected",
                     id="device-channel",
                     className="four columns"),
        ], className="row channel")
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.H3("Settings")
            ], className='Title'),
            html.Div([
                html.Div(id="channel-name"),
                html.Div([
                    html.Div([
                        "Change Interval"
                    ], className="three columns", style={'marginTop': '10px'}),
                    html.Div([
                        daq.Slider(
                            id="change-slider",
                            value=0,
                            min=1,
                            max=16,
                            step=0.01,
                            marks={i: str(i) for i in range(1, 17)},
                            className="eleven columns")
                    ], className="seven columns", style={'marginTop': '15px'}),
                    html.Div([
                        daq.LEDDisplay(
                            id="change-display",
                            value=1.00,
                            size=10,
                            style={'textAlign': 'center'})
                    ], className="two columns", style={'marginTop': '6px'})
                ], className="row stuff", style={'margin': '5px 0'}),
                html.Div([
                    html.Div([
                        "Data Interval"
                    ], className="three columns", style={'marginTop': '10px'}),
                    html.Div([
                        daq.Slider(
                            id="data-slider",
                            value=1000,
                            min=0,
                            max=1000,
                            step=None,
                            marks={0: "0", 1000: "1000"},
                            className="eleven columns"),
                    ], className="seven columns", style={'marginTop': '15px'}),
                    html.Div([
                        daq.LEDDisplay(
                            id="data-display",
                            value=500,
                            size=10,
                            style={'textAlign': 'center', 'marginTop': '5px'},)
                    ], className="two columns",)
                ], className="row stuff"),
            ]),
        ], className="six columns"),

        html.Div([
            html.Div([
                html.H3("G-Force")
            ], className='Title'),
            html.Div([
                html.Div([
                    html.Div(
                        "X-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="x-value",
                        className="one columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "g",
                        className="one columns")
                ], className="row"),
                html.Div([
                    html.Div(
                        "Y-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="y-value",
                        className="one columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "g",
                        className="one columns")
                ], className="row"),
                html.Div([
                    html.Div(
                        "Z-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="z-value",
                        className="one columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "g",
                        className="one columns")
                ], className="row"),
                html.Div([
                    html.Div(
                        "Time Stamp:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="time-stamp",
                        className="one columns",
                        style={'marginRight': '10px'}),
                    html.Div(
                        "s",
                        className="one columns")
                ], className="row"),
            ]),
        ], className="six columns"),
    ], className="row info"),

    html.Div([
        html.H3("Data")
    ], className='Title'),
    html.Div([
        html.Div([
            html.Div([
                daq.Gauge(
                    id="x-gauge",
                    label="X-axis",
                    labelPosition="bottom",
                    units="g",
                    value=0,
                    min=-8,
                    max=8,
                    showCurrentValue=True
                )
            ], className='six columns', style={'margin-bottom': '15px'}),

            html.Div([
                daq.Gauge(
                    id="y-gauge",
                    label="Y-axis",
                    labelPosition="bottom",
                    units="g",
                    value=0,
                    min=-8,
                    max=8,
                    showCurrentValue=True,
                )
            ], className='six columns'),
        ], style={'margin': '15px 0'})
    ], className='row x-y'),
    html.Div([
        html.Div([
            html.Div([
                daq.Gauge(
                    id="z-gauge",
                    label="Z-axis",
                    labelPosition="bottom",
                    units="g",
                    value=0,
                    min=-8,
                    max=8,
                    showCurrentValue=True,
                )
            ], className='six columns'),
        ])
    ], className='row z'),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


@app.callback(Output("x-value", "children"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_x(_, connection):
    if connection:
        return str(ch.getAcceleration()[0])
    return str(0)


@app.callback(Output("y-value", "children"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_y(_, connection):
    if connection:
        return str(ch.getAcceleration()[1])
    return str(0)


@app.callback(Output("z-value", "children"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_z(_, connection):
    if connection:
        return str(ch.getAcceleration()[2])
    return str(0)


@app.callback(Output("time-stamp", "children"),
              [Input("stream", "n_intervals")])
def time_stamp(time):
    return str(time)


@app.callback(Output("x-gauge", "value"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_xgauge(_, connection):
    if connection:
        return ch.getAcceleration()[0]


@app.callback(Output("y-gauge", "value"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_ygauge(_, connection):
    if connection:
        return ch.getAcceleration()[1]


@app.callback(Output("z-gauge", "value"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_zgauge(_, connection):
    if connection:
        return ch.getAcceleration()[2]


@app.callback(Output("device-attached", "children"),
              [Input("connection-est", "value")])
def device_name(connection):
    if connection:
        return str(ch.getDeviceName())


@app.callback(Output("device-version", "children"),
              [Input("connection-est", "value")])
def device_version(connection):
    if connection:
        return str(ch.getDeviceVersion())


@app.callback(Output("device-serial", "children"),
              [Input("connection-est", "value")])
def device_serial_number(connection):
    if connection:
        return str(ch.getDeviceSerialNumber())


@app.callback(Output("device-channel", "children"),
              [Input("connection-est", "value")])
def device_channel(connection):
    if connection is True:
        return str(ch.getChannel())


@app.callback(Output("connection-est", "value"),
              [Input("upon-load", "n_intervals")])
def connection_established(_):
    try:
        ch.openWaitForAttachment(5000)
    except:
        return False
    if ch.getDeviceName() is not None:
        return True


@app.callback(Output("upon-load", "interval"),
              [Input("upon-load", "n_intervals"),
               Input("connection-est", "value")])
def load_once(_, connection):
    if connection is True:
        return 3.6E6
    return 1000


@app.callback(Output("change-display", "value"),
              [Input("change-slider", "value")])
def update_change_display(value):
    ch.setAccelerationChangeTrigger(value)
    return value


@app.callback(Output("data-display", "value"),
              [Input("data-slider", "value")])
def update_data_display(value):
    return value


@app.callback(Output("stream", "interval"),
              [Input("data-slider", "value")])
def update_interval(value):
    if value is 0:
        return 3.6E6
    return value


@app.callback(Output("change-slider", "value"),
              [Input("connection-est", "value")])
def update_slider1(connection):
    if connection:
        return ch.getAccelerationChangeTrigger()


external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/samisahn/dash-app-stylesheets/" +
                "0925c314/dash-accelerometer.css",
                "https://fonts.googleapis.com/css?family=Dosis"]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(port=9000, debug=True)