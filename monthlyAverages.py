# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:06:41 2024

@author:  Ian Kahn
    
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]

# Load the water level data
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Initialize a dictionary to store the monthly averages
monthly_averages = {}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        year, month, _, _ = vector
        key = (year, month, station_index)
        
        if key not in monthly_averages:
            monthly_averages[key] = []
        
        monthly_averages[key].append(water_level)

# Calculate the average for each month and station
average_matrix = {}

for key, values in monthly_averages.items():
    year, month, station_index = key
    average_matrix[key] = np.mean(values)

# Convert the dictionary to a structured array for saving
dtype = [('Year', 'i4'), ('Month', 'i4'), ('StationIndex', 'i4'), ('AverageWaterLevel', 'f4')]
average_data = np.array([(year, month, station_index, avg) for (year, month, station_index), avg in average_matrix.items()], dtype=dtype)

# Save the structured array to a .npz file
np.savez('monthly_average_water_levels.npz', average_data=average_data)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = False
if testingFlag:
    print("Year  Month  StationIndex  AverageWaterLevel")
    for row in average_data[:10]:
        print(row)

# Plotting example for a specific station (optional)
station_to_plot = 2  # Change this to the index of the station you want to plot

plot_data = average_data[average_data['StationIndex'] == station_to_plot]

plt.figure(figsize=(10, 6))
plt.plot([datetime(year=row['Year'], month=row['Month'], day=1) for row in plot_data], plot_data['AverageWaterLevel'])
plt.title(f'Monthly Average Water Level for Station {station_to_plot}')
plt.xlabel('Date')
plt.ylabel('Average Water Level (CM)')
plt.show()


#choose the first 3 months of time that i have and print it to the screen 
#(print the average water levels CM)
#and compute it manually , 
#overlay the monthly average over the raw data for a year or 2