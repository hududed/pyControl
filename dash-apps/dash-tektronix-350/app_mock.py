import dash
from dash.dependencies import Input, Output
import dash_daq as daq
from dash_daq import DarkThemeProvider
import dash_html_components as html

import numpy as np
import dash_core_components as dcc
import plotly.graph_objs as go
from scipy import signal
from time import sleep
import os


app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

server = app.server

tabs = [
    {'label': 'Run #{}'.format(i), 'value': i} for i in range(1, 2)
]

tab = 1

runs = {}

root_layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div([
        daq.ToggleSwitch(
            id='toggleTheme',
            style={
                'position': 'absolute',
                'transform': 'translate(-50%, 20%)'
            },
            size=25
        ),
    ], id="toggleDiv",
             style={
                 'width': 'fit-content',
                 'margin': '0 auto'
             }),

    html.Div(id='page-content'),
])

light_layout = html.Div(id='container', children=[
    # Function Generator Panel - Left
    html.Div([
        html.H2("Dash DAQ: Function Generator & Oscilloscope Control Panel",
                style={
                    'color': '#EBF0F8',
                    'marginLeft': '40px',
                    'display': 'inline-block',
                    'text-align': 'center'
                }),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                 "excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png",
                 style={
                     'position': 'relative',
                     'float': 'right',
                     'right': '10px',
                     'height': '75px'
                 })
    ], className='banner',
             id='header',
             style={
                 'height': '75px',
                 'margin': '0px -10px 10px',
                 'backgroundColor': '#447EFF'
             }),

    html.Div([
        html.Div([
            html.Div([
                html.H3("POWER", id="power-title")
            ], className='Title'),
            html.Div([
                html.Div(
                    [
                        daq.PowerButton(
                            id='function-generator',
                            on='true',
                            label="Function Generator",
                            labelPosition='bottom',
                            color="#447EFF"),
                    ],
                    className='six columns',
                    style={'margin-bottom': '15px'}),
                html.Div(
                    [
                        daq.PowerButton(
                            id='oscilloscope',
                            on='true',
                            label="Oscilloscope",
                            labelPosition='bottom',
                            color="#447EFF")
                    ],
                    className='six columns',
                    style={'margin-bottom': '15px'}),
            ], style={'margin': '15px 0'})
        ], className='row power-settings-tab'),
        html.Div([
            html.Div(
                [html.H3("FUNCTION", id="function-title")],
                className='Title'),
            html.Div([
                daq.Knob(
                    value=1E6,
                    id="frequency-input",
                    label="Frequency (Hz)",
                    labelPosition="bottom",
                    size=75,
                    color="#447EFF",
                    scale={'interval': 1E5},
                    max=2.5E6,
                    min=1E5,
                    className='four columns'
                ),
                daq.Knob(
                    value=1,
                    id="amplitude-input",
                    label="Amplitude (mV)",
                    labelPosition="bottom",
                    size=75,
                    scale={'labelInterval': 10},
                    color="#447EFF",
                    max=10,
                    className='four columns'
                ),
                daq.Knob(
                    value=0,
                    id="offset-input",
                    label="Offset (mV)",
                    labelPosition="bottom",
                    size=75,
                    scale={'labelInterval': 10},
                    color="#447EFF",
                    max=10,
                    className='four columns'
                )], style={'marginLeft': '20%', 'textAlign': 'center'}),
            html.Div([
                daq.LEDDisplay(
                    id='frequency-display',
                    size=10, value=1E6,
                    label="Frequency (Hz)",
                    labelPosition="bottom",
                    color="#447EFF",
                    style={'marginBottom': '30px'},
                    className='four columns'),
                daq.LEDDisplay(
                    id='amplitude-display',
                    size=10,
                    value=1,
                    label="Amplitude (mV)",
                    labelPosition="bottom",
                    color="#447EFF",
                    className='four columns'),
                daq.LEDDisplay(
                    id='offset-display',
                    size=10,
                    value=10,
                    label="Offset (mV)",
                    labelPosition="bottom",
                    color="#447EFF",
                    className='four columns'),
            ], style={'marginLeft': '20%', 'textAlign': 'center'}),
            dcc.RadioItems(
                id='function-type',
                options=[
                    {'label': 'Sine', 'value': 'SIN'},
                    {'label': 'Square', 'value': 'SQUARE'},
                    {'label': 'Ramp', 'value': 'RAMP'},
                ],
                value='SIN',
                labelStyle={'display': 'inline-block'},
                style={'margin': '30px auto 0px auto',
                       'display': 'flex',
                       'width': '80%',
                       'alignItems': 'center',
                       'justifyContent': 'space-between'}
                )
            ], className='row power-settings-tab'),
        html.Hr(),
        daq.ColorPicker(
            id="color-picker",
            label="Color Picker",
            value=dict(hex="#447EFF"),
            size=164,
        ),
    ], className='four columns left-panel'),

    # Oscillator Panel - Right
    html.Div([
        html.Div([html.H3("GRAPH", id="graph-title")], className='Title'),
        dcc.Tabs(
            tabs=tabs,
            value=1,
            id='tabs',
            style={'backgroundColor': '#447EFF', 'height': '80%'},
        ),

        html.Div([
            html.Div([
                html.Div([
                    html.Div(
                        id="graph-info",
                        style={
                            'textAlign': 'center',
                            'fontSize': '16px', 'padding': '0px 5px',
                            'lineHeight': '20px',
                            'border': '2px solid #447EFF'}),
                ], className="row graph-param"),
            ], className="six columns"),
            html.Button('+',
                        id='new-tab',
                        type='submit',
                        style={'height': '20px', 'width': '20px',
                               'padding': '2px', 'lineHeight': '10px',
                               'float': 'right'}),
        ], className='row oscope-info', style={'margin': '15px'}),
        html.Hr(),
        dcc.Graph(
            id='oscope-graph',
            figure=dict(
                data=[dict(x=np.linspace(-0.000045, 0.000045, 1e3),
                           y=[0] * len(np.linspace(-0.000045, 0.000045, 1e3)),
                           marker={'color': '#2a3f5f'})],
                layout=go.Layout(
                    xaxis={'title': 's', 'color': '#506784',
                           'titlefont': dict(
                               family='Dosis',
                               size=15,
                           )},
                    yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                           'titlefont': dict(
                               family='Dosis',
                               size=15,
                           ), 'autorange': False, 'range': [-10, 10]},
                    margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                    plot_bgcolor='#F3F6FA',
                )
            ),
            config={'displayModeBar': True,
                    'modeBarButtonsToRemove': ['pan2d',
                                               'zoomIn2d',
                                               'zoomOut2d',
                                               'autoScale2d',
                                               'hoverClosestCartesian',
                                               'hoverCompareCartesian']}
        )
    ], className='seven columns right-panel')
])

dark_layout = DarkThemeProvider([
    html.Link(
        href="https://cdn.rawgit.com/samisahn/" +
        "dash-app-stylesheets/dc60135a/dash-tektronix-350-dark.css",
        rel="stylesheet"
    ),
    # Function Generator Panel - Left
    html.Div([
        html.H2("Dash DAQ: Function Generator & Oscilloscope Control Panel",
                style={
                    'color': 'white',
                    'marginLeft': '40px',
                    'display': 'inline-block',
                    'text-align': 'center'
                }),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/" +
                 "excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png",
                 style={
                     'position': 'relative',
                     'float': 'right',
                     'right': '10px',
                     'height': '75px'
                 })
    ], className='banner',
             id='dark-header',
             style={
                 'height': '75px',
                 'margin': '0px -10px 10px',
                 'backgroundColor': '#1d1d1d'
             }),

    html.Div([
        html.Div([
            html.Div([
                html.H3("POWER", id="power-title")
            ], className='Title'),
            html.Div([
                html.Div(
                    [
                        daq.PowerButton(
                            id='function-generator',
                            on='true',
                            label="Function Generator",
                            labelPosition='bottom',
                            color="#EBF0F8"),
                    ],
                    className='six columns',
                    style={'margin-bottom': '15px'}),
                html.Div(
                    [
                        daq.PowerButton(
                            id='oscilloscope',
                            on='true',
                            label="Oscilloscope",
                            labelPosition='bottom',
                            color="#EBF0F8")
                    ],
                    className='six columns',
                    style={'margin-bottom': '15px'}),
            ], style={'margin': '15px 0'})
        ], className='row power-settings-tab'),
        html.Div([
            html.Div(
                [html.H3("FUNCTION", id="function-title")],
                className='Title'),
            html.Div([
                daq.Knob(
                    value=1E6,
                    id="frequency-input",
                    label="Frequency (Hz)",
                    labelPosition="bottom",
                    size=75,
                    color="#EBF0F8",
                    scale={'interval': 1E5},
                    max=2.5E6,
                    min=1E5,
                    className='four columns'
                ),
                daq.Knob(
                    value=1,
                    id="amplitude-input",
                    label="Amplitude (mV)",
                    labelPosition="bottom",
                    size=75,
                    scale={'labelInterval': 10},
                    color="#EBF0F8",
                    max=10,
                    className='four columns'
                ),
                daq.Knob(
                    value=0,
                    id="offset-input",
                    label="Offset (mV)",
                    labelPosition="bottom",
                    size=75,
                    scale={'labelInterval': 10},
                    color="#EBF0F8",
                    max=10,
                    className='four columns'
                )], style={'marginLeft': '20%', 'textAlign': 'center'}),
            html.Div([
                daq.LEDDisplay(
                    id='frequency-display',
                    size=10, value=1E6,
                    label="Frequency (Hz)",
                    labelPosition="bottom",
                    color="#EBF0F8",
                    style={'marginBottom': '30px'},
                    className='four columns'),
                daq.LEDDisplay(
                    id='amplitude-display',
                    size=10,
                    value=1,
                    label="Amplitude (mV)",
                    labelPosition="bottom",
                    color="#EBF0F8",
                    className='four columns'),
                daq.LEDDisplay(
                    id='offset-display',
                    size=10,
                    value=10,
                    label="Offset (mV)",
                    labelPosition="bottom",
                    color="#EBF0F8",
                    className='four columns'),
            ], style={'marginLeft': '20%', 'textAlign': 'center'}),
            dcc.RadioItems(
                id='function-type',
                options=[
                    {'label': 'Sine', 'value': 'SIN'},
                    {'label': 'Square', 'value': 'SQUARE'},
                    {'label': 'Ramp', 'value': 'RAMP'},
                ],
                value='SIN',
                labelStyle={'display': 'inline-block'},
                style={'margin': '30px auto 0px auto',
                       'display': 'flex',
                       'width': '80%',
                       'alignItems': 'center',
                       'justifyContent': 'space-between'}
                )
            ], className='row power-settings-tab'),
        html.Hr(),
        daq.ColorPicker(
            id="color-picker",
            label="Color Picker",
            value=dict(hex="#EBF0F8"),
            size=164,
            theme={'dark': True}
        ),
    ], className='four columns left-panel'),

    # Oscillator Panel - Right
    html.Div([
        html.Div([html.H3("GRAPH", id="graph-title")], className='Title'),
        dcc.Tabs(
            tabs=tabs,
            value=1,
            id='dark-tabs',
            style={
                'backgroundColor': '#EBF0F8',
                'color': '#2a3f5f',
                'height': '80%'},
        ),

        html.Div([
            html.Div([
                html.Div([
                    html.Div(
                        id="dark-graph-info",
                        style={
                            'textAlign': 'center',
                            'fontSize': '16px',
                            'padding': '0px 5px',
                            'lineHeight': '20px',
                            'border': '2px solid #EBF0F8'}),
                ], className="row graph-param"),
            ], className="six columns"),
            html.Button('+',
                        id='new-tab',
                        type='submit',
                        style={
                            'backgroundColor': '#EBF0F8',
                            'height': '20px',
                            'width': '20px',
                            'padding': '2px',
                            'lineHeight': '10px',
                            'float': 'right'}),
        ], className='row oscope-info', style={'margin': '15px'}),
        html.Hr(),
        dcc.Graph(
            id='dark-oscope-graph',
            figure=dict(
                data=[dict(x=np.linspace(-0.000045, 0.000045, 1e3),
                           y=[0] * len(np.linspace(-0.000045, 0.000045, 1e3)),
                           marker={'color': '#f2f5fa'})],
                layout=go.Layout(
                    xaxis={'title': 's', 'color': '#EBF0F8',
                           'titlefont': dict(
                               family='Dosis',
                               size=15,
                           )},
                    yaxis={'title': 'Voltage (mV)', 'color': '#EBF0F8',
                           'titlefont': dict(
                               family='Dosis',
                               size=15,
                           ), 'autorange': False, 'range': [-10, 10]},
                    margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
            ),
            config={'displayModeBar': True,
                    'modeBarButtonsToRemove': ['pan2d',
                                               'zoomIn2d',
                                               'zoomOut2d',
                                               'autoScale2d',
                                               'hoverClosestCartesian',
                                               'hoverCompareCartesian']}
        )
    ], className='seven columns right-panel')
])


app.layout = root_layout


@app.callback(Output('toggleTheme', 'value'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dark':
        return True
    else:
        return False


@app.callback(Output('page-content', 'children'),
              [Input('toggleTheme', 'value')])
def page_layout(value):
    if value:
        return dark_layout
    else:
        return light_layout


# Callbacks for color picker
@app.callback(Output('frequency-input', 'color'),
              [Input('color-picker', 'value')])
def color_frequency_input(color):
    return color['hex']


@app.callback(Output('amplitude-input', 'color'),
              [Input('color-picker', 'value')])
def color_amplitude_input(color):
    return color['hex']


@app.callback(Output('offset-input', 'color'),
              [Input('color-picker', 'value')])
def color_offset_input(color):
    return color['hex']


@app.callback(Output('frequency-display', 'color'),
              [Input('color-picker', 'value')])
def color_frequency_display(color):
    return color['hex']


@app.callback(Output('amplitude-display', 'color'),
              [Input('color-picker', 'value')])
def color_amplitude_display(color):
    return color['hex']


@app.callback(Output('offset-display', 'color'),
              [Input('color-picker', 'value')])
def color_offset_display(color):
    return color['hex']


@app.callback(Output('graph-info', 'style'),
              [Input('color-picker', 'value')])
def color_info_border(color):
    return {'textAlign': 'center', 'border': "2px solid " + color['hex']}


@app.callback(Output('dark-graph-info', 'style'),
              [Input('color-picker', 'value')])
def color_dinfo_border(color):
    return {'textAlign': 'center', 'border': "2px solid " + color['hex']}


@app.callback(Output('tabs', 'style'),
              [Input('color-picker', 'value')])
def color_tabs_background(color):
    return {'backgroundColor': color['hex']}


@app.callback(Output('power-title', 'style'),
              [Input('color-picker', 'value')])
def color_power_title(color):
    return {'color': color['hex']}


@app.callback(Output('function-title', 'style'),
              [Input('color-picker', 'value')])
def color_function_title(color):
    return {'color': color['hex']}


@app.callback(Output('graph-title', 'style'),
              [Input('color-picker', 'value')])
def color_graph_title(color):
    return {'color': color['hex']}


@app.callback(Output('function-generator', 'color'),
              [Input('color-picker', 'value')])
def color_function_generator(color):
    return color['hex']


@app.callback(Output('oscilloscope', 'color'),
              [Input('color-picker', 'value')])
def color_oscilloscope(color):
    return color['hex']


@app.callback(Output('header', 'style'),
              [Input('color-picker', 'value')])
def color_banner(color):
    return {'backgroundColor': color['hex']}


# Callbacks for knob inputs
@app.callback(Output('frequency-display', 'value'),
              [Input('frequency-input', 'value')],)
def update_frequency_display(value):
    return value


@app.callback(Output('amplitude-display', 'value'),
              [Input('amplitude-input', 'value')],)
def update_amplitude_display(value):
    return value


@app.callback(Output('offset-display', 'value'),
              [Input('offset-input', 'value')])
def update_offset_display(value):
    return value


# Callbacks graph and graph info
@app.callback(Output('graph-info', 'children'),
              [Input('oscope-graph', 'figure'),
               Input('tabs', 'value')])
def update_info(_, value):
    if '' + str(value) in runs:
        return runs['' + str(value)][1]
    return "-"


@app.callback(Output('dark-graph-info', 'children'),
              [Input('dark-oscope-graph', 'figure'),
               Input('dark-tabs', 'value')])
def update_dinfo(_, value):
    if '' + str(value) in runs:
        return runs['' + str(value)][1]
    return "-"


@app.callback(Output('oscope-graph', 'figure'),
              [Input('tabs', 'value'),
               Input('frequency-input', 'value'),
               Input('function-type', 'value'),
               Input('amplitude-input', 'value'),
               Input('offset-input', 'value'),
               Input('oscilloscope', 'on'),
               Input('function-generator', 'on')])
def update_output(value, frequency, wave, amplitude, offset, osc_on, fnct_on):
    global tab
    time = np.linspace(-0.000045, 0.000045, 1e3)
    zero = dict(
        data=[dict(x=time, y=[0] * len(time),
                   marker={'color': '#2a3f5f'})],
        layout=go.Layout(
            xaxis={'title': 's', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   )},
            yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   ), 'autorange': False, 'range': [-10, 10]},
            margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
            plot_bgcolor='#F3F6FA',
        )
    )

    if not osc_on:
        return dict(
            data=[],
            layout=go.Layout(
                xaxis={'title': 's', 'color': '#506784', 'titlefont': dict(
                    family='Dosis',
                    size=15,
                ), 'showticklabels': False, 'ticks': '', 'zeroline': False},
                yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'showticklabels': False, 'zeroline': False},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='#506784',
            )
        )

    if not fnct_on:
        return zero

    if tab is not value:
        if '' + str(value) in runs:
            tab = value
            figure = runs['' + str(value)][0]
            figure['data'][0]['marker']['color'] = '#2a3f5f'
            figure['layout'] = go.Layout(
                xaxis={'title': 's', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       )},
                yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'autorange': False, 'range': [-10, 10]},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='#F3F6FA',
            )
            return figure
        tab = value
        return zero

    else:
        if wave == 'SIN':
            y = [float(offset) +
                 (float(amplitude) *
                  np.sin(np.radians(2.0 * np.pi * float(frequency) * t)))
                 for t in time]

        elif wave == 'SQUARE':
            y = [float(offset) +
                 float(amplitude) *
                 (signal.square(2.0 * np.pi * float(frequency)/10 * t))
                 for t in time]

        elif wave == 'RAMP':
            y = float(amplitude) * \
                (np.abs(signal.sawtooth(2*np.pi * float(frequency)/10 * time)))
            y = float(offset) + 2*y - float(amplitude)

        figure = dict(
            data=[dict(x=time, y=y, marker={'color': '#2a3f5f'})],
            layout=go.Layout(
                xaxis={'title': 's', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       )},
                yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'autorange': False, 'range': [-10, 10]},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='#F3F6FA',
            )
        )

        runs['' + str(value)] = figure, str(wave) + " | " + str(frequency) +\
            "Hz" + " | " + str(amplitude) + "mV" + " | " + str(offset) + "mV"

        # wait to update the runs variable
        sleep(0.10)

        return figure


@app.callback(Output('dark-oscope-graph', 'figure'),
              [Input('dark-tabs', 'value'),
               Input('frequency-input', 'value'),
               Input('function-type', 'value'),
               Input('amplitude-input', 'value'),
               Input('offset-input', 'value'),
               Input('oscilloscope', 'on'),
               Input('function-generator', 'on')])
def update_doutput(value, frequency, wave, amplitude, offset, osc_on, fnct_on):
    global tab
    time = np.linspace(-0.000045, 0.000045, 1e3)
    zero = dict(
        data=[dict(x=time, y=[0] * len(time), marker={'color': '#f2f5fa'})],
        layout=go.Layout(
            xaxis={'title': 's', 'color': '#EBF0F8',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   )},
            yaxis={'title': 'Voltage (mV)', 'color': '#EBF0F8',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   ), 'autorange': False, 'range': [-10, 10]},
            margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
    )

    if not osc_on:
        return dict(
            data=[],
            layout=go.Layout(
                xaxis={'title': 's', 'color': 'rgba(0,0,0,0)',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'showticklabels': False,
                       'ticks': '', 'zeroline': False},
                yaxis={'title': 'Voltage (mV)', 'color': 'rgba(0,0,0,0)',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'showticklabels': False, 'zeroline': False},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        )

    if not fnct_on:
        return zero

    if tab is not value:
        if '' + str(value) in runs:
            tab = value
            figure = runs['' + str(value)][0]
            figure['data'][0]['marker']['color'] = "#f2f5fa"
            figure['layout'] = go.Layout(
                xaxis={'title': 's', 'color': '#EBF0F8',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       )},
                yaxis={'title': 'Voltage (mV)', 'color': '#EBF0F8',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'autorange': False, 'range': [-10, 10]},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return figure
        tab = value
        return zero

    else:
        if wave == 'SIN':
            y = [float(offset) +
                 (float(amplitude) *
                  np.sin(np.radians(2.0 * np.pi * float(frequency) * t)))
                 for t in time]

        elif wave == 'SQUARE':
            y = [float(offset) +
                 float(amplitude) *
                 (signal.square(2.0 * np.pi * float(frequency)/10 * t))
                 for t in time]

        elif wave == 'RAMP':
            y = float(amplitude) * \
                (np.abs(signal.sawtooth(2*np.pi * float(frequency)/10 * time)))
            y = float(offset) + 2*y - float(amplitude)

        figure = dict(
            data=[dict(x=time, y=y, marker={'color': '#f2f5fa'})],
            layout=go.Layout(
                xaxis={'title': 's', 'color': '#EBF0F8',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       )},
                yaxis={'title': 'Voltage (mV)', 'color': '#EBF0F8',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'autorange': False, 'range': [-10, 10]},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        )

        runs['' + str(value)] = figure, str(wave) + " | " + str(frequency) +  \
            "Hz" + " | " + str(amplitude) + "mV" + " | " + str(offset) + "mV"

        # wait to update the runs variable
        sleep(0.10)

        return figure


@app.callback(Output('tabs', 'tabs'),
              [Input('new-tab', 'n_clicks')])
def new_tabs(n_clicks):
    if n_clicks is not None:
        tabs.append({'label': 'Run #' + str(tabs[-1]['value'] + 1),
                     'value': int(tabs[-1]['value']) + 1})
        return tabs
    return tabs


@app.callback(Output('dark-tabs', 'tabs'),
              [Input('new-tab', 'n_clicks')])
def new_dtabs(n_clicks):
    if n_clicks is not None:
        tabs.append({'label': 'Run #' + str(tabs[-1]['value'] + 1),
                     'value': int(tabs[-1]['value']) + 1})
        return tabs
    return tabs


external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/samisahn/dash-app-stylesheets/" +
                "eccb1a1a/dash-tektronix-350.css",
                "https://fonts.googleapis.com/css?family=Dosis"]

for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/' +
                        'ca0d8f02a1659981a0ea7f013a378bbd/raw/' +
                        'e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server(port=5500, debug=True)
