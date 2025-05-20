'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise y focused on styling the Dash app with a new background color

# Importing Libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load css stylesheet based on a open source ones
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Adding a new extra style
colors = {
    'background': '#7a818b',
    'text': '#4ce1ee'
}

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

# Apply styles to the figure
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Define the layout of the app and now with the style
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children="Hello Dash",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),


        html.Div(children='''
                Dash: A web application framework for Python.
                Creating Interactive Dashboards based on code, for low coders.
                Now styled with a new background color.
                ''',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
                ),

        dcc.Graph(
            id='example-graph-2',
            figure=fig
            )
    ]
)

# Run the app
app.run_server(debug=True)