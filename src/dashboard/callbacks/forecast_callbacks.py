"""
Forecast Lab callbacks.
"""

from dash import Input, Output, html
import numpy as np
import plotly.graph_objects as go

from ingestion.data_manager import DataManager


data_manager = None


def get_data_manager():
    global data_manager
    if data_manager is None:
        data_manager = DataManager(country="Sri Lanka", start_year=2010, end_year=2025)
    return data_manager


def register_forecast_callbacks(app):
    @app.callback(
        Output("forecast-indicator", "options"),
        Input("forecast-model", "value"),
    )
    def update_indicator_options(_):
        manager = get_data_manager()
        df_data = manager.fetch_all()
        if df_data.empty:
            return []
        numeric = df_data.select_dtypes(include=[np.number])
        return [{"label": col.replace("_", " ").title(), "value": col} for col in numeric.columns[:20]]

    @app.callback(
        Output("forecast-indicator", "value"),
        Input("forecast-indicator", "options"),
    )
    def set_default_indicator(options):
        if options:
            return options[0]["value"]
        return None

    @app.callback(
        Output("forecast-graph", "figure"),
        Output("forecast-summary", "children"),
        Input("forecast-model", "value"),
        Input("forecast-indicator", "value"),
        Input("forecast-steps", "value"),
    )
    def update_forecast(model_type, indicator, steps):
        if not indicator or not model_type:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Select an indicator and model to view forecasts")
            return empty_fig, "Select an indicator and forecasting model."

        manager = get_data_manager()
        df_data = manager.fetch_all()

        if df_data.empty or indicator not in df_data.columns:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Selected data is not available")
            return empty_fig, "Selected indicator data is not available."

        historical = df_data[indicator].dropna()
        if len(historical) < 5:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Insufficient historical data")
            return empty_fig, "Need at least 5 data points for forecasting."

        if model_type == "arima":
            forecast_result = generate_arima_forecast(historical, steps)
        else:
            forecast_result = generate_var_forecast(df_data.select_dtypes(include=[np.number]), indicator, steps)

        if "error" in forecast_result:
            empty_fig = go.Figure()
            empty_fig.update_layout(title=f"Forecast Error: {forecast_result['error']}")
            return empty_fig, forecast_result["error"]

        fig = create_forecast_figure(historical, forecast_result, indicator, model_type)
        summary = create_forecast_summary(forecast_result, indicator, model_type, steps)
        return fig, summary

    @app.callback(
        Output("causality-heatmap", "figure"),
        Input("forecast-indicator", "value"),
    )
    def update_causality_heatmap(_):
        manager = get_data_manager()
        df_data = manager.fetch_all().select_dtypes(include=[np.number]).dropna(axis=1, how="all")
        if df_data.empty or df_data.shape[1] < 2:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Insufficient data for causality analysis")
            return empty_fig

        causality_matrix = get_granger_causality(df_data.iloc[:, :8])
        if causality_matrix is None:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Causality analysis not available")
            return empty_fig

        return create_causality_heatmap(causality_matrix)


def generate_arima_forecast(historical_data, steps):
    try:
        from models.forecasting import ARIMAForecaster

        forecaster = ARIMAForecaster()
        forecast_df = forecaster.fit_predict(historical_data, historical_data.name, steps)
        if forecast_df.empty:
            return {"error": "ARIMA forecasting failed"}

        return {
            "forecast": forecast_df["forecast"].tolist(),
            "lower_ci": forecast_df["lower_ci"].tolist(),
            "upper_ci": forecast_df["upper_ci"].tolist(),
            "dates": forecast_df.index.tolist(),
            "model_info": "ARIMA / SARIMA",
        }
    except Exception as exc:
        return {"error": f"ARIMA forecast failed: {exc}"}


def generate_var_forecast(data_df, target_indicator, steps):
    try:
        from models.forecasting import VARForecaster

        forecaster = VARForecaster()
        forecasts = forecaster.fit_predict(data_df.dropna(), steps)
        if not forecasts or target_indicator not in forecasts:
            return {"error": "VAR forecasting failed"}

        forecast_df = forecasts[target_indicator]
        return {
            "forecast": forecast_df["forecast"].tolist(),
            "lower_ci": forecast_df["lower_ci"].tolist(),
            "upper_ci": forecast_df["upper_ci"].tolist(),
            "dates": forecast_df.index.tolist(),
            "model_info": "VAR",
        }
    except Exception as exc:
        return {"error": f"VAR forecast failed: {exc}"}


def get_granger_causality(data_df):
    try:
        from models.forecasting import GrangerCausalityAnalyzer

        analyzer = GrangerCausalityAnalyzer(maxlag=3)
        return analyzer.analyze(data_df)
    except Exception:
        return None


def create_forecast_figure(historical, forecast_result, indicator, model_type):
    forecast_dates = forecast_result["dates"]
    forecast_values = forecast_result["forecast"]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=historical.index,
                y=historical.values,
                mode="lines+markers",
                name="Historical",
                line=dict(color="#2f4858", width=3),
            ),
            go.Scatter(
                x=forecast_dates,
                y=forecast_values,
                mode="lines+markers",
                name=f"{model_type.upper()} forecast",
                line=dict(color="#bc6c25", width=3, dash="dash"),
            ),
            go.Scatter(
                x=forecast_dates + forecast_dates[::-1],
                y=forecast_result["upper_ci"] + forecast_result["lower_ci"][::-1],
                fill="toself",
                fillcolor="rgba(188, 108, 37, 0.18)",
                line=dict(color="rgba(255,255,255,0)"),
                name="95% confidence band",
            ),
        ]
    )

    fig.update_layout(
        title=f"{indicator.replace('_', ' ').title()} Forecast",
        xaxis_title="Year",
        yaxis_title="Value",
        hovermode="x unified",
        paper_bgcolor="#fffdf8",
        plot_bgcolor="#fffdf8",
        font={"family": "Georgia, serif", "color": "#1d2a33"},
        margin={"l": 40, "r": 20, "t": 70, "b": 40},
    )
    fig.update_yaxes(gridcolor="#e8e0d3")
    fig.update_xaxes(gridcolor="#f0ebe2")
    return fig


def create_forecast_summary(forecast_result, indicator, model_type, steps):
    forecast_values = forecast_result["forecast"]
    avg_forecast = np.mean(forecast_values)
    min_forecast = min(forecast_values)
    max_forecast = max(forecast_values)
    trend = "rising" if forecast_values[-1] > forecast_values[0] else "softening"

    return html.Div(
        [
            html.P(f"{indicator.replace('_', ' ').title()} shows a {trend} path over the next {steps} years."),
            html.Ul(
                [
                    html.Li(f"Average forecast: {avg_forecast:.2f}"),
                    html.Li(f"Range: {min_forecast:.2f} to {max_forecast:.2f}"),
                    html.Li(f"Model: {forecast_result.get('model_info', model_type.upper())}"),
                    html.Li("Confidence interval: 95 percent band shown in the chart"),
                ]
            ),
        ]
    )


def create_causality_heatmap(causality_matrix):
    variables = causality_matrix.index.tolist()
    p_values = np.full((len(variables), len(variables)), np.nan)

    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            cell = causality_matrix.loc[var1, var2]
            if isinstance(cell, dict) and "p_value" in cell:
                p_values[i, j] = cell["p_value"]

    fig = go.Figure(
        data=go.Heatmap(
            z=p_values,
            x=variables,
            y=variables,
            colorscale="YlOrRd_r",
            zmin=0,
            zmax=0.1,
            colorbar=dict(title="p-value"),
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title="Granger Causality Matrix",
        xaxis_title="Effect (Y)",
        yaxis_title="Cause (X)",
        paper_bgcolor="#fffdf8",
        plot_bgcolor="#fffdf8",
        font={"family": "Georgia, serif", "color": "#1d2a33"},
        margin={"l": 40, "r": 20, "t": 70, "b": 40},
    )
    return fig
