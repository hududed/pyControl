import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from time import sleep
from pymeasure.instruments.newport import ESP300

serial = b'37000805'
ctrl = ESP300("GPIB0::3::INSTR")

def defaultset():  # dont think this works as it should.
    ctrl.data_bits = 8
    ctrl.baud_rate = 19200
    ctrl.StopBits = 1
    ctrl.read_termination = '\r\n'
    ctrl.write_termination = '\r'

app = dash.Dash(__name__)
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
for css in external_css:
    app.css.append_css({"external_url": css})

# root_layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#
#     html.Div([
#         daq.ToggleSwitch(
#             id='toggleTheme',
#             style={
#                 'position': 'absolute',
#                 'transform': 'translate(-50%, 20%)'
#             },
#             size=25
#         ),
#     ], id="toggleDiv",
#         style={
#             'width': 'fit-content',
#             'margin': '0 auto'
#         }),
#
#     html.Div(id='page-content'),
# ])

root_layout = html.Div(
    [
        dcc.Interval(id="upon-load", interval=1000, n_intervals=0),
        dcc.Interval(id="stream", interval=500, n_intervals=0),
        html.Div([
                html.H2("AutoPatterning Setup",
                        style={'color': '#1d1d1d',
                               'margin-left': '2%',
                               'display': 'inline-block',
                               'text-align': 'center'}),
                # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                #              "excel/dash-daq/dash-daq-logo-by-plotly-stripe.png",
                #          style={'position': 'relative',
                #                 'float': 'right',
                #                 'right': '10px',
                #                 'height': '75px'})
        ], className='banner',
            style={
                'height': '75px',
                'margin': '0px -10px 10px',
                'background-color': '#EBF0F8',
            },
        ),
        html.Div([
            html.H3("XYZ Controller Info", className="six columns"),
        ],  className='row Title'),
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
            # html.Div([
            #     html.Div("Channel: ", className="two columns"),
            #     html.Div("Disconnected",
            #              id="device-channel",
            #              className="four columns"),
            # ], className="row channel")
        ]),

        html.Div([
            html.Div([
                html.H3("XYZ-Setting")
            ], className='Title'),
            html.Div([
                html.Div([
                    dcc.Input(
                        id="input-submit",
                        placeholder="x-position",
                        type="text",
                        value="",
                        style={
                            "width": "35%",
                            "marginLeft": "13.87%",
                            "marginTop": "3%",
                        },
                    ),
                    html.Div(id='output-submit')
                ], className="row"),
                # html.Div([
                #     dcc.Input(
                #         id="y-set",
                #         placeholder="y-position",
                #         type="text",
                #         value="",
                #         style={
                #             "width": "35%",
                #             "marginLeft": "13.87%",
                #             "marginTop": "3%",
                #         },
                #     ),
                # ], className="row"),
                # html.Div([
                #     dcc.Input(
                #         id="z-set",
                #         placeholder="z-position",
                #         type="text",
                #         value="",
                #         style={
                #             "width": "35%",
                #             "marginLeft": "13.87%",
                #             "marginTop": "3%",
                #         },
                #     ),
                # ], className="row"),
            ]),
        ], className="three columns"),

        html.Div([
            html.Div([
                html.H3("XYZ-Position")
            ], className='Title'),
            html.Div([
                html.Div([
                    html.Div(
                        "X-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="x-value",
                        className="two columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "mm",
                        className="one columns")
                ], className="row"),
                html.Div([
                    html.Div(
                        "Y-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="y-value",
                        className="two columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "mm",
                        className="one columns")
                ], className="row"),
                html.Div([
                    html.Div(
                        "Z-axis:",
                        style={'textAlign': 'right'},
                        className="three columns"),
                    html.Div(
                        id="z-value",
                        className="two columns",
                        style={'marginRight': '20px'}),
                    html.Div(
                        "mm",
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
        ], className="five columns"),

        html.Div([
            html.Div([
                html.H3("Laser Settings")
            ], className='Title'),
            html.Div([
                daq.BooleanSwitch(
                id='flipper-switch',
                on=False,
            ),
            html.Div(
                id='flipper-switch-output')
            ], className="row"),
        ], className='three columns')





    ], className="twelve columns"
)

app.layout = root_layout


# # Enable Preset Settings
# @app.callback(
#     Output("pre-settings", "disabled"),
#     [Input("x-set", "value")]
#     # Input("y-set", "value"),
#     # Input("z-set", "value")],
# )
# def presetting_enable(xpos, ypos, zpos):
#     if (xpos != "") or (ypos != "") and (zpos != ""):
#         return False
#     else:
#         return True

# Preset Settings
@app.callback(
    Output("output-submit", "children"),
    # [Input("pre-settings", "value")],
    [Input("input-submit", "n_submit")],
    [State('input-submit', 'value')]
    # State("y-set", "value"),
    # State("z-set", "value")]
    # State("step-size", "value"),
    # State("acceleration-set", "value"),
    # State("baudrate", "value")]
)
def moving_x(ns1, input1):
    # a = float(input_data)
    # ctrl.x.position = float(input1)
    return u'moved to "{}"'.format(input1)
    # if (
    #     (xpos != "")
    #     # and (ypos != "")
    #     # and (zpos != "")
    #     # and (preset_switch == True)
    # ):
    #     ctrl.x.position = xpos
    #     # ser.baudrate = baud
    #     # command = "/{}m{}h{}j{}L{}RR\r".format(
    #     #     address, motor_current, hold_current, stepsize, accel_set
    #     # )
    #     # ser.flush()
    #     # ser.write(command.encode("utf-8"))
    #     # response = str(ser.read(7)) # Make response equal to none if freezing
    #     return ctrl.x.position
    # else:
    #     response = "x not read"
    #     return response


### Enable laser ###
@app.callback(
    Output('flipper-switch-output', 'children'),
    [Input('flipper-switch', 'on')])
def laser(on):
    """Switch 'on' or 'off'"""
    # Raw byte commands for "MGMSG_MOT_MOVE_JOG".
    #     on = b"\x6A\x04\x00\x01\x21\x01"  # x01 up
    #     off = b"\x6A\x04\x00\x02\x21\x01"  # x02 down

    if on:
        motor = ftd2xx.openEx(serial)
        print(motor.getDeviceInfo())
        motor.setBaudRate(115200)
        motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
        sleep(.05)
        motor.purge()
        sleep(.05)
        motor.resetDevice()
        motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
        motor.setRts()

        # Send raw bytes to USB driver.
        motor.write(b"\x6A\x04\x00\x01\x21\x01")  # up or
        motor.close()
        return 'The laser is on : {}' .format(on)
    else:
        motor = ftd2xx.openEx(serial)
        print(motor.getDeviceInfo())
        motor.setBaudRate(115200)
        motor.setDataCharacteristics(constants.BITS_8, constants.STOP_BITS_1, constants.PARITY_NONE)
        sleep(.05)
        motor.purge()
        sleep(.05)
        motor.resetDevice()
        motor.setFlowControl(constants.FLOW_RTS_CTS, 0, 0)
        motor.setRts()

        # Send raw bytes to USB driver.
        motor.write(b"\x6A\x04\x00\x02\x21\x01")  # up or
        motor.close()
        return 'The laser is on : {}' .format(on)

### Status XYZ Positions ###
@app.callback(Output("x-value", "children"),
              [Input("stream", "n_intervals")],
              [State("connection-est", "value")])
def stream_x(_, connection):
    if connection:
        return ctrl.x.position
    return str(0)

# @app.callback(Output("y-value", "children"),
#               [Input("stream", "n_intervals")],
#               [State("connection-est", "value")])
# def stream_y(_, connection):
#     if connection:
#         return ctrl.y.position
#     return str(0)
#
# @app.callback(Output("z-value", "children"),
#               [Input("stream", "n_intervals")],
#               [State("connection-est", "value")])
# def stream_z(_, connection):
#     if connection:
#         return ctrl.phi.position
#     return str(0)


### XYZ Device Connection ###
@app.callback(Output("device-attached", "children"),
              [Input("connection-est", "value")])
def device_name(connection):
    if connection:
        return ctrl.name

@app.callback(Output("device-version", "children"),
              [Input("connection-est", "value")])
def device_version(connection):
    if connection:
        return ctrl.id


### Connection stream ###
@app.callback(Output("connection-est", "value"),
              [Input("upon-load", "n_intervals")])
def connection_established(_):
    if ctrl.name is not None:
        return True

@app.callback(Output("upon-load", "interval"),
              [Input("upon-load", "n_intervals"),
               Input("connection-est", "value")])
def load_once(_, connection):
    if connection is True:
        return 3.6E6
    return 1000


if __name__ == '__main__':
    defaultset()
    app.run_server(port=8800, debug=True)
