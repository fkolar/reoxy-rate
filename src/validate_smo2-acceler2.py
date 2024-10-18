import numpy as np
import pandas as pd

# Create a dataset with only 'time' and 'SmO2' columns (input data)
data = {
    'time': [1, 2, 3, 4, 5, 6, 7],
    'SmO2': [60, 61, 61, 61, 59, 62, 62]
}

df = pd.DataFrame(data)

# Ensure time starts from 1 and calculate SmO2 acceleration (SmO2')
df = df.sort_values('time')

# Calculate SmO2' (SmO2 acceleration)
df['SmO2_accel'] = df['SmO2'].diff() / df['time'].diff()

# Handle the first NaN and any inf values
df['SmO2_accel'].fillna(0, inplace=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Calculate SmO2'' (SmO2 jerk)
df['SmO2_jerk'] = df['SmO2_accel'].diff() / df['time'].diff()
df['SmO2_jerk'].fillna(0, inplace=True)


# Final output matching the target dataset
result_df = df[['time', 'SmO2', 'SmO2_accel', 'SmO2_jerk']]

# Compare with expected values
print(result_df)
