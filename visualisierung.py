import pandas as pd
import sqlite3
from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

conn = sqlite3.connect('Datenbank.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

app = dash.Dash(__name__)

"""c.execute('''SELECT Name,AVG([Co2_pro_Kopf]) AS [MEAN] FROM hat_Co2Emissionen
GROUP BY Name ORDER BY MEAN DESC LIMIT 20''') #finde Top 10 Länder mit höchsten CO2-Emissionen (bzw. andere Faktoren)
pro Kopf 1997-2017
"""


c.execute('''SELECT * FROM hat_BIP WHERE 
Name = 'United States' OR
Name = 'China' OR
Name = 'Japan' OR
Name = 'Germany' OR
Name = 'United Kingdom' OR
Name = 'France' OR
Name = 'Italy' OR
Name = 'Brazil' OR
Name = 'Canada' OR
Name = "India"''')

df1 = DataFrame(c.fetchall(), columns=['Name','Jahre','BIP'])
print(df1[:5])

c.execute('''SELECT * FROM hat_Fleischkonsum WHERE
Name = 'Hong Kong' OR
Name = 'United States' OR
Name = 'New Zealand' OR
Name = 'Spain' OR
Name = 'French Polynesia' OR
Name = 'Bahamas' OR
Name = 'Bermuda' OR
Name = 'Argentina' OR
Name = 'Macao' OR
Name = "Luxembourg"''')
df2 = DataFrame(c.fetchall(),columns=['Name','Jahre','Fleischkonsum'])
print (df2[:5])

c.execute('''SELECT Name,Jahre,Wachstumsfaktor FROM hat_Bevölkerung WHERE
Name = 'Qatar' OR
Name = 'United Arab Emirates' OR
Name = 'Bahrain' OR
Name = 'Kuwait' OR
Name = 'Equatorial Guinea' OR
Name = 'Niger' OR
http://127.0.0.1:8050/Name = 'Turks and Caicos Islands' OR
Name = 'Liberia' OR
Name = 'South Sudan' OR
Name = "Oman"''')
df3 = DataFrame(c.fetchall(),columns=['Name','Jahre','Wachstumsfaktor'])
print(df3[:5])

c.execute('''SELECT Name,Jahre,Co2_pro_Kopf FROM hat_Co2Emissionen WHERE
Name = 'Qatar' OR
Name = 'Kuwait' OR
Name = 'Trinidad and Tobago' OR
Name = 'Bahrain' OR
Name = 'United Arab Emirates' OR
Name = 'Luxembourg' OR
Name = 'Aruba' OR
Name = 'United States' OR
Name = 'Australia' OR
Name = "Canada"''')
df4 = DataFrame(c.fetchall(),columns=['Name','Jahre','Co2_pro_Kopf'])
print(df4[:5])

#-------------------------------------------------------------------------------
#Layout

app.layout = html.Div([

    html.H1("Fleisch, Bevölkerung & CO2 Verhältnis", style={'text-align':'center'}),

])

fig1 = px.line(df1, x="Jahre",y="BIP",color="Name")
fig1.show()

fig2 = px.line(df2, x="Jahre",y="Fleischkonsum",color="Name")
fig2.show()

fig3 = px.line(df3, x="Jahre",y="Wachstumsfaktor",color="Name")
fig3.show()

fig4 = px.line(df4, x="Jahre",y="Co2_pro_Kopf",color="Name")
fig4.show()

if __name__ == '__main__':
    app.run_server(debug=True)

#conn.close()"""
