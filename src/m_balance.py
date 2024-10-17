import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants set based on the output from cmr_rate.py
CMR = 0.67059
M_prime = -44.63840  # hmmm it seems to be too small and it plots strange thing
M_prime = M_prime * -1


file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'].str.strip(), format='%H:%M:%S')
df['Duration (sec)'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# Sort by time
df = df.sort_values('Duration (sec)')

# This is somethign I am not sure about if this rate of change is correct
# but I try to test the same code in the validate_smo2-acceler and I got the same output as set in
# the Evans smo2 csv file
df['SmO2_diff'] = df['SmO2'].diff()  # Difference in SmO2
df['time_diff'] = df['Duration (sec)'].diff()  # Difference in time
df['SmO2_accel'] = df['SmO2_diff'] / df['time_diff']  # SmO2' = ΔSmO2 / Δtime


df['SmO2_accel'] = df['SmO2_accel'].fillna(0)

# Calculate second derivative (jerk) as the rate of change of SmO2' over time
df['SmO2_accel_diff'] = df['SmO2_accel'].diff()  # Difference in SmO2'
df['SmO2_jerk'] = df['SmO2_accel_diff'] / df['time_diff']  # SmO2'' = ΔSmO2' / Δtime


df['SmO2_jerk'] = df['SmO2_jerk'].fillna(0)
df.drop(columns=['SmO2_diff', 'time_diff', 'SmO2_accel_diff'], inplace=True)


M_bal = np.zeros(len(df))
M_bal[0] = M_prime  # Start with full M_prime
tau_recovery = 300

# Step 5: Apply the M' balance model based on the rolling SmO2 rate (acceleration)
for i in range(1, len(df)):
    dt = df['Duration (sec)'].iloc[i] - df['Duration (sec)'].iloc[i - 1]
    d_rate = df['SmO2_accel'].iloc[i]  # Acceleration rate

    if d_rate < CMR:  # Depletion of M'
        M_bal[i] = M_bal[i - 1] - (CMR - d_rate) * dt
    else:  # Restoration of M'
        M_bal[i] = M_bal[i - 1] + (M_prime - M_bal[i - 1]) * (1 - np.exp(-dt / tau_recovery))

    # Ensure M' balance does not go below 0 or above M'
    M_bal[i] = max(0, min(M_prime, M_bal[i]))

# Step 6: Add M' balance to the data frame
df['M_bal'] = M_bal

# Step 7: Plot M' Balance, SmO2, and Power on the Y-axes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot M' Balance on the left y-axis (red)
ax1.plot(df['Duration (sec)'], df['M_bal'], label="M' Balance", color='red')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel("M' Balance (Joules)", color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Create a second y-axis to plot SmO2 (blue)
ax2 = ax1.twinx()
ax2.plot(df['Duration (sec)'], df['SmO2'], label='SmO2', color='blue')
ax2.set_ylabel('Muscle oxygenation (%)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Create a third y-axis to plot Power (green)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # Offset the power axis
ax3.plot(df['Duration (sec)'], df['power'], label='Power', color='green')
ax3.set_ylabel('Power (Watts)', color='green')
ax3.tick_params(axis='y', labelcolor='green')

# Combine legends from all three y-axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='best')

plt.title("M' Balance, SmO2, and Power Over Time")
plt.grid(True)
plt.show()

# Output the final data
df.to_csv('../data/M_bal_output_with_power_smo2.csv', index=False)  # Save results to a CSV file
