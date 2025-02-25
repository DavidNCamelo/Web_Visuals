'''
Learning Plotly and Dash for interactive data visualization based in code

Learning from Udemy Course https://www.udemy.com/course/visualizacion-interactiva-con-python
'''
# This exercise y focused on styling the Dash app with a new background color

# Importing Libraries
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Create Dash app
app = dash.Dash(__name__)

# Load data from open source
df = pd.read_excel("https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx")

# Review DataFrame
print(df.head())

# Create filtered DataFrame
dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths', 'cases']].sum()

# Review filtered DataFrame
print(dff.head())

# Create Layout
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable-id',
            data=dff.to_dict('records'),
            columns=[
                {'name': i, 'id': i, 'deletable': False, 'selectable': False} for i in dff.columns
            ],
            editable=False,
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            row_selectable='multi',
            row_deletable=False,
            selected_rows=[],
            page_action='native',
            #page_current=0,
            #page_size=6,
            style_cell={'whiteSpace': 'normal'},
            fixed_rows={'headers': True, 'data': 0},
            virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'countriesAndTerritories'},
                'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'deaths'},
                'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'},
                'width': '40%', 'textAlign': 'left'}
            ],
    )],
    className='row'
    ),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='filter_dropdown',
                options=[
                    {'label': 'Deaths', 'value': 'deaths'},
                    {'label': 'Cases', 'value': 'cases'}
                ],
                value='deaths',
                multi=False,
                clearable=False
            ),
        ],
        className='six columns'
        ),

    html.Div([
        dcc.Dropdown(
            id='piedropdown',
            options=[
                {'label': 'Deaths', 'value': 'deaths'},
                {'label': 'Cases', 'value': 'cases'}
            ],
            value='deaths',
            multi=False,
            clearable=False
        ),
    ],
    className='row'
    ),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart')
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart')
        ],className='six columns'),
    ],
    className='row'
    )
    ])
])

# Create Callback
@app.callback(
    [Output('linechart', 'figure'),
     Output('piechart', 'figure')],
     [Input('datatable-id', 'selected_rows'),
      Input('piedropdown', 'value'),
      Input('filter_dropdown', 'value')]
)

# Create function to update charts
def update_data(chosen_rows, piedropval, filter_dropdown):
    if len(chosen_rows) == 0:
        df_filter = dff
    else:
        df_filter = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filter,
        names='countriesAndTerritories',
        values=piedropval,
        hole=.3,
        labels={'countriesAndTerritories': 'Countries'}
    )

    # Extract list of chosen countries
    list_chosen_countries = df_filter['countriesAndTerritories'].tolist()

    # Filter original DataFrame with chosen countries
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    # Create line chart
    line_chart = px.line(
        data_frame=df_line,
        x='dateRep',
        y=filter_dropdown,
        color='countriesAndTerritories',
        labels={'countriesAndTerritories': 'Countries', 'dateRep': 'Date'},
        title='Cases and Deaths'
    )

    line_chart.update_layout(uirevision='foo')

    return (line_chart, pie_chart)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
