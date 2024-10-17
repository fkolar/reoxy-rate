import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid


file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'].str.strip(), format='%H:%M:%S')

# Calc only CP from the 3MT
start_time = '07:41:15'
end_time = '07:44:15'
start_time_dt = pd.to_datetime(start_time, format='%H:%M:%S')
end_time_dt = pd.to_datetime(end_time, format='%H:%M:%S')

# Filter data
filtered_data = df[(df['timestamp'] >= start_time_dt) & (df['timestamp'] <= end_time_dt)].copy()

# Create duration in seconds from the timestamp
filtered_data['Duration (sec)'] = (filtered_data['timestamp'] - filtered_data['timestamp'].iloc[0]).dt.total_seconds()

# I have to strip some initial power ramp up so it start from teh highest power number,
# not really take all before I climb there.
max_power_idx = filtered_data['power'].idxmax()
filtered_data = filtered_data.loc[max_power_idx:].reset_index(drop=True)

# Power-Duration model function
def power_duration_curve(t, CP, W_prime):
    return CP + W_prime / t

# Calc the last 30 seconds' avg power as CP  - based on some study I found
last_30_seconds = filtered_data['Duration (sec)'].max() - 30
last_30s_data = filtered_data[filtered_data['Duration (sec)'] >= last_30_seconds]
CP_actual = last_30s_data['power'].mean()

# Calc W' from above CP (first 2:30 minutes)
data_above_cp = filtered_data[(filtered_data['Duration (sec)'] <= 150) & (filtered_data['power'] > CP_actual)]
power_above_cp = data_above_cp['power'] - CP_actual
duration_above_cp = data_above_cp['Duration (sec)']
W_prime_actual = trapezoid(power_above_cp, duration_above_cp)

# Use filtered data points for power and duration
power = filtered_data['power'].values
duration = filtered_data['Duration (sec)'].values


popt, _ = curve_fit(power_duration_curve, duration, power)
CP_est, W_prime_est = popt

# Plot the Power-Duration curve
t_fit = np.linspace(min(duration), max(duration), 1000)
P_fit = power_duration_curve(t_fit, CP_est, W_prime_est)

plt.plot(t_fit, P_fit, label='Fitted Power-Duration Curve (Estimated)', color='black', zorder=3)
plt.scatter(duration, power, label='Data Points', color='lightblue', zorder=5, alpha=0.6)

# Add a horizontal line for Actual CP
plt.axhline(y=CP_actual, color='red', linestyle='--', label=f'Actual CP = {CP_actual:.1f} W', zorder=3)

# Some labels
plt.xlabel('Time (seconds)')
plt.ylabel('Power Output (W)')
plt.title(f'Power-Duration Curve (Interval: {start_time} to {end_time})')

# Add annotation for CP and W'
W_prime_actual_kj = W_prime_actual / 1000
W_prime_est_kj = W_prime_est / 1000
plt.text(min(duration) + 10, CP_actual + 10,
         f'Actual CP = {CP_actual:.1f} W\nActual W\' = {W_prime_actual_kj:.1f} kJ',
         color='black', zorder=6)


plt.text(min(duration) + 10, CP_actual - 50,
         f'Estimated CP = {CP_est:.1f} W\nEstimated W\' = {W_prime_est_kj:.1f} kJ',
         color='blue', zorder=6)


plt.legend(loc='upper right')
plt.grid(True)
plt.xlim([min(duration), max(duration)])
plt.ylim([0, max(power) + 100])


plt.show()


print(f"Actual Critical Power (CP): {CP_actual:.2f} W")
print(f"Actual W': {W_prime_actual:.2f} J ({W_prime_actual_kj:.2f} kJ)")
print(f"Estimated Critical Power (CP): {CP_est:.2f} W")
print(f"Estimated W': {W_prime_est:.2f} J ({W_prime_est_kj:.2f} kJ)")
