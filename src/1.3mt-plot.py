import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data
file_path = "../data/3mt.csv"  # replace with your file path
df = pd.read_csv(file_path)

df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

df['power_smooth'] = df['power'].rolling(window=5).mean()
df['SmO2_smooth'] = df['SmO2'].rolling(window=5).mean()

# Only plot the actual 3MT
highlight_start_str = '07:41:15'
highlight_end_str = '07:44:15'
highlight_start = pd.to_datetime(highlight_start_str, format='%H:%M:%S')
highlight_end = pd.to_datetime(highlight_end_str, format='%H:%M:%S')


fig, ax1 = plt.subplots()

# Plot Power on the left y axis
ax1.set_xlabel('Time')
ax1.set_ylabel('Power (W)', color='tab:red')
ax1.plot(df['timestamp'], df['power_smooth'], color='tab:red', label='Smoothed Power')
ax1.tick_params(axis='y', labelcolor='tab:red')

#  another axis  for SmO2
ax2 = ax1.twinx()
ax2.set_ylabel('SmO2 (%)', color='tab:blue')
ax2.plot(df['timestamp'], df['SmO2_smooth'], color='tab:blue', label='Smoothed SmO2')
ax2.tick_params(axis='y', labelcolor='tab:blue')

ax1.axvspan(highlight_start, highlight_end, color='lightgrey', alpha=0.3, label='Highlighted Interval')

# Add vertical and horizontal liens
ax1.grid(True, which='both', axis='x', linestyle='--', linewidth=0.7, color='grey', alpha=0.7)  # Vertical gridlines
ax2.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, color='grey', alpha=0.7)  # Horizontal gridlines

# Beatify labels
plt.xticks(rotation=45)


plt.title('Smoothed Power and SmO2 over Time with Highlighted Interval')
fig.tight_layout()

# Show the plot
plt.show()
