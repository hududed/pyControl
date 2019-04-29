import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from ftd2xx import listDevices
from time import sleep
from pymeasure.instruments.newport import ESP300

FTDIresources = listDevices()
serial = FTDIresources[0]
ctrl = ESP300("GPIB0::3::INSTR")

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
        html.Div([
                html.H2("AutoPatterning Setup",
                        style={'color': '#1d1d1d',
                               'margin-left': '2%',
                               'display': 'inline-block',
                               'text-align': 'center'})
                # html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                #              "excel/dash-daq/dash-daq-logo-by-plotly-stripe.png",
                #          style={'position': 'relative',
                #                 'float': 'right',
                #                 'right': '10px',
                #                 'height': '75px'})
            ], className='banner', style={
                'height': '75px',
                'margin': '0px -10px 10px',
                'background-color': '#EBF0F8',
                }),
        html.Div([
            html.H3("XYZ Controller Info", className="six columns"),
        ],  className='row Title'),
        html.Div([
            # html.Div([
            #     html.Div("Attached:", className="two columns"),
            #     html.Div("Disconnected",
            #              id="device-attached",
            #              className="nine columns"),
            #     daq.Indicator(
            #         id="connection-est",
            #         value=False,
            #         className="one columns",
            #         style={'margin': '6px'}
            #     )
            # ], className="row attachment"),
            # html.Hr(style={'marginBottom': '0', 'marginTop': '0'}),
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
        daq.BooleanSwitch(
            id='my-boolean-switch',
            on=False,
        ),
        html.Div(id='boolean-switch-output')








    ], className="six columns"
)

app.layout = root_layout

# Enable laser

@app.callback(
    Output('boolean-switch-output', 'children'),
    [Input('my-boolean-switch', 'on')])

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

@app.callback(Output("device-version", "children"),
              [Input("connection-est", "value")])
def device_name(connection):
    if connection:
        return str(ctrl.id)

# def enable_laser(stop):
#     if stop >= 1:
#         laser('on')
#     else:
#         laser('off')

#
# def update_output(on):
#     return 'the switch is {}' .format(on)


if __name__ == '__main__':
    app.run_server(debug=True)
