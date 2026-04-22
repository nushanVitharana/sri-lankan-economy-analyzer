#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dash import Dash
from dashboard.layouts.main_layout import create_layout
from dashboard.callbacks.timeline_callbacks import register_timeline_callbacks
from dashboard.callbacks.signal_callbacks import register_signal_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = create_layout()

# Register callbacks
register_timeline_callbacks(app)
register_signal_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
