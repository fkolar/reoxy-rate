import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'].str.strip(), format='%H:%M:%S')

# Track the entire session, no start and stop time limitations, OR SHOULD I, only read
# 3MT what I used before ?
df['Duration (sec)'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

CP = 216
W_prime = 3030


power = df['power'].values
duration = df['Duration (sec)'].values


plt.scatter(duration, power, label='Data Points', color='lightblue', zorder=5, alpha=0.6)
plt.axhline(y=CP, color='red', linestyle='--', label=f'Known CP = {CP:.1f} W', zorder=3)

plt.xlabel('Time (seconds)')
plt.ylabel('Power Output (W)')
plt.title('Power Output vs Known Critical Power')

W_prime_kj = W_prime / 1000  # Convert to kJ
plt.text(min(duration) + 10, CP + 10,
         f'Known CP = {CP:.1f} W\nKnown W\' = {W_prime_kj:.1f} kJ',
         color='black', zorder=6)

plt.legend(loc='upper right')
plt.grid(True)
plt.xlim([min(duration), max(duration)])
plt.ylim([0, max(power) + 100])

plt.show()

# ==================
# W' BALANCE MODEL - From Evan but set the values I got from above
# ==================

# Initialize W' balance model with known W_prime
W_bal = np.zeros(len(df))
W_bal[0] = W_prime

# Tau (recovery time constant)
tau_recovery = 250  # This can be adjusted based on experimental data or individual athlete characteristics

# Update W' balance over time
for i in range(1, len(df)):
    dt = df['Duration (sec)'].iloc[i] - df['Duration (sec)'].iloc[i - 1]  # Time step
    power_i = df['power'].iloc[i]

    # Depletion of W' when power is greater than CP
    if power_i > CP:
        W_bal[i] = W_bal[i - 1] - (power_i - CP) * dt
    # Recovery of W' when power is below CP
    else:
        W_bal[i] = W_bal[i - 1] + (W_prime - W_bal[i - 1]) * (1 - np.exp(-dt / tau_recovery))

    # Ensure W' balance stays within 0 and W_prime
    W_bal[i] = max(0, min(W_prime, W_bal[i]))

# Add W' balance to the dataframe
df['W_bal'] = W_bal

# =====================
# PLOT W' BALANCE & POWER
# =====================
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot W' balance on the left y-axis
ax1.plot(df['Duration (sec)'], df['W_bal'], label="W' Balance", color='red')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel("W' Balance (Joules)", color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Create a second y-axis to plot power
ax2 = ax1.twinx()
ax2.plot(df['Duration (sec)'], df['power'], label='Power Output', color='blue')
ax2.set_ylabel('Power Output (Watts)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Combine legends from both y-axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='best')

# Show the plot
plt.title("W' Balance and Power Over Time")
plt.show()
