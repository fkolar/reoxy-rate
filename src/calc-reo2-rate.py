import pandas as pd
from datetime import datetime

# Load the data from a CSV file (replace 'your_data.csv' with the path to your file)
#df = pd.read_csv('../data/right-leg.csv')
df = pd.read_csv('../data/right-leg-2.csv')
# df = pd.read_csv('../data/trainred/right-arm.csv')


# Different time handling  - one that comes out from Moxy vs train.red
try:
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    df['Time_in_seconds'] = (df['Time'] - df['Time'].min()).dt.total_seconds()
except ValueError:
    df['Time_in_seconds'] = pd.to_numeric(df['Time'])

# Find the lowest SmO2 point (This is represent occlusion )
lowest_point = df[df['SmO2'] == df['SmO2'].min()]
recovery_start_time = lowest_point['Time_in_seconds'].iloc[0]
lowest_smO2 = lowest_point['SmO2'].iloc[0]

# Should, wait to the highest point or filter data for the next 2.5 minutes (150 seconds) after occlusion ?
post_occlusion_df = df[df['Time_in_seconds'] > recovery_start_time]
post_occlusion_df = post_occlusion_df[post_occlusion_df['Time_in_seconds'] <= recovery_start_time + 150]

# Calculate the slope (SmO2 change per second) over this 2.5-minute period
if len(post_occlusion_df) > 1:
    smO2_change = post_occlusion_df['SmO2'].iloc[-1] - post_occlusion_df['SmO2'].iloc[0]
    time_change = post_occlusion_df['Time_in_seconds'].iloc[-1] - post_occlusion_df['Time_in_seconds'].iloc[0]
    reactive_oxygenation_rate = smO2_change / time_change

    # Print results
    print(f"Lowest SmO2 (occlusion): {lowest_smO2}")
    print(f"Recovery Start Time: {recovery_start_time} seconds")
    print(f"SmO2 at 2.5 minutes post-occlusion: {post_occlusion_df['SmO2'].iloc[-1]}")
    print(f"Reactive Oxygenation Rate (slope %/sec): {reactive_oxygenation_rate}")
    print(f"Reactive Oxygenation Rate (slope %/min): {reactive_oxygenation_rate * 60}")
else:
    print("Not enough data points after occlusion to calculate the reactive oxygenation rate.")