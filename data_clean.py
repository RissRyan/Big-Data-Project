# Import libraries
import pandas as pd
from datetime import datetime

# Import the datasets
df_weather_brut = pd.read_csv("datasets/historical_weather_2016.csv", sep=",")

# Change features' names
new_columns_weather = ["station_id","airport_name","latitude","longitude","elevation","date","source","report_type","airport_code","quality_control","liquid_precipitation_hourly","snow_depth","snow_accumulation","sky_condition_observation","average_air_temperature","atmospheric_pressure_observation","atmospheric_pressure_change","visibility_observation","wind_observation"]
df_weather_brut.columns = new_columns_weather

# Drop useless columns
df_weather_brut = df_weather_brut.drop(columns=["station_id","airport_name","elevation","source","report_type","quality_control","snow_depth","snow_accumulation","average_air_temperature","atmospheric_pressure_change"])

# Change useful columns' order
new_columns_weather_order = ["airport_code","date","latitude","longitude","liquid_precipitation_hourly","sky_condition_observation","atmospheric_pressure_observation","visibility_observation","wind_observation"]
df_weather_brut = df_weather_brut.reindex(columns=new_columns_weather_order)

# Export dataframe to csv
new_dataset_weather = "datasets/north_america_historical_weather_2016.csv"
df_weather_brut.to_csv(new_dataset_weather, sep=',', index=False)

# Import dataframes from datasets
df_weather = pd.read_csv("datasets/north_america_historical_weather_2016.csv", sep=",")
df_weather = df_weather[df_weather['airport_code'] != "99999"]

# Clean Data for a better treatment
def convert_precipitation(value):
    if isinstance(value, str):
        return float(value[3:5] + "." + value[5:7])
    else:
        return None  # Default value if invalid format
    
def convert_atmospheric_pressure(value):
    if isinstance(value, str):
        return value[0:5] + " " + value[8:-2]
    else:
        return None  # Default value if invalid format
    
def convert_visibility(value):
    if isinstance(value, str):
        return float(value[0:6])/3.281
    else:
        return None  # Default value if invalid format
    
def convert_wind(value):
    if isinstance(value, str):
        return value[0:3] + " " + value[8:11] + "." + value[11:12]
    else:
        return None  # Default value if invalid format

def convert_sky_condition(value):
    if isinstance(value, str):
        return value[1:3] + " " + value[3:5]
    else:
        return None  # Default value if invalid format

# Applicate of functions to the columns
df_weather['liquid_precipitation_hourly'] = df_weather['liquid_precipitation_hourly'].apply(lambda x: convert_precipitation(x))

df_weather['atmospheric_pressure_observation'] = df_weather['atmospheric_pressure_observation'].apply(lambda x: convert_atmospheric_pressure(x))
df_weather[['atmospheric_pressure_1', 'atmospheric_pressure_2']] = df_weather['atmospheric_pressure_observation'].str.split(' ', expand=True)
df_weather = df_weather.drop(columns=['atmospheric_pressure_observation'])
df_weather['atmospheric_pressure_1'] = df_weather['atmospheric_pressure_1'].astype(float)
df_weather['atmospheric_pressure_2'] = df_weather['atmospheric_pressure_2'].astype(float)
df_weather = df_weather[df_weather['atmospheric_pressure_1'] != 99999]
df_weather = df_weather[df_weather['atmospheric_pressure_2'] != 99999]

df_weather['visibility_observation'] = df_weather['visibility_observation'].apply(lambda x: convert_visibility(x))
df_weather = df_weather[df_weather['visibility_observation'] != 304784.82170070097]

df_weather['wind_observation'] = df_weather['wind_observation'].apply(lambda x: convert_wind(x))
df_weather[['wind_direction', 'wind_speed']] = df_weather['wind_observation'].str.split(' ', expand=True)
df_weather = df_weather.drop(columns=['wind_observation'])
df_weather['wind_direction'] = df_weather['wind_direction'].astype(float)
df_weather['wind_speed'] = df_weather['wind_speed'].astype(float)
df_weather = df_weather[df_weather['wind_speed'] != 999.9]
df_weather = df_weather[df_weather['wind_direction'] != 999]

df_weather['date'] = df_weather['date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S"))

df_weather['airport_code'] = df_weather['airport_code'].str.strip()

df_weather['sky_condition_observation'] = df_weather['sky_condition_observation'].apply(lambda x: convert_sky_condition(x))
df_weather = df_weather[df_weather['sky_condition_observation'] != '20 00']
df_weather[['sky_condition_1', 'sky_condition_2']] = df_weather['sky_condition_observation'].str.split(' ', expand=True)
df_weather = df_weather.drop(columns=['sky_condition_observation'])

# Save dataframe
new_dataset_weather = "datasets/north_america_weather_2016_final.csv"
df_weather.to_csv(new_dataset_weather, sep=',', index=False)