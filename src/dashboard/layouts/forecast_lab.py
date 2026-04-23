from dash import dcc, html

from dashboard.data_loader import DashboardData


data = DashboardData()


def forecast_lab_layout():
    options = [{"label": data.get_label(c), "value": c} for c in data.get_display_columns()]

    return html.Div(
        [
            html.H3("Future Economic Outlook", style={"marginTop": "0"}),
            html.P(
                "Forecast enriched indicators and compare them with a causality map built from the broader macro dataset.",
                style={"color": "#5b6670"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Forecasting model", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id="forecast-model",
                                options=[
                                    {"label": "ARIMA / SARIMA", "value": "arima"},
                                    {"label": "VAR", "value": "var"},
                                ],
                                value="arima",
                                clearable=False,
                            ),
                        ],
                        style={"flex": "1", "minWidth": "220px"},
                    ),
                    html.Div(
                        [
                            html.Label("Indicator", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id="forecast-indicator",
                                options=options,
                                value=options[0]["value"] if options else None,
                                clearable=False,
                            ),
                        ],
                        style={"flex": "1", "minWidth": "220px"},
                    ),
                ],
                style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "20px"},
            ),
            html.Div(
                [
                    html.Label("Forecast horizon (years)", style={"fontWeight": "bold"}),
                    dcc.Slider(
                        id="forecast-steps",
                        min=1,
                        max=10,
                        step=1,
                        value=5,
                        marks={i: str(i) for i in range(1, 11)},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),
            dcc.Graph(id="forecast-graph"),
            html.Div(
                [
                    html.H4("Forecast Summary"),
                    html.Div(
                        id="forecast-summary",
                        style={"marginTop": "10px", "backgroundColor": "#f7f3eb", "borderRadius": "12px", "padding": "14px"},
                    ),
                ],
                style={"marginTop": "20px"},
            ),
            html.Div(
                [
                    html.H4("Causal Relationships (Granger Causality)"),
                    html.P("Lower p-values point to stronger evidence that one indicator systematically leads another."),
                    dcc.Graph(id="causality-heatmap", style={"height": "600px"}),
                ],
                style={"marginTop": "40px"},
            ),
        ]
    )
