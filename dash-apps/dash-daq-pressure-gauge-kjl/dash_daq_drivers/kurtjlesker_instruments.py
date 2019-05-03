# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 15:15:48 2018

Driver(s) for Kurt J. Lesker Instruments

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

RESPONSE_BIT_NUM = 13
GAUGE_TYPES = ['CG', 'IG', 'AI']
INTERFACE = INTF_SERIAL
GAUGE_READY = 'status ok'
STATUS = {
    '00 ST OK': GAUGE_READY,
    '01 OVPRS': 'IG over pressure; AI pressure over 1100 Torr',
    '02 EMISS': 'Ie failure',
    '04 FLVLO': 'filament V low',
    '08 FLOPN': 'IG filament open; CG sensor wire is open circuit or \
CG cable unplugged',
    '10 DEGAS': 'upper pressure limit exceeded during DEGAS operation',
    '20 ICLOW': 'Ic too low',
    '40 FLVHI': 'filament V high',
    '?01 INVALID': 'The device does not exist',
    '?01 SYNTX ER': 'Unknown command'
}


def make_gauge_callback(name, instr, app, inputs):
    """generate a callback for the gauges which number can vary from instrument
        to instrument
    """
    @app.callback(
        Output('%s_gauge_%s' % (instr.unique_id(), name), 'value'),
        inputs)
    def update_gauge(interval_value):

        return instr.last_measure[name]

    update_gauge.__name__ = '%s_gauge_%s' % (instr.unique_id(), name)

    return update_gauge


class MGC4000(Instrument):

    def __init__(
        self,
        instr_port_name='',
        mock=False,
        instr_user_name='MGC 4000',
        theme='light',
        **kwargs
    ):

        # manage the presence of the keyword interface which will determine
        # which method of communication protocol this instrument will use
        if 'interface' in kwargs.keys():

            interface = kwargs.pop('interface')

        else:

            interface = INTERFACE

        instr_mesurands = {
            'CG1': 'mbar',
            'CG2': 'mbar',
            'CG3': 'mbar',
            'CG4': 'mbar'
        }

        super(MGC4000, self).__init__(instr_port_name,
                                      instr_id_name='MGC4000',
                                      instr_user_name=instr_user_name,
                                      mock_mode=mock,
                                      instr_intf=interface,
                                      baud_rate=19200,
                                      term_chars='\r',
                                      instr_mesurands=instr_mesurands,
                                      **kwargs)

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
            children='Connect',
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

    def generate_callbacks(self, app, inputs=[]):
        """assigns the callback for this instrument's instance"""
        for name in self.measure_params:
            make_gauge_callback(name, self, app, inputs)

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
            # exception for bad theme here

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

    def measure(self, instr_param):
        if instr_param in self.measure_params:
            # method to check the type and id of the gauge
            gtype, n = self.check_is_gauge(instr_param)
            if self.mock_mode:
                answer = 10 * np.random.random()
            else:
                if n is not None:
                    if self.is_gauge_ready(gtype, n):
                        answer = float(self.ask('#  RD%s%i' % (gtype, n)))
                    else:
                        print("gauge is not ready")
                        answer = np.nan
                else:
                    answer = np.nan
            self.last_measure[instr_param] = answer
            self.measured_data[instr_param].append(
                self.last_measure[instr_param]
            )
            # store the time at which the data was taken
            self.measured_data['%s_time' % instr_param].append(
                datetime.datetime.now()
            )
        else:
            print(
                "you are trying to measure a non existent instr_param : "
                + instr_param
            )
            print("existing instr_params :", self.measure_params)
            answer = np.nan

        return answer

    def read(self, num_bytes=RESPONSE_BIT_NUM):

        answer = super(MGC4000, self).read(num_bytes)

        if answer:
            if answer[0] == '*':
                # the first 3 characters after the * are only space for RS232
                # the last one is a \r
                return answer[4:-1]
            elif answer[0] == '?':
                return answer
            else:
                print('Invalid answer from %s' % (self))
                return None
        else:
            print('No answer recieved from %s' % (self))
            return None

    def ask(self, msg):
        return super(MGC4000, self).ask(msg, num_bytes=RESPONSE_BIT_NUM)

    def status(self, gtype='CG', n=None):
        """query the status of a given pressure gauge"""

        if n is None:
            gtype, n = self.check_is_gauge(gtype)

        answer = self.ask('#  RS%s%i' % (gtype, n))

        if answer in STATUS:
            return STATUS[answer]
        else:
            return answer

    def is_gauge_ready(self, gtype='CG', n=None):
        """tell us if the gauge is ready to be measured"""
        answer = self.status(gtype, n)
        return (answer == GAUGE_READY)

    def check_is_gauge(self, gauge):
        """check if the name assigned to the gauge is permitted"""
        n = int(gauge[2:])
        gtype = gauge[:2]

        if gtype in GAUGE_TYPES:
            return gtype, n
        else:
            # Raise an error here
            print("The gauge type '%s' is not accepted, please choose one \
from the list %s" % (gtype, GAUGE_TYPES))
            return None, None
