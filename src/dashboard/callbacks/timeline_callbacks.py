from dash import Input, Output
import plotly.express as px
from dashboard.data_loader import DashboardData

data = DashboardData()

def register_timeline_callbacks(app):

    @app.callback(
        Output("timeline-chart", "figure"),
        Input("timeline-indicator", "value")
    )
    def update_timeline(indicator):

        df = data.df

        fig = px.line(
            df,
            x=df.index,
            y=indicator,
            title=f"{indicator} over time"
        )

        return fig