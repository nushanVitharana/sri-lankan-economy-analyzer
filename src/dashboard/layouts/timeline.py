from dash import dcc, html

from dashboard.data_loader import DashboardData


data = DashboardData()


def timeline_layout():
    options = [
        {"label": data.get_label(column), "value": column}
        for column in data.get_display_columns()
    ]

    return html.Div(
        [
            html.Div(
                [
                    html.Label("Indicator", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="timeline-indicator",
                        options=options,
                        value=options[0]["value"] if options else None,
                        clearable=False,
                    ),
                ],
                style={"maxWidth": "460px", "marginBottom": "18px"},
            ),
            html.Div(
                "Use this to inspect richer stress indicators such as import cover, current account pressure, and the composite macro stress index.",
                style={"color": "#5b6670", "marginBottom": "16px"},
            ),
            dcc.Graph(id="timeline-chart"),
        ]
    )
