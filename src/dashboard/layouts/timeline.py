from dash import html, dcc

def timeline_layout():
    return html.Div([

        html.H3("Crisis Timeline"),

        dcc.Dropdown(
            id="timeline-indicator",
            options=[
                {"label": "Reserves", "value": "reserves"},
                {"label": "Inflation", "value": "inflation"},
                {"label": "Debt", "value": "debt"}
            ],
            value="reserves"
        ),

        dcc.Graph(id="timeline-chart")

    ])