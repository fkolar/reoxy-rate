import pandas as pd
from datetime import datetime

# Load the data from a CSV file (replace 'your_data.csv' with the path to your file)
#df = pd.read_csv('../data/right-leg.csv')
df = pd.read_csv('../data/left-leg.csv')
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

# Lowest value
lowest_point = df[df['SmO2'] == df['SmO2'].min()]
recovery_start_time = lowest_point['Time'].iloc[0]
lowest_smO2 = lowest_point['SmO2'].iloc[0]

# recovery value
recovery_end_time = df['Time'].iloc[-1]
highest_smO2 = df['SmO2'].iloc[-1]

recovery_duration = (recovery_end_time - recovery_start_time).total_seconds()

smO2_difference = highest_smO2 - lowest_smO2

reoxygenation_rate_per_sec = smO2_difference / recovery_duration
reoxygenation_rate_per_min = reoxygenation_rate_per_sec * 60

# Print the results
print(f"Lowest SmO2: {lowest_smO2}")
print(f"Recovery Start Time: {recovery_start_time}")
print(f"Highest SmO2: {highest_smO2}")
print(f"Recovery End Time: {recovery_end_time}")
print(f"Reoxygenation Rate (%/sec): {reoxygenation_rate_per_sec}")
print(f"Reoxygenation Rate (%/min): {reoxygenation_rate_per_min}")
