'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise is a fourth part for Callback implementation
# Case of multiple Inputs
# This code also required changes because the original code was not working, punctually on update_graph function
# The original code was not working because was receiving lists with different lengths, so the merge was not possible

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

# Load data from open source
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv').dropna()

# List elements for dropdown
indicators = df["Indicator Name"].unique()

# Create Layout
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id="xaxis-column",
                options=[{'label': i, 'value': i} for i in indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id="xaxis-type",
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}
        ),

        html.Div([
            dcc.Dropdown(
                id="yaxis-column",
                options=[{'label': i, 'value': i} for i in indicators],
                value='Life expentancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id="yaxis-type",
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'float':'right', 'display': 'inline-block'}
        )
    ]),

    dcc.Graph(id="indicator-graphic"),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
])

# Create callback
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-column', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')]
)

# Update Function Definition
def upgrade_graph(xaxis_column_name, xaxis_type, yaxis_column_name, yaxis_type, year_value):
    dff = df[df['Year'] == year_value]  # Filtrar por año
    
    # Separar en dos DataFrames según el indicador seleccionado
    x_data = dff[dff['Indicator Name'] == xaxis_column_name][['Country Name', 'Value']]
    y_data = dff[dff['Indicator Name'] == yaxis_column_name][['Country Name', 'Value']]
    
    # Renombrar las columnas de "Value" para diferenciarlas antes de hacer el merge
    x_data = x_data.rename(columns={'Value': 'x_value'})
    y_data = y_data.rename(columns={'Value': 'y_value'})

    # Hacer merge para que coincidan en 'Country Name' (clave común)
    merged_df = pd.merge(x_data, y_data, on="Country Name")

    # Si el DataFrame está vacío, devolver un gráfico vacío
    if merged_df.empty:
        return px.scatter(title="No data available for selected indicators")

    # Generar la figura con los datos fusionados
    fig = px.scatter(
        x=merged_df['x_value'],
        y=merged_df['y_value'],
        hover_name=merged_df['Country Name']
    )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)