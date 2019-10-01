import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import pprint
import plotly.figure_factory as ff
import pandas as pd
from time import sleep

from time import sleep
from pymeasure.instruments.newport import ESP300

ctrl = ESP300("GPIB0::3::INSTR")  # XYZ controller

app = dash.Dash(__name__)
server = app.server
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True
#
# CSS Imports
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
]
for css in external_css:
    app.css.append_css({"external_url": css})

params = [
    'x', 'y', 'z'
]

app.layout = html.Div([
    dcc.Interval(id="upon-load", interval=1000, n_intervals=0),
    dcc.Interval(id="stream", interval=5000, n_intervals=0),

    html.Div(
        [
            html.H2("Johnson AutoBox",
                    className="five columns",
                    style={'color': '#1d1d1d',
                           'margin-left': '10%',
                           'display': 'inline-block',
                           'text-align': 'center'
                           },
                    ),
            daq.StopButton(
                id="start-stop",
                label="",
                className="three columns",
                n_clicks=0,
                style={
                    "paddingTop": "1%",
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                },
            ),
        ],
        className='row',
        style={
            'height': '75px',
            'margin': '0px -10px 10px',
            'background-color': '#EBF0F8'
        },
    ),

    html.Div([
        html.Div([
            html.H3("Training Set Table")
        ], className='Title'
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id='table',
                    columns=
                    (
                            [{'id': 'Model', 'name': 'Run'}] +
                            [{'id': p, 'name': p} for p in params]
                    ),
                    data=[
                        dict(Model=i, **{param: 0 for param in params})
                        for i in range(1, 3)
                    ],
                    style_cell_conditional=[
                        {'if': {'column_id': 'Model'},
                         'width': '100px'},
                        {'if': {'column_id': 'x'},
                         'width': '100px'},
                        {'if': {'column_id': 'y'},
                         'width': '100px'},
                        {'if': {'column_id': 'z'},
                         'width': '100px'},
                    ],
                    n_fixed_rows=1,
                    editable=True,
                ),
                html.Button(
                    'Execute',
                    id="run",
                    className="two columns",
                    n_clicks=0,
                    style={
                        # "float": "right",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "marginLeft": "2%",
                        "marginTop": "0%",
                    },
                ),
            ], className='row'
        ),
        html.Br(),
        # html.Div(
        #     [
        #         dcc.Graph(id="table-output"),
        #     ],
        #     className='row',
        #     style={
        #         "display": "flex",
        #         # "visibility": "hidden"
        #     }
        # ),
    ],
        className="eight columns",
        style={
            "border-radius": "5px",
            "border-width": "5px",
            "border": "1px solid rgb(216, 216, 216)",
        },
    ),

    # Placeholder Divs
    html.Div([
        # dcc.Graph(id='table-editing-simple-output')
        # html.Div(id="stop-all"),
        # html.Div(id="move-x"),
        # html.Div(id="move-y"),
        # html.Div(id="move-z"),
        # html.Div(id="start-pattern"),
        # html.Div(id="flipper-on"),
        # html.Div(id="laser-on"),
        # html.Div(id="power-set"),
        # html.Div(id="com-value"),
        html.Div(id="run-output"),
        html.Div(id='table-output')
        # html.Div(id="velocity-store"),
        # dcc.Interval(id="velocity-interval", interval=360000, n_intervals=0),
    ]),
    # style={"visibility": "hidden"}
])


# app.layout = html.Div([
#     dash_table.DataTable(
#         id='editing-prune-data',
#         columns=[{
#             'name': 'Column {}'.format(i),
#             'id': 'column-{}'.format(i)
#         } for i in range(1, 5)],
#         data=[
#             {'column-{}'.format(i): (j + (i-1)*5) for i in range(1, 5)}
#             for j in range(5)
#         ],
#         editable=True
#     ),
#     html.Div(id='editing-prune-data-output')
# ])

def enable():
    ctrl.x.enable()
    ctrl.y.enable()
    ctrl.phi.enable()


def motion_done():
    ctrl.x.motion_done
    ctrl.y.motion_done
    ctrl.phi.motion_done


def max_velocity():
    ctrl.x.velocity = 0.4
    ctrl.y.velocity = 0.4
    ctrl.phi.velocity = 0.4


# # Move Button X
# @app.callback(
#     [Output("table-output", "figure")],
#     [Input("run", "n_clicks"),
#      Input("table", "data"),
#      Input("table", "columns")],
#     # [State("table", "data"),
#     #  State("table", "columns")]
# )
# def run_spots(n_clicks, rows, columns):
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#
#     if n_clicks >= 1:
#
#         return {
#             'data': [
#                 {
#                     'type': 'parcoords',
#                     'dimensions': [{
#                         'label': col['name'],
#                         'values': df[col['id']]
#                     } for col in columns]
#                 }
#             ]
#         }
#
#         # return{
#         #     'data':[
#         #         [[col['name'], df[col['id']]]
#         #          for col in columns]
#         #     ]
#         # enable()
#         # x = "{}".format(value)
#         # ctrl.x.position = float(x)
#     else:
#         return

@app.callback(
    Output('run-output', 'children'),
    [Input("run", "n_clicks")],
    [State('table', 'data'),
     State('table', 'columns')]
)
def run_spots(n_clicks, rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

    if n_clicks >= 1:
        enable()
        max_velocity()

        for i in range(2):
            x = "{}".format(df.iloc[i][1])
            y = "{}".format(df.iloc[i][2])
            z = "{}".format(df.iloc[i][3])
            ctrl.x.position = float(x)
            ctrl.y.position = float(y)
            ctrl.phi.position = float(z)
            while not (ctrl.x.motion_done and ctrl.y.motion_done):
                sleep(1)

        # return 'X: {}, Y: {}, Z: {}.'.format(df.iloc[0][1], df.iloc[0][2], df.iloc[0][3])


# @app.callback(Output('table-output', 'children'),
#               [Input('run', 'n_clicks')],
#               [State('table', 'data')])
# def display_output(n_clicks, rows):
#     pruned_rows = []
#     for row in rows:
#         # require that all elements in a row are specified
#         # the pruning behavior that you need may be different than this
#         if all([cell != '' for cell in row.values()]):
#             pruned_rows.append(row)
#
#     if n_clicks >= 1:
#         return html.Div([
#             html.Div('Raw Data'),
#             html.Pre(pprint.pformat(rows)),
#             html.Hr(),
#             html.Div('Pruned Data'),
#             html.Pre(pprint.pformat(pruned_rows)),
#         ])


# @app.callback(
#     Output('table-output', 'figure'),
#     [Input('table', 'data'),
#      Input('table', 'columns')]
# )
# def display_output(data, columns):
#     df = pd.DataFrame(data, columns=[c['name'] for c in columns])
#     # new_table_figure = ff.create_table(df)
#     return {
#         'data':[{
#             'x': df.loc[0],
#             'type': 'text'
#         }]
#
#     }


# return {
#     # df.head()
#     'data': [
#         {
#             'type': 'parcoords',
#             'dimensions': [{
#                 'label': col['name'],
#                 'values': df[col['id']]
#             } for col in columns]
#         }
#     ]
# }


if __name__ == '__main__':
    app.run_server(debug=True)
