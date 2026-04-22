from dash import dcc

def indicator_dropdown(id, options, value=None):
    return dcc.Dropdown(
        id=id,
        options=[{"label": o, "value": o} for o in options],
        value=value
    )