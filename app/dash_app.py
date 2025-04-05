# Dash App for Visualizing Cache Stats
# Run this separately after the Flask app is running

import dash
from dash import html, dcc
import plotly.graph_objs as go
import requests
import time

app = dash.Dash(__name__)
app.title = "Cache Strategy Dashboard"

# ----------------------
# Helper Functions
# ----------------------


def get_stats():
    try:
        return requests.get("http://localhost:5000/stats").json()
    except:
        return {}


def get_logs():
    try:
        return requests.get("http://localhost:5000/log").json()
    except:
        return []


# ----------------------
# Layout
# ----------------------

app.layout = html.Div(style={"fontFamily": "Arial", "padding": 20}, children=[
    html.H1("🧠 Web Cache Strategy Dashboard"),
    dcc.Interval(id="interval", interval=2000, n_intervals=0),

    html.Div([
        html.Div([
            dcc.Graph(id="stats-graph")
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="timeline-graph")
        ], style={"width": "48%", "display": "inline-block"})
    ])
])

# ----------------------
# Callbacks
# ----------------------


@app.callback(
    dash.dependencies.Output("stats-graph", "figure"),
    [dash.dependencies.Input("interval", "n_intervals")]
)
def update_stats(n):
    stats = get_stats()
    labels = list(stats.keys())
    values = list(stats.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title="Cache Hits / Misses / Updates", margin={"t": 50})
    return fig


@app.callback(
    dash.dependencies.Output("timeline-graph", "figure"),
    [dash.dependencies.Input("interval", "n_intervals")]
)
def update_timeline(n):
    logs = get_logs()
    if not logs:
        return go.Figure()

    times = [time.strftime('%H:%M:%S', time.localtime(e['time'])) for e in logs]
    events = [e['event'] for e in logs]

    fig = go.Figure(data=[
        go.Scatter(x=times, y=events, mode='markers+lines', marker=dict(size=10))
    ])
    fig.update_layout(title="Cache Events Timeline", xaxis_title="Time", yaxis_title="Event")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
