from dash import html, dcc

def signal_lab_layout():
    return html.Div([

        html.H3("Signal Lab — What leads what?"),

        html.Div([
            dcc.Dropdown(id="signal-x"),
            dcc.Dropdown(id="signal-y")
        ], style={"display": "flex", "gap": "10px"}),

        dcc.Graph(id="correlation-graph"),

        html.Div(id="lag-interpretation",
                 style={"marginTop": "20px", "fontWeight": "bold"})
    ])