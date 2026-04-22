from dash import Input, Output
import plotly.express as px

from dashboard.data_loader import DashboardData
from models.lag_detector import find_best_lag, interpret_lag

data = DashboardData()

def register_signal_callbacks(app):

    @app.callback(
        Output("signal-x", "options"),
        Output("signal-y", "options"),
        Input("signal-x", "id")  # dummy trigger
    )
    def populate_dropdowns(_):
        cols = data.get_columns()
        opts = [{"label": c, "value": c} for c in cols]
        return opts, opts

    @app.callback(
        Output("correlation-graph", "figure"),
        Output("lag-interpretation", "children"),
        Input("signal-x", "value"),
        Input("signal-y", "value")
    )
    def update_signal(x, y):

        if not x or not y:
            return {}, ""

        corr_df = data.get_cross_corr(x, y)

        fig = px.bar(
            corr_df,
            x="lag",
            y="correlation",
            title=f"Lag Correlation: {x} vs {y}"
        )

        best = find_best_lag(corr_df)
        text = interpret_lag(best, x, y)

        return fig, text