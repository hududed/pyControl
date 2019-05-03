# In[]:
# Import required libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, Event
from dash_daq import StopButton, Indicator, DarkThemeProvider, ToggleSwitch
import plotly.graph_objs as go

from dash_daq_drivers.kurtjlesker_instruments import MGC4000

# line colors
line_colors = ['#19d3f3', '#e763fa', '#00cc96', '#EF553B']

# font and background colors associated with each themes
bkg_color = {'dark': '#2a3f5f', 'light': '#F3F6FA'}
grid_color = {'dark': 'white', 'light': '#C8D4E3'}
text_color = {'dark': 'white', 'light': '#506784'}

# create a pressure gauge
pressure_gauge = MGC4000(mock=False)

# set the gauge inside the lab's instrument rack
instrument_rack = [pressure_gauge]


def is_instrument_port(port_name):
    """test if a string can be a com of gpib port"""
    answer = False
    if isinstance(port_name, str):
        ports = ['COM', 'com', 'GPIB0::', 'gpib0::']
        for port in ports:
            if port in port_name:
                answer = not (port == port_name)
    return answer


# Create controls using a function
def generate_lab_layout(instr_list, theme='light'):
    """generate the layout of the app from a list of instruments"""

    # the rack contains the control components of the instrument(s) interface
    rack = []
    for instr in instr_list:
        rack.append(instr.setup_layout(theme))

    html_layout = [
        html.Div(
            [
                # Instruments are in the instrument rack
                html.Div(
                    [
                        html.Div(
                            id='instrument-rack',
                            children=rack,
                            style={'width': '100%'}
                        ),
                        # Control panel for the data acquisition
                        html.Div(
                            id='measure-div',
                            children=[
                                StopButton(
                                    id='measureButton',
                                    buttonText='Start'
                                ),
                                Indicator(
                                    id='measuring',
                                    value=False,
                                    label='Is measuring :',
                                    labelPosition="top",
                                )
                            ],
                            style={
                                'width': '300px',
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                                'justifyContent': 'space-between'
                            }
                        )
                    ],
                    style={
                        'width': '100%',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [
                        # Display of the acquired data
                        dcc.Graph(
                            id='graph',
                            style={'width': '90 %'},
                            figure={
                                'data': [],
                                'layout': dict(
                                    paper_bgcolor=bkg_color[theme],
                                    plot_bgcolor=bkg_color[theme],
                                    font=dict(
                                        color=text_color[theme],
                                        size=15,
                                    )
                                )
                            }
                        )
                    ],
                    style={
                        'width': '100%',
                        'alignItems': 'center',
                    }
                ),
                html.Div(
                    [
                        dcc.Markdown('''
**What is this app about?**

This is an app to show the graphic elements of Dash DAQ used to create an
interface for the pressure gauges from Kurt J. Lesker multi gauges controller
MGC4000. This mock demo does not actually connect to a physical instrument
the values displayed are generated randomly for demonstration purposes.

**How to use the app**

Choose which gauge(s) you would like to measure values from in the
`Instrument parameters` combobox and click `Run`, the measured data will be
displayed on the graph below while the latest measured value will be
displayed on each gauge. You can purchase the Dash DAQ components at [
dashdaq.io](https://www.dashdaq.io/)''')
                    ],
                    style={
                        'max-width': '600px',
                        'margin': '15px auto 300 px auto',
                        'padding': '40px',
                        'box-shadow': '10px 10px 5px rgba(0, 0, 0, 0.2)',
                        'border': '1px solid #DFE8F3'
                    },
                    className="row"
                )
            ],
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'color': text_color[theme],
                'background': bkg_color[theme]
            }
        )
    ]

    if theme == 'dark':
        return DarkThemeProvider(children=html_layout)
    elif theme == 'light':
        return html.Div(children=html_layout)


root_layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        dcc.Interval(id='interval', interval=5000),
        html.Div(
            id='header',
            children=[
                html.H2('Dash DAQ: pressure gauge monitoring'),
                ToggleSwitch(
                    id='toggleTheme',
                    label='Dark/Light layout',
                    size=30,
                ),
                html.Img(
                    src='https://s3-us-west-1.amazonaws.com/plotly'
                        '-tutorials/excel/dash-daq/dash-daq-logo'
                        '-by-plotly-stripe.png',
                    style={
                        'height': '100',
                        'float': 'right',
                    }
                )
            ],
            className='banner',
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'space-between',
                'background': '#A2B1C6',
                'color': '#506784'
            }
        ),
        html.Div(
            id='page-content',
            children=generate_lab_layout(instrument_rack),
            style={'width': '100%'}
        ),
    ]
)

# Create dash app
app = dash.Dash('')
server = app.server
app.css.append_css(
    {'external_url': 'https://codepen.io/bachibouzouk/pen/dKJyoK.css'}
)

app.config.suppress_callback_exceptions = False
app.scripts.config.serve_locally = True

# In[]:
# Create app layout
app.layout = root_layout

# In[]:
# Create callbacks
# generate the callbacks between the instrument and the app
for instr in instrument_rack:
    instr.generate_callbacks(
        app,
        inputs=[Input('interval', 'n_intervals')]
    )


@app.callback(Output('page-content', 'children'),

              [Input('toggleTheme', 'value')])
def page_layout(value):
    if value:
        return generate_lab_layout(instrument_rack, 'dark')
    else:
        return generate_lab_layout(instrument_rack, 'light')


@app.callback(
    Output('measuring', 'value'),
    [],
    [State('measuring', 'value')],
    [Event('measureButton', 'click')]
)
def trigger_measure(is_measuring):
    return not is_measuring


@app.callback(
    Output('measureButton', 'buttonText'),
    [],
    [State('measuring', 'value')],
    [Event('measureButton', 'click')]
)
def change_measure_btn_label(is_measuring):
    if is_measuring:
        return 'Start'
    else:
        return 'Stop'


@app.callback(
    Output('%s_controls_div' % pressure_gauge.unique_id(), 'style'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')],
    [State('%s_controls_div' % pressure_gauge.unique_id(), 'style')],
)
def grey_out_controls_div(pwr_status, style_dict):
    answer = style_dict
    if pwr_status:
        answer['opacity'] = 1
    else:
        answer['opacity'] = 0.3
    return answer


@app.callback(
    Output('%s_gauges_div' % pressure_gauge.unique_id(), 'style'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')],
    [State('%s_gauges_div' % pressure_gauge.unique_id(), 'style')],
)
def grey_out_gauges_div(pwr_status, style_dict):
    answer = style_dict
    if pwr_status:
        answer['opacity'] = 1
    else:
        answer['opacity'] = 0.3
    return answer


@app.callback(
    Output('measure-div', 'style'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')],
    [State('measure-div', 'style')],
)
def grey_out_measuring_div(pwr_status, style_dict):
    answer = style_dict
    if pwr_status:
        answer['opacity'] = 1
    else:
        answer['opacity'] = 0.3
    return answer


@app.callback(
    Output('measureButton', 'disabled'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')]
)
def enable_measure_btn(pwr_status):
    return not pwr_status


@app.callback(
    Output('%s_instr_port' % pressure_gauge.unique_id(), 'value'),
    [
        Input('%s_power_button' % pressure_gauge.unique_id(), 'on'),
        Input('interval', 'n_intervals')
    ],
    [
        State('%s_instr_port' % (pressure_gauge.unique_id()), 'value'),
        State('%s_instr_port' % (pressure_gauge.unique_id()), 'placeholder')
    ]
)
def instrument_port_prevent_reset(pwr_status, n_intervals, text, placeholder):
    """prevents the input box's value to be reset by dcc.Interval"""
    if pwr_status:
        return text
    else:
        return placeholder


@app.callback(
    Output('%s_instr_port' % pressure_gauge.unique_id(), 'disabled'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')],
)
def enable_instrument_port_input(pwr_status):
    return not pwr_status


@app.callback(
    Output('%s_instr_port_btn' % pressure_gauge.unique_id(), 'disabled'),
    [Input('%s_power_button' % pressure_gauge.unique_id(), 'on')],
    [
        State('%s_instr_port' % (pressure_gauge.unique_id()), 'value'),
        State('%s_instr_port' % (pressure_gauge.unique_id()), 'placeholder')
    ],
    [Event('%s_instr_port' % pressure_gauge.unique_id(), 'change')]
)
def instrument_port_btn_update(pwr_status, text, placeholder):
    """enable or disable the connect button depending on the port name"""
    answer = True

    if text != placeholder:
        if is_instrument_port(text):
            answer = not pwr_status
    return answer


@app.callback(
    Output('%s_instr_port_btn' % pressure_gauge.unique_id(), 'n_clicks'),
    [],
    [State('%s_instr_port' % (pressure_gauge.unique_id()), 'value')],
    [Event('%s_instr_port_btn' % pressure_gauge.unique_id(), 'click')]
)
def instrument_port_btn_click(text):
    """reconnect the instrument to the new com port"""
    pressure_gauge.connect(text)
    return 0


@app.callback(
    Output('graph', 'figure'),
    [
        Input('interval', 'n_intervals'),
        Input('measuring', 'value'),
        Input('%s_channel' % (pressure_gauge.unique_id()), 'value'),
        Input('toggleTheme', 'value')
    ],
    [
        State('%s_power_button' % pressure_gauge.unique_id(), 'on')
    ]
)
def update_graph(
    n_interval,
    is_measuring,
    selected_params,
    is_dark_theme,
    pwr_status
):

    if is_dark_theme:
        theme = 'dark'
    else:
        theme = 'light'
    # here one should write the script of what the instrument do
    data_for_graph = []

    if pwr_status and is_measuring:
        for instr in instrument_rack:

            # triggers the measure on the selected channels
            if is_measuring:
                for instr_channel in selected_params:
                    instr.measure(instr_param='%s' % instr_channel)

            # collects the data measured by all channels to update the graph
            for instr_chan in selected_params:

                if instr.measured_data[instr_chan]:
                    xdata = 1000*instr.measured_data['%s_time' % instr_chan]
                    ydata = instr.measured_data[instr_chan]
                    data_for_graph.append(
                        go.Scatter(
                            x=xdata,
                            y=ydata,
                            mode='lines+markers',
                            name='%s:%s' % (instr, instr_chan),
                            line={
                                'width': 2
                            }
                        )
                    )

    return {
        'data': data_for_graph,
        'layout': dict(
            xaxis={
                'type': 'date',
                'title': 'Time',
                'color': text_color[theme],
                'gridcolor': grid_color[theme]
            },
            yaxis={
                'title': 'Pressure (mbar)',
                'gridcolor': grid_color[theme]
            },
            font=dict(
                color=text_color[theme],
                size=15,
            ),
            margin={'l': 100, 'b': 100, 't': 50, 'r': 20, 'pad': 0},
            plot_bgcolor=bkg_color[theme],
            paper_bgcolor=bkg_color[theme]
        )
    }


# In[]:
# Main
if __name__ == '__main__':
    app.run_server(debug=False)
