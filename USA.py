import plotly.express as px
import pandas as pd

data = pd.read_csv('data/2017t.csv')

unique_airports = data[['latitude', 'longitude', 'name']].drop_duplicates()

# Crée un scatter plot avec un point par aéroport
fig = px.scatter_geo(
    unique_airports,
    lat='latitude',
    lon='longitude',
    text='name',
    title='Airports in the United States',
    scope='usa',  # Spécifie la zone géographique aux États-Unis
)

# Personnalise la mise en page de la carte
fig.update_geos(
    showcoastlines=True,
    coastlinecolor="black",
    showland=True,
    landcolor="lightgray",
    showocean=True,
    oceancolor="skyblue",
)

# Montre la figure
fig.show()
