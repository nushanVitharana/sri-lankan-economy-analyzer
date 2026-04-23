from dash import dcc, html

from dashboard.data_loader import DashboardData


data = DashboardData()


def signal_lab_layout():
    columns = data.get_display_columns()
    options = [{"label": data.get_label(c), "value": c} for c in columns]
    default_x = columns[0] if columns else None
    default_y = columns[1] if len(columns) > 1 else default_x

    return html.Div(
        [
            html.H3("What leads what?", style={"marginTop": "0"}),
            html.P(
                "Compare richer macro indicators to see whether stress in one area tends to show up earlier in another.",
                style={"color": "#5b6670"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Leading candidate", style={"fontWeight": "bold"}),
                            dcc.Dropdown(id="signal-x", options=options, value=default_x, clearable=False),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Label("Affected indicator", style={"fontWeight": "bold"}),
                            dcc.Dropdown(id="signal-y", options=options, value=default_y, clearable=False),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={"display": "flex", "gap": "14px", "flexWrap": "wrap"},
            ),
            dcc.Graph(id="correlation-graph"),
            html.Div(
                id="lag-interpretation",
                style={
                    "marginTop": "20px",
                    "fontWeight": "bold",
                    "backgroundColor": "#f7f3eb",
                    "borderRadius": "12px",
                    "padding": "14px",
                },
            ),
        ]
    )
