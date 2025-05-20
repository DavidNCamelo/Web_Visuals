'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# First component of the Dash app Layout

# Importing Libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load css stylesheet based on a open source ones
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create a DataFrame

df = pd.DataFrame({
    "Fruit": ["Apple", "Banana", "Orange", "Apple", "Banana", "Orange"],
    "Amount": [4, 6, 8, 12, 15, 20],
    "City": ["SF", "SF", "SF", "NYC", "MTL", "NYC"]
})

# Create a figure
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Hello Dash"),

    html.Div('''
             Dash: A web application framework for Python.
             Creating Interactive Dashboards based on code, for low coders.
             '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
        )
])

# Run the app
app.run_server(debug=True)