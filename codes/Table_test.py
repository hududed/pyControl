import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd

from time import sleep

# from pymeasure.instruments.newport import ESP300

# ctrl = ESP300("GPIB0::3::INSTR")  # XYZ controller

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

app.layout = html.Div(
    [
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

        html.Div(
            [
                html.Div(
                    [
                        html.H3("Training Set Table")
                    ], className='Title'
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='table',
                            columns=(
                                    [{'id': 'Model', 'name': 'Model'}] +
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
                html.Div(
                    [
                        dcc.Graph(id="table-output"),
                    ],
                    className='row',
                    style={
                        "display": "flex",
                        # "visibility": "hidden"
                    }
                ),
            ],
            className="eight columns",
            style={
                "border-radius": "5px",
                "border-width": "5px",
                "border": "1px solid rgb(216, 216, 216)",
            },
        ),

        # Placeholder Divs
        html.Div(
            [
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
                # html.Div(id="velocity-store"),
                # dcc.Interval(id="velocity-interval", interval=360000, n_intervals=0),
            ],
            # style={"visibility": "hidden"},
        ),

    ],

)


#
# def enable():
#     ctrl.x.enable()
#     ctrl.y.enable()
#     ctrl.phi.enable()


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
#         # x = "{}".format(df.iloc[0][1])
#         # ctrl.x.position = float(x)
#         # y = "{}".format(df.iloc[0][2])
#         # ctrl.x.position = float(y)
#         # z = "{}".format(df.iloc[0][3])
#         # ctrl.x.position = float(z)



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
        return 'X: {}, Y: {}, Z: {}.'.format(df.iloc[0][1], df.iloc[0][2], df.iloc[0][3])
        # [[col['name'], df[col['id']]] for col in columns]


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
# else:
#     return
# def display_output(rows, columns):
#     df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
#     # print(df.iloc[0])
#
#
#
#     return {
#         'data': [
#             {
#                 'type': 'parcoords',
#                 'dimensions': [{
#                     'label': col['name'],
#                     'values': df[col['id']]
#                 } for col in columns]
#             }
#         ]
#     }


if __name__ == '__main__':
    app.run_server(port=7000, debug=True)
