# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:12:03 2018

Driver(s) for Pfeiffer Instruments

@author: Pierre-Francois Duc
"""

# In[]:
# Import required libraries
import numpy as np
import datetime

import dash_html_components as html
import dash_core_components as dcc
from dash_daq import Gauge, StopButton, PowerButton, Indicator, \
    DarkThemeProvider
from dash.dependencies import Output

from .generic_instruments import Instrument, INTF_SERIAL


def automatic_gauge_value_callback(name, instr, app, inputs):
    """generate a callback for the gauges which number can vary from instrument
        to instrument.
    """
    @app.callback(
        Output('%s_gauge_%s' % (instr.unique_id(), name), 'value'),
        inputs)
    def update_gauge(interval_value):
        return instr.last_measure[name]

    update_gauge.__name__ = '%s_gauge_%s' % (instr.unique_id(), name)

    return update_gauge


class TPG256A(Instrument):
    """instrument driver for Pfeiffer MaxiGauge TPG256A interfaced with Dash"""

    def __init__(
        self,
        instr_port_name='',
        mock=False,
        instr_user_name='Pfeiffer Gauge',
        gauge_dict=None,
        theme='light',
        **kwargs
    ):
        """
        instr_port_name (string) -- the communication port name to which the
        instrument is connected
        mock (bool) -- if set to True, there will be no actual connexion to
        an instrument
        instr_user_name (string) --  the name of the instrument chosen
        by the user
        instr_mesurands (dict) -- a dict of gauge names as keys and units as
        items
        theme (string) -- choice between 'light' or 'dark' theme
        kwargs (various) -- see instrument.Instrument for more details
        """

        if gauge_dict is None or not isinstance(gauge_dict, dict):
            # the parameters of the instrument
            instr_mesurands = {
                'P1': 'mbar',
                'P2': 'mbar',
                'P3': 'mbar',
                'P4': 'mbar'
            }
        else:
            instr_mesurands = gauge_dict

        super(TPG256A, self).__init__(
            instr_port_name,
            instr_id_name='TPG256A',
            instr_user_name=instr_user_name,
            mock_mode=mock,
            instr_intf=INTF_SERIAL,
            instr_mesurands=instr_mesurands,
            **kwargs
        )

        self.term_chars = "\n\r"

        # to record the time of each individual parameter measures
        for param_name in instr_mesurands:
            self.measured_data['%s_time' % param_name] = []

        # populate the dropdown with the instrument parameters
        dropdown_options = [{'label': lbl, 'value': lbl}
                            for lbl in self.measure_params]
        self.channels_dropdown = dcc.Dropdown(
            id="%s_channel" % (self.unique_id()),
            options=dropdown_options,
            value=self.measure_params,
            multi=True
        )

        # list of gauges for each parameters
        self.gauge_list = [
            Gauge(
                id='%s_gauge_%s' % (self.unique_id(), lbl),
                label='%s last value (%s)' % (lbl, self.params_units[lbl]),
                min=0.,
                max=10.,
                value=0.1,
                size=150,
                units='mbar',
                showCurrentValue=True
            )
            for lbl in self.measure_params
        ]

        # an input to choose the COM port to connect to the instrument
        self.connexion_input = dcc.Input(
            id='%s_instr_port' % (self.unique_id()),
            placeholder='Enter port name...',
            type='text',
            value=''
        )

        # a button which will initiate the connexion to the instrument
        self.connexion_button = StopButton(
            id='%s_instr_port_btn' % (self.unique_id()),
            buttonText='Connect',
            disabled=True
        )

        self.power_btn = PowerButton(
            id='%s_power_button' % (self.unique_id()),
            on='false'
        )

        self.mock_indicator = Indicator(
            id='%s_mock_indicator' % (self.unique_id()),
            value=self.mock_mode
        )

        # create the interface of the instrument
        self.control_components = self.setup_layout(theme)

    def setup_layout(self, theme='light'):
        """returns a layout of the controls in html"""

        if theme == 'light':
            dark_theme = False
            bkg_color = '#F3F6FA'
        elif theme == 'dark':
            dark_theme = True
            bkg_color = '#2a3f5f'
        else:
            pass
            # exeption for bad theme here

        # setup the layout of the instrument

        html_layout = [
            html.Link(
                href="https://codepen.io/plotly/pen/EQZeaW.css",
                rel="stylesheet"
            ),
            # Instrument name and power button
            html.Div(
                id='instr_hdr',
                children=[
                    html.H3('%s' % self.instr_user_name),
                    html.Div(
                        id='power_btn',
                        children=[
                            self.power_btn
                        ],
                        className='power_btn',
                        style={'margin': '20px'}
                    )
                ],
                className='row',
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'vertical-align': 'middle'
                }
            ),
            # Instrument port and parameters input
            html.Div(
                id='%s_controls_div' % self.unique_id(),
                children=[
                    html.Label(
                        [
                            'Instrument Port ',
                            self.connexion_input
                        ],
                        style={'margin': '12px'}
                    ),
                    html.Div(
                        [
                            self.connexion_button,
                        ],
                        style={'margin': '12px'}
                    ),
                    html.Label(
                        [
                            'Instrument parameter(s)',
                            self.channels_dropdown
                        ],
                        style={'margin': '12px'}
                    ),
                    html.Div(
                        [
                            html.P('Is mock :'),
                            self.mock_indicator
                        ],
                        style={
                            'alignItems': 'center',
                            'vertical-align': 'middle',
                            'margin': '5px',
                            'display': 'flex',
                            'flexDirection': 'column',
                        }
                    )
                ],
                className='%s_controls_div' % self.unique_id(),
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'alignItems': 'center',
                    'justifyContent': 'space-between'
                }
            ),
            html.Div(
                id='%s_gauges_div' % self.unique_id(),
                children=[
                    html.Div(
                        self.gauge_list,
                        id='%s_gauges_div' % self.unique_id(),
                        style={
                            'display': 'flex',
                            'flexDirection': 'row',
                            'alignItems': 'center',
                            'justifyContent': 'space-between',
                            'background': bkg_color
                        }
                    )
                ],

            )
        ]

        if dark_theme:

            return html.Div(
                [
                    DarkThemeProvider(
                        children=html_layout
                    )
                ],
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'background': bkg_color
                }
            )
        else:

            return html.Div(
                [
                    html.Div(
                        children=html_layout
                    )
                ],
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'background': bkg_color
                }
            )

    def generate_callbacks(self, app, inputs=[]):
        """assigns the callbacks for this instrument's instance"""

        # each parameter in related to a gauge which value need to be updated
        for param_name in self.measure_params:
            automatic_gauge_value_callback(param_name, self, app, inputs)

    def measure(self, instr_param='P1', **kwargs):
        """Initiate a measure by the instrument"""

        if instr_param in self.measure_params:
            if self.mock_mode:
                self.last_measure[instr_param] = 10 * np.random.random()
            else:
                # get the number of the pressure gauge
                sensor_id = int(instr_param[1])
                answer = self.ask('PR%d' % sensor_id)
                # expects : <status>,<pressure> <CR><LF>
                #          x       ,x.xxxEsx   <CR><LF>
                answer = answer[0].split(',')
                status = int(answer[0])
                pressure = float(answer[-1])

                if status == 0:
                    self.last_measure[instr_param] = pressure
                else:
                    # should raise an exception
                    print(PRESSURE_STATUS[status])
                    self.last_measure[instr_param] = np.nan

            self.measured_data[instr_param].append(
                self.last_measure[instr_param]
            )
            # store the time at which the data was taken
            self.measured_data['%s_time' % instr_param].append(
                datetime.datetime.now()
            )

            return self.last_measure[instr_param]

        else:
            print("Wrong instrument parameter : %s" % instr_param)
            print("existing channels :", self.measure_params)
            return None

    def ask(self, cmd):
        """sends a request to the MaxiGauge and get an answer

            HOST transmits
            message ended by self.term_chars

            cmd

            MG transmits
            positive acknowledgment of a received message
            <ACK> ended by self.term_chars

            self.handshake()

            The HOST invites the MG to transmit data

            <ENQ>

            MG transmits data ended by self.term_chars
        """
        if self.mock_mode:
            return cmd
        else:
            self.connexion.flushInput()
            self.write(cmd)

            # see if the MG responded by ACQ or NAK
            self.handshake()

            # Enquiry
            self.write(CTRL['ENQ'])

            answer = self.read()

            return answer

    def handshake(self):
        """Seek the acknowlegment from MG, or lack thereof"""

        response = self.read()

        if CTRL['ACQ'] in response:
            # what is expected normally
            pass
        elif CTRL['NAK'] in response:
            # raise error and analyse error code here
            pass
        else:
            # raise error because didn't get response at all
            pass


# Control Symbols from p.81 of the communication protocol of Pfeiffer TPG256A
CTRL = {
    'ETX': "\x03",  # End of Text (Ctrl-C)   Reset the interface
    'CR':  "\x0D",  # Carriage Return        Go to the beginning of line
    'LF':  "\x0A",  # Line Feed              Advance by one line
    'ENQ': "\x05",  # Enquiry                Request for data transmission
    'ACQ': "\x06",  # Acknowledge            Positive report signal
    'NAK': "\x15",  # Negative Acknowledge   Negative report signal
    'ESC': "\x1b",  # Escape
}

# pressure status from p.88
PRESSURE_STATUS = {
    0: 'Measurement data okay',
    1: 'Underrange',
    2: 'Overrange',
    3: 'Sensor error',
    4: 'Sensor off',
    5: 'No sensor',
    6: 'Identification error'
}
