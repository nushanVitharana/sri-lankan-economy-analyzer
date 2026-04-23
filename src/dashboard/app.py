#!/usr/bin/env python3
import os
import sys

from dash import Dash

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.callbacks.forecast_callbacks import register_forecast_callbacks
from dashboard.callbacks.signal_callbacks import register_signal_callbacks
from dashboard.callbacks.timeline_callbacks import register_timeline_callbacks
from dashboard.layouts.main_layout import create_layout


app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Sri Lanka Crisis Dashboard"
app.layout = create_layout()

register_timeline_callbacks(app)
register_signal_callbacks(app)
register_forecast_callbacks(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
