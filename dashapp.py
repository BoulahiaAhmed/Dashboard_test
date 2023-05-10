# Import packages
# DCC stands for Dash Core Components
# plotly.express library to build the interactive graphs

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import psycopg2
import pandas as pd

"""
# Initialize the app (always the same for any Dash app)
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Hello World')
])

# Run the app (always the same for any Dash app)
if __name__ == '__main__':
    app.run_server(debug=True)
"""




"""
# Connecting to PostgreSQL Data
# Establish server connection
con = psycopg2.connect(
database="aact",
user="postgres",
password="21271340",
host="localhost",
port= '5432'
)

# Creating cursor object
cursor_obj = con.cursor()

# SQL Query
"""

sql_query = """SELECT
  s.phase,
  COUNT(*) AS num_trials,
  AVG(s.enrollment) AS avg_enrollment,
  MAX(s.enrollment) AS max_enrollment,
  MIN(s.enrollment) AS min_enrollment,
  COUNT(DISTINCT sp.name) AS num_sponsors
FROM
  studies s
LEFT JOIN
  sponsors sp ON s.nct_id = sp.nct_id
GROUP BY
  s.phase;"""



"""
# executing the query
cursor_obj.execute(sql_query)

# Fetching data
result = cursor_obj.fetchall()

# Creating Pands DF
result_df = pd.DataFrame( result , columns=['phase', 'num_trials', 'avg_enrollment', 'max_enrollment', 'min_enrollment', 'num_sponsor'])

"""

url = 'https://raw.githubusercontent.com/BoulahiaAhmed/Dashboard_test/main/dashboard_data.csv'
result_df = pd.read_csv(url)


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(className='row', children='Number of trials, avg enrollment, max enrollment, min enrollment, and number of sponsors for each trial phase.',
    style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['num_trials', 'avg_enrollment', 'max_enrollment', 'min_enrollment', 'num_sponsor'], 
                       value='num_trials',
                       inline= True,
                       id='controls-and-radio-item')]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=result_df.to_dict('records'), 
                                 page_size=20, 
                                 style_table={'overflowX': 'auto','width':'50%'},
                                 style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': 'yellow',
                                    'fontWeight': 'bold'
                                    },)
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='controls-and-graph', style={'width': '90vh', 'height': '90vh'})
        ])
    ])
])


# Add controls to build the interaction
# The callback function : give the app user more freedom to interact with the app

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(result_df, 
                       x='phase', 
                       y=col_chosen, 
                       #histfunc='avg'
                       )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)











































