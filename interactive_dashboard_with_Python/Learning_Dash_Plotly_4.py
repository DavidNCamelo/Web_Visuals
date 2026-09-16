"""
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
"""

# This exercise is for Callback implementation
# Callbacks are the connection between components like slicers, buttons, etc. and the output components like graphs, tables, etc.
# There was necessary make changes based on errors and obsolete functions

# Import required libraries
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# Load css stylesheet based on a open source ones
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialize the Dash app
app = dash.Dash("Hello Dash", external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown-test",
            options=[
                # {"label": "Coke", "value": "K0"},
                {"label": "Apple", "value": "AAPL"},
                {"label": "Tesla", "value": "TSLA"},
                {"label": "Nu", "value": "NU"},
                {"label": "S&P Tech", "value": "IUIT.L"},
                {"label": "US Global GO GOLD", "value": "GOAU"},
            ],
            value="AAPL",
        ),
        dcc.Graph(id="graph-test"),
    ],
    style={"width": "500"},
)


# Callback function
@app.callback(Output("graph-test", "figure"), [Input("dropdown-test", "value")])

# Function to update the graph and data import
def update_graph(selected_dropdown_value):
    # (por ejemplo si el usuario borra la selección del dropdown)
    if not selected_dropdown_value:
        return go.Figure()

    stock = yf.download(
        selected_dropdown_value,
        start="2016-01-01",
        auto_adjust=True,
        progress=False,
    )

    # MultiIndex (ticker, campo) incluso pidiendo un solo ticker.
    # Esto aplana las columnas para poder usar stock["Close"] sin errores.
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    if stock.empty:
        return go.Figure()

    fig = go.Figure(data=[go.Scatter(x=stock.index, y=stock["Close"], mode="lines")])
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
