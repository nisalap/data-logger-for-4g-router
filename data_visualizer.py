from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import datetime


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H2("Router Metrics"),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H4('RSRP'),
                        dcc.Graph(id="graph-rsrp")
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=[
                        html.H4('Tx Power'),
                        dcc.Graph(id="graph-txpower"),
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                )],
            style={'width': '100%', 'display': 'inline-block'}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H4('RSSI'),
                        dcc.Graph(id="graph-rssi")
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                ),
                html.Div(
                    children=[
                        html.H4('SINR'),
                        dcc.Graph(id="graph-sinr"),
                    ],
                    style={'width': '50%', 'display': 'inline-block'}
                )],
            style={'width': '100%', 'display': 'inline-block'}),
        dcc.Interval(
                id='interval-component',
                interval=5*1000, # in milliseconds
                n_intervals=30
            )
        ],
)


def get_state_file_prefix():
    dt = datetime.datetime.now()
    prefix = "logs/" + datetime.datetime.strftime(dt, "%Y-%m-%d")
    return prefix


@app.callback(
    Output("graph-rsrp", "figure"),
    Input("interval-component", "n_intervals"))
def update_line_chart(metric):
    df = pd.read_csv(get_state_file_prefix() + "_internet_stats.csv")
    # df = df.tail(300)
    metrics = ["RSRP"]
    fig = go.Figure()
    for each in metrics:
        fig.add_trace(go.Scatter(x=df.timestamp, y=df[each], mode='lines', name=each))
    return fig


@app.callback(
    Output("graph-txpower", "figure"),
    Input("interval-component", "n_intervals"))
def update_line_chart(metric):
    df = pd.read_csv(get_state_file_prefix() + "_internet_stats.csv")
    # df = df.tail(300)
    metrics = ["TZTXPOWER"]
    fig = go.Figure()
    for each in metrics:
        fig.add_trace(go.Scatter(x=df.timestamp, y=df[each], mode='lines', name=each))
    return fig

@app.callback(
    Output("graph-rssi", "figure"),
    Input("interval-component", "n_intervals"))
def update_line_chart(metric):
    df = pd.read_csv(get_state_file_prefix() + "_internet_stats.csv")
    # df = df.tail(300)
    metrics = ["RSSI"]
    fig = go.Figure()
    for each in metrics:
        fig.add_trace(go.Scatter(x=df.timestamp, y=df[each], mode='lines', name=each))
    return fig

@app.callback(
    Output("graph-sinr", "figure"),
    Input("interval-component", "n_intervals"))
def update_line_chart(metric):
    df = pd.read_csv(get_state_file_prefix() + "_internet_stats.csv")
    # df = df.tail(300)
    metrics = ["SINR"]
    fig = go.Figure()
    for each in metrics:
        fig.add_trace(go.Scatter(x=df.timestamp, y=df[each], mode='lines', name=each))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
