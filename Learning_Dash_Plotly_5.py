'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise is a second part for Callback implementation

# Import required libraries

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Read the data
df = pd.read_csv('master.csv')

# Generate unique values fot the year slicer
mark_values = {str(year): str(year) for year in df['year'].unique()}
mark_values['All'] = 'All'

# Create the app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    html.Div([
        html.Pre(children='Suicide Rates 1985-2016',
        style={"text-align": "center",
               "font-size": "16",
               "color":"black"
            })
    ]),

    html.Div([
        dcc.Graph(id="the-graph")
    ]),

    html.Div([
        dcc.RangeSlider(id='year',
                        min=1985,
                        max=2016,
                        value= [1985,1988],
                        marks= mark_values,
                        step=None)
        ], style={
            "width":"70%",
            "position":"absolute",
            "left":"5%"
        }),
])

# Callback
@app.callback(
    Output("the-graph", "figure"),
    [Input("year", "value")]
)

# Callback iplementation through updates
def update_graph(years_chosen):
    #test years chosedn
    print(years_chosen)

    dff = df[(df["year"]>=years_chosen[0])&(df["year"]<=years_chosen[1])]

    dff = dff.groupby(["country-year"], as_index=False)[["suicides/100k pop", "gdp_per_capita ($)"]].mean()

    # Test dff
    #print(dff[:3])

    #Genrate the graph with express
    scatterplot = px.scatter(
        data_frame=dff,
        x="suicides/100k pop",
        y="gdp_per_capita ($)",
        #hover_data=["country"],
        text="country-year",
        height=550
    )

    scatterplot.update_traces(textposition="top center")

    return(scatterplot)

if __name__ == "__main__":
    app.run_server(debug=True)

    

