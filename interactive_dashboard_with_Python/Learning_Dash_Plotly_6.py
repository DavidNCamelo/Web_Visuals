"""
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
"""

# Versión 100% Python: sin clientside_callback, sin JavaScript, sin dcc.Store.
# Un solo callback del lado del servidor arma la figura completa,
# incluyendo la escala (linear/log).

import dash
import plotly.express as px
from dash import Input, Output, dcc, html
import pandas as pd

# Call stylesheets
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load data from open source data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

# Create a list of available countries
country_options = df["country"].unique()

# Create layout for the app
app.layout = html.Div(
    [
        html.H1("Gapminder Data Visualization"),
        dcc.Graph(id="gapminder-graph"),
        "Country",
        dcc.Dropdown(
            id="country-picker",
            options=[
                {"label": country, "value": country} for country in country_options
            ],
            value="Colombia",
        ),
        "Indicator",
        dcc.Dropdown(
            id="indicator-picker",
            options=[
                {"label": "Population", "value": "pop"},
                {"label": "Life Expectancy", "value": "lifeExp"},
                {"label": "GDP per Capita", "value": "gdpPercap"},
            ],
            value="pop",
        ),
        "Graph Scale",
        dcc.RadioItems(
            id="scale-picker",
            options=[{"label": x, "value": x} for x in ["linear", "log"]],
            value="linear",
        ),
    ]
)


# Un único callback: recibe indicador, país y escala, y devuelve la figura lista
@app.callback(
    Output("gapminder-graph", "figure"),
    [
        Input("indicator-picker", "value"),
        Input("country-picker", "value"),
        Input("scale-picker", "value"),
    ],
)
def update_graph(indicator, country, scale):
    filtered_df = df[df["country"] == country]

    fig = px.scatter(
        filtered_df, x="year", y=indicator, title=f"{indicator} in {country}"
    )

    # Escala aplicada directamente en Python, sin JS
    fig.update_yaxes(type=scale)

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
