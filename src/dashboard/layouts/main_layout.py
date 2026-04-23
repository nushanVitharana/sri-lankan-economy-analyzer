from dash import html

from dashboard.data_loader import DashboardData
from dashboard.layouts.forecast_lab import forecast_lab_layout
from dashboard.layouts.signal_lab import signal_lab_layout
from dashboard.layouts.timeline import timeline_layout


data = DashboardData()


PAGE_STYLE = {
    "backgroundColor": "#f4f1ea",
    "minHeight": "100vh",
    "padding": "32px",
    "fontFamily": "Georgia, 'Times New Roman', serif",
    "color": "#1d2a33",
}

CARD_STYLE = {
    "backgroundColor": "#fffdf8",
    "border": "1px solid #d7cfbf",
    "borderRadius": "18px",
    "padding": "20px",
    "boxShadow": "0 10px 30px rgba(48, 57, 66, 0.08)",
}


def snapshot_cards():
    cards = []
    for card in data.get_snapshot_cards():
        cards.append(
            html.Div(
                [
                    html.Div(card["title"], style={"fontSize": "13px", "textTransform": "uppercase", "color": "#786a52"}),
                    html.Div(str(card["value"]), style={"fontSize": "30px", "fontWeight": "bold", "marginTop": "8px"}),
                    html.Div(card["subtitle"], style={"fontSize": "14px", "marginTop": "8px", "lineHeight": "1.4"}),
                ],
                style={**CARD_STYLE, "flex": "1", "minWidth": "220px"},
            )
        )
    return cards


def section_wrapper(title: str, description: str, content):
    return html.Div(
        [
            html.Div(
                [
                    html.H2(title, style={"marginBottom": "4px"}),
                    html.P(description, style={"marginTop": "0", "color": "#5b6670"}),
                ]
            ),
            content,
        ],
        style={**CARD_STYLE, "marginTop": "24px"},
    )


def create_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Sri Lankan Macro Risk Monitor", style={"fontSize": "14px", "textTransform": "uppercase", "letterSpacing": "1px", "color": "#8b5e34"}),
                    html.H1("Sri Lanka Crisis Dashboard", style={"marginBottom": "10px"}),
                    html.P(
                        "A richer macro view of external vulnerability, fiscal stress, monetary pressure, and household strain.",
                        style={"fontSize": "18px", "maxWidth": "900px", "lineHeight": "1.5", "color": "#47515a"},
                    ),
                ]
            ),
            html.Div(snapshot_cards(), style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginTop": "24px"}),
            section_wrapper(
                "Crisis Timeline",
                "Trace how a selected indicator evolved through the period and compare it with the current stress regime.",
                timeline_layout(),
            ),
            section_wrapper(
                "Signal Lab",
                "Explore which indicators tend to lead others and use lag relationships as early-warning signals.",
                signal_lab_layout(),
            ),
            section_wrapper(
                "Forecast Lab",
                "Inspect the latest forecast path, confidence bands, and systemwide causality structure.",
                forecast_lab_layout(),
            ),
        ],
        style=PAGE_STYLE,
    )
