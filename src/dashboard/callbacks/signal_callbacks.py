from dash import Input, Output
import plotly.express as px

from dashboard.data_loader import DashboardData
from models.lag_detector import find_best_lag, interpret_lag


data = DashboardData()


def register_signal_callbacks(app):
    @app.callback(
        Output("signal-x", "options"),
        Output("signal-y", "options"),
        Input("signal-x", "id"),
    )
    def populate_dropdowns(_):
        cols = data.get_display_columns()
        options = [{"label": data.get_label(col), "value": col} for col in cols]
        return options, options

    @app.callback(
        Output("correlation-graph", "figure"),
        Output("lag-interpretation", "children"),
        Input("signal-x", "value"),
        Input("signal-y", "value"),
    )
    def update_signal(x, y):
        if not x or not y:
            return {}, ""

        corr_df = data.get_cross_corr(x, y)
        fig = px.bar(
            corr_df,
            x="lag",
            y="correlation",
            title=f"Lag Correlation: {data.get_label(x)} vs {data.get_label(y)}",
            color="correlation",
            color_continuous_scale="BrBG",
        )
        fig.update_layout(
            paper_bgcolor="#fffdf8",
            plot_bgcolor="#fffdf8",
            font={"family": "Georgia, serif", "color": "#1d2a33"},
            margin={"l": 40, "r": 20, "t": 70, "b": 40},
        )

        best = find_best_lag(corr_df)
        text = interpret_lag(best, data.get_label(x), data.get_label(y))
        return fig, text
