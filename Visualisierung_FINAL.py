"""FINALER CODE ZUR VISUALISIERUNG (1. Version war bloß eine "Notlösung")
Dieser Code ist inspiriert von Code von: https://dash.plotly.com/basic-callbacks."""

import pandas as pd
import sqlite3
from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

conn =sqlite3.connect('Datenbank.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

c.execute('''SELECT hat_Co2Emissionen.Name,hat_Co2Emissionen.Jahre,
hat_Co2Emissionen.Co2_pro_Kopf, hat_Fleischkonsum.Kg_pro_Kopf,
hat_Bevölkerung.Wachstumsfaktor
FROM hat_Co2Emissionen
INNER JOIN hat_Fleischkonsum ON hat_Co2Emissionen.Name = hat_Fleischkonsum.Name
AND hat_Co2Emissionen.Jahre = hat_Fleischkonsum.Jahre
INNER JOIN hat_Bevölkerung ON hat_Co2Emissionen.Name = hat_Bevölkerung.Name
AND hat_Co2Emissionen.Jahre = hat_Bevölkerung.Jahre''')
df = DataFrame(c.fetchall(), columns = ['Name','Jahre','CO2 pro Kopf','Fl.konsum in kg','Wachstumsfaktor'])
print (df)

app = dash.Dash(__name__)

#-------------------------------------------------------------------------------
#Layout

app.layout = html.Div([

    html.H3("Zusammenhang Fleischkonsum, Wachstumsfaktor & CO2-Emissionen", style={'text-align':'center'}),

    html.Div(id='output_container',style={'text-align':'center'}),
    
    dcc.Graph(id='zsmhg_graph'),
    
    dcc.Slider(
        id='jahr_slider',
        min=df['Jahre'].min(),
        max=df['Jahre'].max(),
        value=df['Jahre'].max(),
        marks={str(Jahre):str(Jahre) for Jahre in df['Jahre'].unique()},
        step = None 
    )
])

# ------------------------------------------------------------------------------
# Verbindung Graph und Dash Komponenten
@app.callback(
    Output('output_container', 'children'),
    Output('zsmhg_graph', 'figure'),
    Input('jahr_slider', 'value'))
def update_graph(gewähltes_jahr):

    container = "Im Jahr: {}".format(gewähltes_jahr)
    
    dff = df[df.Jahre == gewähltes_jahr]

    fig = px.scatter(dff, x="Fl.konsum in kg", y="Wachstumsfaktor", 
                     size="CO2 pro Kopf",hover_name="Name",color="Name")

    return container, fig



if __name__ == '__main__':
    app.run_server(debug=True)
