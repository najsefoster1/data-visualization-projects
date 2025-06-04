#Najse Foster
#Professor Jasur Rhakimov
#CIS609 -
#Unit 6: Assignment
#Bike Share Efficiency Project: Data Preparation and Initial Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

#Step 1: Load and Merge All 7 Datasets
csv_files = [
    '202501-citibike-tripdata_1.csv',
    '202501-citibike-tripdata_2.csv',
    '202501-citibike-tripdata_3.csv',
    '202502-citibike-tripdata_1.csv',
    '202502-citibike-tripdata_2.csv',
    '202502-citibike-tripdata_3.csv',
    '202503-citibike-tripdata.csv'
]

dataframes = [pd.read_csv(file) for file in csv_files]
df_bike = pd.concat(dataframes, ignore_index=True)

#Step 2: Data Cleaning
if 'started_at' in df_bike.columns:
    df_bike.rename(columns={'started_at': 'starttime', 'ended_at': 'stoptime',
                            'start_station_id': 'start station id', 'end_station_id': 'end station id'}, inplace=True)

df_bike.dropna(subset=['starttime', 'stoptime', 'start station id', 'end station id'], inplace=True)

df_bike['starttime'] = pd.to_datetime(df_bike['starttime'])
df_bike['stoptime'] = pd.to_datetime(df_bike['stoptime'])

df_bike['tripduration'] = (df_bike['stoptime'] - df_bike['starttime']).dt.total_seconds() / 60
df_bike = df_bike[df_bike['tripduration'] > 0]

#Feature Engineering
df_bike['day_of_week'] = df_bike['starttime'].dt.day_name()
df_bike['hour_of_day'] = df_bike['starttime'].dt.hour
df_bike['date'] = df_bike['starttime'].dt.date

#Visualizations

#Type 1: Analyze First, Visualize Later - Trips per Day
trips_per_day = df_bike.groupby('date').size()

plt.figure(figsize=(14,6))
trips_per_day.plot()
plt.title('Daily Bike Trips (Jan–Mar 2025)')
plt.xlabel('Date')
plt.ylabel('Number of Trips')
plt.grid(True)
plt.tight_layout()
plt.show()

#Type 2: Visualize First, Analyze Later - Hourly Usage
plt.figure(figsize=(12,6))
sns.countplot(data=df_bike, x='hour_of_day', hue='day_of_week', palette='Set2')
plt.title('Hourly Bike Usage by Day of the Week (Jan–Mar 2025)')
plt.xlabel('Hour of Day')
plt.ylabel('Trip Count')
plt.legend(title='Day of Week', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

#=Save Cleaned Data
df_bike.to_csv('merged_cleaned_citibike_jan_mar_2025.csv', index=False)

print("Data preparation, analysis, and visualizations completed successfully.")
