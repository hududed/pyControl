import dash
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import ftd2xx  # Thorlabs MFF101
import ftd2xx.defines as constants
from ftd2xx import listDevices
from time import sleep

FTDIresources = listDevices()
serial = FTDIresources[0]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    daq.BooleanSwitch(
        id='my-boolean-switch',
        on=False,
    ),
    html.Div(id='boolean-switch-output')
])

# Enable laser

@app.callback(
    Output('boolean-switch-output', 'children'),
    [Input('my-boolean-switch', 'on')])

def laser(on):
    """Switch 'on' or 'off'"""
    serial = FTDIresources[0]
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
