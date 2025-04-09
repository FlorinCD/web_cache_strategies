# Dash App for Visualizing Cache Stats
# Run this separately after the Flask app is running

import dash
from dash import html, dcc
import plotly.graph_objs as go
import requests
import time
import json

app = dash.Dash(__name__)
app.title = "Cache Strategy Dashboard"

# ----------------------
# Helper Functions
# ----------------------


def get_stats(strategy_type):
    try:
        if strategy_type == "cache_first":
            return requests.get("http://localhost:5000/cache_first_stats").json()
        elif strategy_type == "network_first":
            return requests.get("http://localhost:5000/network_first_stats").json()
        elif strategy_type == "stale_while_revalidate":
            return requests.get("http://localhost:5000/stale_while_revalidate_stats").json()
        return json.dumps({"error": "Invalid strategy type"})
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
    strategy_type = "cache_first"  # here we decide what strategy to display, eg: "cache_first"

    if strategy_type == "cache_first":
        stats = get_stats(strategy_type)
        labels = list(stats.keys())
        values = list(stats.values())
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title="Hits / Misses / latency_hits / latency_misses", margin={"t": 50})
    elif strategy_type == "network_first":
        pass
    elif strategy_type == "stale_while_revalidate":
        pass
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
