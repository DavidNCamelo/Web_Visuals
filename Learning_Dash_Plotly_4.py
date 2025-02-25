'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise is for Callback implementation
# Callbacks are the connection between components like slicers, buttons, etc. and the output components like graphs, tables, etc.
# There was necessary make changes based on errors and obsolete functions

# Import required libraries
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime as dt

# Load css stylesheet based on a open source ones
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the Dash app
app = dash.Dash('Hello Dash', external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown-test",
        options=[
            #{"label": "Coke", "value": "K0"},
            {"label": "Apple", "value": "AAPL"},
            {"label": "Tesla", "value": "TSLA"}
        ],
        value="APPL"   # Default value 
    ),
    dcc.Graph(id="graph-test")
], style={"width": "500"})

# Callback function
@app.callback(
    Output("graph-test", "figure"),
    [Input("dropdown-test", "value")]
)

# Function to update the graph and data import
def update_graph(selected_dropdown_value):
    stock = stock = yf.download(selected_dropdown_value, start="2016-01-01")
    fig = go.Figure(data=[go.Scatter(x=stock.index, y=stock['Close'], mode='lines')])
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
