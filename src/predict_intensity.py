# File: predict_intensity.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from utils.smo2_calculations import add_additional_features, apply_clustering, threshold_based_classification

# Step 1: Load the data
file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)

# Step 2: Apply function to add SmO2 acceleration and jerk metrics
df_with_metrics = add_additional_features(df, time_column='timestamp', smo2_column='SmO2')

# Step 3: Experiment with clustering
df_with_metrics = apply_clustering(df_with_metrics, features=['SmO2_rolling_mean', 'SmO2_accel', 'SmO2_jerk'], method='dbscan')

# Step 4: Apply threshold-based rules for classification
df_with_metrics = threshold_based_classification(df_with_metrics)

# Step 5: Plot the results
plt.figure(figsize=(20, 7))
scatter = plt.scatter(df_with_metrics['timestamp'], df_with_metrics['SmO2'], c=df_with_metrics['Cluster'], cmap='viridis')
plt.xlabel('Time')
plt.ylabel('SmO2')
plt.title('Clusters and Intensity Phases')
plt.colorbar(label='Cluster')
plt.show()
