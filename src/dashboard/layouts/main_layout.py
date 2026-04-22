from dash import html
from dashboard.layouts.timeline import timeline_layout
from dashboard.layouts.signal_lab import signal_lab_layout

def create_layout():
    return html.Div([
        html.H1("Sri Lanka Crisis Dashboard"),

        html.Div([
            timeline_layout(),
        ], style={"marginBottom": "40px"}),

        html.Div([
            signal_lab_layout(),
        ])
    ])