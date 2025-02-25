'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise is a second part for Callback implementation
# But also focused for data load optimization

# However, it's happening somethig weird, there are some errors when generating the json outpul

# Import required libraries

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import json
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# Call stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load data from open source data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Create a list of available countries
country_options = df['country'].unique()

# Create layout for the app
app.layout = html.Div([
    html.H1('Gapminder Data Visualization'),

    dcc.Graph(id='gapminder-graph'),

    'Country',
    dcc.Dropdown(
        id='country-picker',
        options=[{'label': country, 'value': country} for country in country_options],
        value='Colombia'
    ),

    dcc.Store(id='gapminder-figure-store', data={"data": [], "layout": {}}),

    'Indicator',
    dcc.Dropdown(
        id='indicator-picker',
        options=[
            {'label': 'Population', 'value': 'pop'},
            {'label': 'Life Expectancy', 'value': 'lifeExp'},
            {'label': 'GDP per Capita', 'value': 'gdpPercap'}
        ],
        value='pop'
    ),

    'Graph Scale',
    dcc.RadioItems(
        id='scale-picker',
        options=[
            {'label': x, 'value': x} for x in ['linear', 'log']
        ],
        value='linear'
    ),

    #This next section show how the data it's being stored in the store
    html.Hr(),
    html.Details([
        html.Summary('Stored Data'),
        dcc.Markdown(id='stored-data')
    ])
])

# Create callback for the graph
@app.callback(
    Output('gapminder-figure-store', 'data'),
    [Input('indicator-picker', 'value'),
     Input('country-picker', 'value')]
    )

# Function to update the graph
def update_store(indicator, country):
    filtered_df = df[df['country'] == country]
    
    fig = px.scatter(
        filtered_df, x="year", y=indicator,
        title=f"{indicator} in {country}"
    )

    # ✅ Convertir la figura a JSON compatible
    fig_dict = json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))

    return fig_dict


# Client side callback to update the graph
app.clientside_callback(
    '''
    function(figure, scale) {
        if (!figure || typeof figure !== "object" || !figure.data) {
            return { "data": [], "layout": { "yaxis": { "type": scale } } };
        }
        return {
            ...figure,
            layout: { ...figure.layout, yaxis: { type: scale } }
        };
    }
    ''',
    Output("gapminder-graph", "figure"),
    [Input("gapminder-figure-store", "data"),
     Input("scale-picker", "value")]
)


# Callback to update the stored data
@app.callback(
    Output('stored-data', 'children'),
    [Input('gapminder-figure-store', 'data')]
)

# Function to update the stored data
def update_stored_data(data):
    return '```json\n' + json.dumps(data, indent=2) + '\n```'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)