"""Code zur Erstellung der Datenbank läuft circa 50 Minuten. Besser nicht ausführen
(außer es ist sehr viel Zeit da :D). Fertige Database ist bereitgestellt."""

import pandas as pd
import sqlite3
from pandas import DataFrame
import numpy as np


#Erstelle eine leere Datenbank mit folgenden Tabellen
conn = sqlite3.connect('Datenbank.db')
conn.execute("PRAGMA foreign_keys = 1") #Erlaube Foreign Keys
c = conn.cursor()

#Erstelle Tabelle Land
c.execute('''CREATE TABLE IF NOT EXISTS Land
([Land_Name] TEXT PRIMARY KEY)''')

#Erstelle Tabelle Jahr
c.execute('''CREATE TABLE IF NOT EXISTS Jahr
([Jahreszahl] INTEGER PRIMARY KEY)''')

#Erstelle Tabelle hat_Bevölkerung
c.execute('''CREATE TABLE IF NOT EXISTS hat_Bevölkerung
([Name] text,
[Jahre] integer,
[Anzahl] integer,
[Wachstumsfaktor] real,
FOREIGN KEY (Name) REFERENCES Land (Land_Name),
FOREIGN KEY (Jahre) REFERENCES Jahr (Jahreszahl))''')

#Erstelle Tabelle hat_Co2Emissionen
c.execute('''CREATE TABLE IF NOT EXISTS hat_Co2Emissionen
([Name] text,
[Jahre] integer,
[Tonnen] real,
[Co2_pro_Kopf] real,
FOREIGN KEY (Name) REFERENCES Land (Land_Name),
FOREIGN KEY (Jahre) REFERENCES Jahr (Jahreszahl))''')

#Erstelle Tabelle hat_BIP
c.execute('''CREATE TABLE IF NOT EXISTS hat_BIP
([Name] text,
[Jahre] integer,
[BIP] real,
FOREIGN KEY (Name) REFERENCES Land (Land_Name),
FOREIGN KEY (Jahre) REFERENCES Jahr (Jahreszahl))''')

#Erstelle Tabelle hat_Fleischkonsum
c.execute('''CREATE TABLE IF NOT EXISTS hat_Fleischkonsum
([Name] text,
[Jahre] integer,
[Kg_pro_Kopf] real,
FOREIGN KEY (Name) REFERENCES Land (Land_Name),
FOREIGN KEY (Jahre) REFERENCES Jahr (Jahreszahl))''')

#conn.commit()

#Einslesen der CSV Dateien als Dataframes
df_co2 = pd.read_csv('co2_emission.csv')
df_popgrowth = pd.read_csv('population_growth.csv')
df_poptotal = pd.read_csv('population_total.csv')
df_gdp = pd.read_csv('gdp.csv')
df_meat = pd.read_csv('meat-supply-per-person.csv')
df_AlleLaender = pd.read_csv('theworld.csv')

del df_AlleLaender['Code']

#Filtern nach den Jahren 1997-2017
df_co2 = df_co2.loc[df_co2["Year"]>1996]
df_co2 = df_co2.loc[df_co2["Year"]<2018]

#Entfernen der Spalten 1960-1996, 2018-2020, Country Code, Indicator Name, Indicator Code
del df_popgrowth['Indicator Name']
del df_popgrowth['Indicator Code']
del df_popgrowth['Country Code']

for i in range(1960,1997):
    del df_popgrowth[str(i)]

for i in range(2018,2021):
    del df_popgrowth[str(i)]

del df_gdp['Indicator Name']
del df_gdp['Indicator Code']
del df_gdp['Country Code']

for i in range(1960,1997):
    del df_gdp[str(i)]

for i in range(2018,2021):
    del df_gdp[str(i)]

#Filtern nach 1997 bis 2017
df_meat = df_meat.loc[df_meat["Year"]>1996]
df_meat = df_meat.loc[df_meat["Year"]<2018]

#Filtern nach 1997 bis 2017
df_poptotal = df_poptotal.loc[df_poptotal["Year"]>1996]
df_poptotal = df_poptotal.loc[df_poptotal["Year"]<2018]

#Erstelle Dataframe für die Tabelle Land
df_Laender = pd.DataFrame(columns=['Land_Name'])
df_Laender['Land_Name'] = df_AlleLaender['Name']

#Fülle die Tabelle Land in der Datenbank
df_Laender.to_sql('Land', conn, if_exists='append', index = False)

#Erstelle Dataframe für die Tabelle Jahr
df_Jahr = pd.DataFrame(np.array([[1997],[1998],[1999],[2000],[2001],[2002],[2003],[2004],[2005],[2006],[2007],[2008],[2009],[2010],[2011],[2012],[2013],[2014],[2015],[2016],[2017]]),columns=['Jahreszahl'])
df_Jahr.to_sql('Jahr', conn, if_exists='append', index = False)

#Erstelle Dataframe für die Tabelle hat_Bevölkerung
df_hat_Bevölkerung = pd.DataFrame(columns=['Name', 'Jahre', 'Anzahl', 'Wachstumsfaktor'])
df_hat_Bevölkerung['Name'] = df_poptotal['Country Name']
df_hat_Bevölkerung['Jahre'] = df_poptotal['Year']
df_hat_Bevölkerung['Anzahl'] = df_poptotal['Count']

df_hat_Bevölkerung = pd.merge(df_AlleLaender, df_hat_Bevölkerung)

#Erstelle die Tabelle hat_Fleischkonsum
df_hat_Fleischkonsum = pd.DataFrame(columns=['Name','Jahre','Kg_pro_Kopf'])
df_hat_Fleischkonsum['Name'] = df_meat['Entity']
df_hat_Fleischkonsum['Jahre'] = df_meat['Year']
df_hat_Fleischkonsum['Kg_pro_Kopf'] = df_meat['Meat supply per person (kilograms per year)']

df_hat_Fleischkonsum = pd.merge(df_AlleLaender, df_hat_Fleischkonsum)

df_hat_Fleischkonsum.to_sql('hat_Fleischkonsum', conn, if_exists='append', index = False)

#Erstelle die Tabelle hat_Co2Emissionen
df_hat_Co2Emissionen = pd.DataFrame(columns=['Name','Jahre','Tonnen','Co2_pro_Kopf'])
df_hat_Co2Emissionen['Name'] = df_co2['Entity']
df_hat_Co2Emissionen['Jahre'] = df_co2['Year']
df_hat_Co2Emissionen['Tonnen'] = df_co2['Annual CO₂ emissions (tonnes )']

df_hat_Co2Emissionen = pd.merge(df_AlleLaender, df_hat_Co2Emissionen)

for i, j in df_hat_Co2Emissionen.iterrows():
    for k, l in df_hat_Bevölkerung.iterrows():
        if j['Name'] == l['Name'] and j['Jahre'] == l['Jahre']:
            df_hat_Co2Emissionen.at[i, 'Co2_pro_Kopf'] = j['Tonnen'] / l['Anzahl']

df_hat_Co2Emissionen.to_sql('hat_Co2Emissionen', conn, if_exists='append', index = False)

#Fülle die Tabelle hat_Bevölkerung mit den entsprechenden Wachstumsfaktoren (Vllt reicht auch Jahr 1997, dann kann man die anderen Werte auch selber berechnen)
for n in range(1997,2018):
    for i, j in df_hat_Bevölkerung.iterrows():
        for k, l in df_popgrowth.iterrows():
            if j['Name'] == l['Country Name'] and j['Jahre'] == n:
                df_hat_Bevölkerung.at[i, 'Wachstumsfaktor'] = l[str(n)]

df_hat_Bevölkerung.to_sql('hat_Bevölkerung', conn, if_exists='append', index = False)

#Erstelle die Tabelle hat_BIP
df_hat_BIP = pd.DataFrame(columns=['Name','Jahre','BIP'])
df_hat_BIP['Name'] = df_poptotal['Country Name']
df_hat_BIP['Jahre'] = df_poptotal['Year']

df_hat_BIP = pd.merge(df_AlleLaender, df_hat_BIP)

for n in range(1997,2018):
    for i, j in df_hat_BIP.iterrows():
        for k, l in df_gdp.iterrows():
            if j['Name'] == l['Country Name'] and j['Jahre'] == n:
                df_hat_BIP.at[i, 'BIP'] = l[str(n)]

df_hat_BIP.to_sql('hat_BIP', conn, if_exists='append', index = False)
