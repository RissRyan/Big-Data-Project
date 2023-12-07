import pandas as pd

# Read the CSV file into a pandas DataFrame
df_airport = pd.read_csv('data/airports_w_headers.csv')

df_airport.columns = df_airport.columns.str.strip(' "')

df_airport.drop('airport_id', axis=1, inplace=True)
df_airport.drop('icao', axis=1, inplace=True)
df_airport.drop('city', axis=1, inplace=True)
df_airport.drop('country', axis=1, inplace=True)
df_airport.drop('altitude', axis=1, inplace=True)
df_airport.drop('timezone', axis=1, inplace=True)
df_airport.drop('dst', axis=1, inplace=True)
df_airport.drop('timezone_name', axis=1, inplace=True)
df_airport.drop('type', axis=1, inplace=True)
df_airport.drop('source', axis=1, inplace=True)

data = pd.read_csv('data/2017.csv')

data.drop('Unnamed: 27', axis=1, inplace=True)
data.drop('OP_CARRIER_FL_NUM', axis=1, inplace=True)
data.drop('TAXI_OUT', axis=1, inplace=True)
data.drop('WHEELS_OFF', axis=1, inplace=True)
data.drop('WHEELS_ON', axis=1, inplace=True)
data.drop('TAXI_IN', axis=1, inplace=True)
data.drop('DEST', axis=1, inplace=True)
data.drop('CRS_DEP_TIME', axis=1, inplace=True)
data.drop('DEP_TIME', axis=1, inplace=True)
data.drop('DEP_DELAY', axis=1, inplace=True)
data.drop('CRS_ARR_TIME', axis=1, inplace=True)
data.drop('ARR_TIME', axis=1, inplace=True)
data.drop('CRS_ELAPSED_TIME', axis=1, inplace=True)
data.drop('ACTUAL_ELAPSED_TIME', axis=1, inplace=True)
data.drop('AIR_TIME', axis=1, inplace=True)
data.drop('DISTANCE', axis=1, inplace=True)

# Remplacement des valeurs nulles par 0 dans les colonnes spécifiées
columns_to_fill = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
data[columns_to_fill] = data[columns_to_fill].fillna(0)

# Merge the two DataFrames on the common column "iata"
merged_df = pd.merge(data, df_airport, how='inner', left_on='ORIGIN', right_on='iata')

merged_df.drop('ORIGIN', axis=1, inplace=True)
merged_df.drop('iata', axis=1, inplace=True)

print(merged_df.columns)

merged_df.to_csv('data/2017t.csv', index=False)