import numpy as np
import pandas as pd

# Use input from Evan and check if I get te
file_path = '../data/evan-smo2.csv'
names = ['time', 'SmO2', 'SmO2_accel', 'SmO2_jerk', 'acceleration','jerk']
df = pd.read_csv(file_path, names=names)

# Ensure SmO2 column and time column exist
if 'SmO2' not in df.columns or 'time' not in df.columns:
    raise ValueError('SmO2 or time column not found in the CSV file.')

# Sort data by time to ensure proper calculation
df = df.sort_values('time')

# Calculate SmO2' (first derivative) - Rate of change of SmO2 over time
df['SmO2_diff'] = df['SmO2'].diff()  # Difference in SmO2
df['time_diff'] = df['time'].diff()   # Difference in time
df['SmO2_accel'] = df['SmO2_diff'] / df['time_diff']  # SmO2' = ΔSmO2 / Δtime

# Fill NaN values generated from the diff() function (use forward fill or fill with 0)
df['SmO2_accel'].fillna(0, inplace=True)

# Calculate SmO2'' (second derivative) - Rate of change of SmO2' over time
df['SmO2_accel_diff'] = df['SmO2_accel'].diff()  # Difference in SmO2'
df['SmO2_jerk'] = df['SmO2_accel_diff'] / df['time_diff']  # SmO2'' = ΔSmO2' / Δtime

# Fill NaN values for SmO2_jerk
df['SmO2_jerk'].fillna(0, inplace=True)

# Drop intermediate columns used for calculation (optional)
df.drop(columns=['SmO2_diff', 'time_diff', 'SmO2_accel_diff'], inplace=True)

# Print the resulting dataframe
print(df[['time', 'SmO2', 'SmO2_accel', 'SmO2_jerk']].head(20))
