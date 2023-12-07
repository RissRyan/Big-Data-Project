# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import folium
from io import BytesIO
import base64

# Import new dataset for analysis
data = pd.read_csv("datasets/north_america_weather_2016_final.csv", sep=",")

# ===========================
#     Graph for Dashboard
# ===========================

# Barchart on the year for a *feature and an *airport
def generate_bar_chart(airport_code, feature):
    data_filtered = data[(data['airport_code'] == airport_code) & (data[feature].notnull())]
    data_filtered['date'] = pd.to_datetime(data_filtered['date'])
    data_filtered = data_filtered.set_index('date').sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(data_filtered.index, data_filtered[feature], color='skyblue')
    plt.title(f'{feature.capitalize()} for {airport_code}')
    plt.xlabel('Date')
    plt.ylabel(feature.capitalize())
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

generate_bar_chart('KDWH', 'wind_direction')

# ---------------------------------------------------------------------------
# Top X of *feature for *airport
def plotTopX(feature, x=5, ascending=False):
    # Group by 'airport_code' et select X top value higher or lower
    # in function of the 'feature'
    grouped_data = data.groupby('airport_code').agg({feature: 'max'}).reset_index()
    sorted_data = grouped_data.sort_values(by=feature, ascending=ascending).head(x)
    
    # Recovery data for the airports
    top_x = data[data['airport_code'].isin(sorted_data['airport_code'])]

    # Creation of bar graph
    plt.figure(figsize=(10, 6))
    
    # Sort values
    top_x = top_x.sort_values(by=feature, ascending=ascending)
    
    plt.bar(top_x['airport_code'], top_x[feature])
    plt.xlabel('Airport Code')
    plt.ylabel(feature)
    plt.title(f'Top {x} airports with {"lowest" if ascending else "highest"} {feature}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plotTopX('wind_speed', x=5)

# ---------------------------------------------------------------------------
# Pie Chart for Precipitation
def generate_pie_chart_precipitation(airport_code):
    data_filtered = data[(data['airport_code'] == airport_code) & (data['liquid_precipitation_hourly'].notnull())]
    
    # Exclude NaN columns of 'liquid_precipitation_hourly'
    data_filtered = data_filtered.dropna(subset=['liquid_precipitation_hourly'])
    
    if data_filtered.empty:
        print(f"No data available for {airport_code} or there are no valid values in 'liquid_precipitation_hourly'.")
        return
    
    labels = ['No Precipitation', 'Light', 'Moderate', 'Heavy']
    bins = [0, 0.1, 2.5, 7.6, np.inf]
    
    # Categorizing precipitation data
    data_filtered['precipitation_category'] = pd.cut(data_filtered['liquid_precipitation_hourly'], bins=bins, labels=labels)
    grouped_data = data_filtered['precipitation_category'].value_counts()
    
    # Creation of Pie Chart
    plt.figure(figsize=(8, 6))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'Hourly Precipitation Rates for {airport_code}')
    plt.axis('equal')  # For perfect circle aspect
    plt.tight_layout()
    plt.show()

generate_pie_chart_precipitation('KDWH')

# ---------------------------------------------------------------------------
# Pressure on time plot for an *airport
def plot_pressure_time(airport_code):
    data_filtered = data[data['airport_code'] == airport_code]
    data_filtered['date'] = pd.to_datetime(data_filtered['date'])

    plt.figure(figsize=(10, 6))
    plt.scatter(data_filtered['date'], data_filtered['atmospheric_pressure_1'], alpha=0.5)
    plt.title(f'Atmospheric Pressure (scatter plot) over Time for {airport_code}')
    plt.xlabel('Date')
    plt.ylabel('Atmospheric Pressure (1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_pressure_time('KDWH')

# ---------------------------------------------------------------------------
# Visibility over the time for an *airport
def plot_visibility_over_time(airport_code):
    data_filtered = data[(data['airport_code'] == airport_code) & (data['visibility_observation'].notnull())]
    
    if data_filtered.empty:
        print(f"No data available for {airport_code} or there are no valid values for 'visibility_observation'.")
        return
    
    data_filtered['date'] = pd.to_datetime(data_filtered['date'])
    data_filtered = data_filtered.sort_values('date')
    
    plt.figure(figsize=(10, 6))
    plt.plot(data_filtered['date'], data_filtered['visibility_observation'], marker='o', linestyle='-')
    plt.title(f'Visibility Over Time for {airport_code}')
    plt.xlabel('Date')
    plt.ylabel('Visibility')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_visibility_over_time('KDWH')

# ---------------------------------------------------------------------------
# Precipitation distribution per mounth
def precipitation_distribution_by_month(airport_code):
    # Sort data for specified airport
    data_filtered = data[data['airport_code'] == airport_code]
    
    if data_filtered.empty:
        print(f"No data available for {airport_code}.")
        return
    
    # Ensure that date data is in datetime format
    data_filtered['date'] = pd.to_datetime(data_filtered['date'])
    
    # Extract mounth
    data_filtered['month'] = data_filtered['date'].dt.month_name()
    
    # Group by month and categorize precipitation (rain, snow, etc.).
    categories = ['No Precipitation', 'Light', 'Moderate', 'Heavy']
    bins = [0, 0.1, 2.5, 7.6, data_filtered['liquid_precipitation_hourly'].max()]
    data_filtered['precipitation_category'] = pd.cut(data_filtered['liquid_precipitation_hourly'], bins=bins, labels=categories)
    
    # Group by month and precipitation category and count occurrences
    grouped_data = data_filtered.groupby(['month', 'precipitation_category']).size().unstack().fillna(0)
    
    # Creating stacked bar charts
    plt.figure(figsize=(12, 8))
    grouped_data.plot(kind='bar', stacked=True)
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title(f'Precipitation Distribution by Month for {airport_code}')
    plt.legend(title='Precipitation Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

precipitation_distribution_by_month('KJFK')

# ---------------------------------------------------------------------------

# It is possible to found detail of sky codes here :
# https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM

# Double Distribution of Sky Condition for a specific airport
def sky_condition_distribution_by_month(airport_code):
    # Filter data for specified airport
    data_filtered = data[data['airport_code'] == airport_code]
    
    if data_filtered.empty:
        print(f"No data available for {airport_code}.")
        return
    
    # Ensure that date data is in datetime format
    data_filtered['date'] = pd.to_datetime(data_filtered['date'])
    
    # Extract month
    data_filtered['month'] = data_filtered['date'].dt.month_name()
    
    # Group by month
    grouped_data_1 = data_filtered.groupby(['month', 'sky_condition_1']).size().unstack().fillna(0)
    grouped_data_2 = data_filtered.groupby(['month', 'sky_condition_2']).size().unstack().fillna(0)
    
    # Creation of a side-by-side bar graph for each sky condition
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    
    grouped_data_1.plot(kind='bar', stacked=True, ax=axes[0])
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Count')
    axes[0].set_title(f'Sky Condition 1 Distribution by Month for {airport_code}')
    axes[0].legend(title='Sky Condition 1')
    axes[0].tick_params(axis='x', rotation=45)
    
    grouped_data_2.plot(kind='bar', stacked=True, ax=axes[1])
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Count')
    axes[1].set_title(f'Sky Condition 2 Distribution by Month for {airport_code}')
    axes[1].legend(title='Sky Condition 2')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

sky_condition_distribution_by_month('KJFK')

# Double Distribution of Sky Condition for a specific airport for specific month
def sky_condition_distribution_for_month(airport_code, month):
    # Date must be in the format ""
    
    # Filter data for specified airport
    data_filtered = data[(data['airport_code'] == airport_code) & (pd.to_datetime(data['date']).dt.month == pd.to_datetime(month).month)]
    
    if data_filtered.empty:
        print(f"No data available for {airport_code} in {month}.")
        return
    
    # Group by month
    grouped_data_1 = data_filtered.groupby('sky_condition_1').size().fillna(0)
    grouped_data_2 = data_filtered.groupby('sky_condition_2').size().fillna(0)
    
    # Creation of a side-by-side bar graph for each sky condition
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    
    grouped_data_1.plot(kind='bar', ax=axes[0])
    axes[0].set_xlabel('Sky Condition 1')
    axes[0].set_ylabel('Count')
    axes[0].set_title(f'Sky Condition 1 Distribution for {airport_code} in {month}')
    axes[0].tick_params(axis='x', rotation=45)
    
    grouped_data_2.plot(kind='bar', ax=axes[1])
    axes[1].set_xlabel('Sky Condition 2')
    axes[1].set_ylabel('Count')
    axes[1].set_title(f'Sky Condition 2 Distribution for {airport_code} in {month}')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

sky_condition_distribution_for_month('KJFK', '2016-05-01')