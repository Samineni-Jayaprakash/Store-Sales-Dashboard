import dash
from dash import html
import os

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div("Hello from Render! Your Dash app is live.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)
