from dash import Input, Output
import plotly.express as px

from dashboard.data_loader import DashboardData


data = DashboardData()


def register_timeline_callbacks(app):
    @app.callback(
        Output("timeline-chart", "figure"),
        Input("timeline-indicator", "value"),
    )
    def update_timeline(indicator):
        df = data.df.ffill()
        label = data.get_label(indicator)
        unit = data.get_unit(indicator)

        fig = px.line(
            df,
            x=df.index,
            y=indicator,
            title=f"{label} Over Time",
            markers=True,
        )
        fig.update_layout(
            paper_bgcolor="#fffdf8",
            plot_bgcolor="#fffdf8",
            font={"family": "Georgia, serif", "color": "#1d2a33"},
            hovermode="x unified",
            margin={"l": 40, "r": 20, "t": 70, "b": 40},
        )
        fig.update_traces(line={"color": "#8b5e34", "width": 3})
        fig.update_yaxes(title=unit or label, gridcolor="#e8e0d3")
        fig.update_xaxes(title="", gridcolor="#f0ebe2")
        return fig
