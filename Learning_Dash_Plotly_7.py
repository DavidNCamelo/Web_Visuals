'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise is a third part for Callback implementation

# Import required libraries

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import json
import plotly.express as px

# Call stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load data from open source data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Create app layout
app.layout = html.Div([
    dcc.Graph(id="graph-with-slider"),

    dcc.Slider(
        id="year-slider",
        min=df["year"].min(),
        max=df["year"].max(),
        value=df["year"].min(),
        marks={str(year): str(year) for year in df["year"].unique()},
        step=None
    )
])

# Create callback
@app.callback(
    Output("graph-with-slider", "figure"),
    [Input("year-slider", "value")]
)

# Update function
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)
    
    fig.update_layout(transition_duration=500)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)