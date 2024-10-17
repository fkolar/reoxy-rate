import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'].str.strip(), format='%H:%M:%S')

#  start and stop frame for the 3MT only. Or should I include whole session with warmup ?
start_time = '07:41:15'
end_time = '07:44:15'

# If -1 take full session
if start_time != -1:
    start_time_dt = pd.to_datetime(start_time, format='%H:%M:%S')
else:
    start_time_dt = df['timestamp'].min()  # Take the earliest timestamp

if end_time != -1:
    end_time_dt = pd.to_datetime(end_time, format='%H:%M:%S')
else:
    end_time_dt = df['timestamp'].max()  # Take the latest timestamp


filtered_data = df[(df['timestamp'] >= start_time_dt) & (df['timestamp'] <= end_time_dt)].copy()
filtered_data['Duration (sec)'] = (filtered_data['timestamp'] - filtered_data['timestamp'].iloc[0]).dt.total_seconds()
filtered_data['SmO2_smoothed'] = filtered_data['SmO2'].rolling(window=10, center=True).mean()

# Deoxygenation Rates (ΔSmO2) after smoothing - Is this correct?
filtered_data['De-oxy rate'] = filtered_data['SmO2_smoothed'].diff() / filtered_data['Duration (sec)'].diff()
filtered_data = filtered_data.dropna().reset_index(drop=True)


deoxy_rate = filtered_data['De-oxy rate'].values
duration = filtered_data['Duration (sec)'].values


def critical_metabolic_rate(t, CMR, M_prime):
    return CMR + M_prime / t


popt, pcov = curve_fit(critical_metabolic_rate, duration, deoxy_rate)
CMR, M_prime = popt

# Step 11: Print the estimated parameters
print(f"Estimated Critical Metabolic Rate (CMR): {CMR:.5f} %/s")
print(f"Estimated M': {M_prime:.5f}")
