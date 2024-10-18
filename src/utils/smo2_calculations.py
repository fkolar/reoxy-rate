import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


def add_smo2_metrics(df, time_column='time', smo2_column='SmO2'):
    # Ensure the DataFrame contains the required columns
    if time_column not in df.columns or smo2_column not in df.columns:
        raise ValueError(f"The DataFrame must contain '{time_column}' and '{smo2_column}' columns.")

    # Convert time_column to datetime if it's not already
    if df[time_column].dtype == 'object':
        df[time_column] = pd.to_datetime(df[time_column], errors='coerce')

    # Sort data by time to ensure proper calculation
    df = df.sort_values(time_column)

    # Calculate time differences in seconds
    df['time_diff'] = df[time_column].diff().dt.total_seconds()

    # Calculate SmO2' (SmO2 acceleration)
    df['SmO2_accel'] = df[smo2_column].diff() / df['time_diff']

    # Handle NaN and inf values
    df['SmO2_accel'].fillna(0, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Calculate SmO2'' (SmO2 jerk)
    df['SmO2_jerk'] = df['SmO2_accel'].diff() / df['time_diff']
    df['SmO2_jerk'].fillna(0, inplace=True)

    # Drop the 'time_diff' column if you don't need it anymore
    df.drop(columns=['time_diff'], inplace=True)

    return df


def add_additional_features(df, time_column='time', smo2_column='SmO2'):
    if time_column not in df.columns or smo2_column not in df.columns:
        raise ValueError(f"The DataFrame must contain '{time_column}' and '{smo2_column}' columns.")

    df = df.sort_values(time_column)

    df['SmO2_accel'] = df[smo2_column].diff() / pd.to_numeric(df[time_column].diff())
    df['SmO2_accel'].fillna(0, inplace=True)

    df['SmO2_jerk'] = df['SmO2_accel'].diff() / pd.to_numeric(df[time_column].diff())
    df['SmO2_jerk'].fillna(0, inplace=True)

    # Total SmO2 Drop (max - min)
    df['SmO2_total_drop'] = df[smo2_column].rolling(window=10).max() - df[smo2_column].rolling(window=10).min()

    # SmO2 Recovery Slope (rate of SmO2 increase)
    df['SmO2_recovery_slope'] = df[smo2_column].rolling(window=10).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[0], raw=True)

    df['SmO2_steady_state'] = df['SmO2_accel'].apply(lambda x: 1 if abs(x) < 0.05 else 0)

    df.fillna(0, inplace=True)

    return df


def apply_clustering(df, features, method='kmeans', n_clusters=5):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features])

    if method == 'dbscan':
        model = DBSCAN(eps=0.5, min_samples=10)
        df['Cluster'] = model.fit_predict(scaled_features)
    elif method == 'gmm':
        model = GaussianMixture(n_components=n_clusters, random_state=42)
        df['Cluster'] = model.fit_predict(scaled_features)
    else:
        model = KMeans(n_clusters=n_clusters, random_state=42)
        df['Cluster'] = model.fit_predict(scaled_features)

    return df


def threshold_based_classification(df):
    # Define rules for intensity phases
    df['Phase'] = 'Moderate'  # Default

    # If SmO2_accel is near zero and jerk is near zero, it's steady state or recovery
    df.loc[(df['SmO2_accel'].abs() < 0.05) & (df['SmO2_jerk'].abs() < 0.05), 'Phase'] = 'Recovery'

    # If SmO2_accel is negative and jerk is positive, it indicates high intensity
    df.loc[(df['SmO2_accel'] < 0) & (df['SmO2_jerk'] > 0), 'Phase'] = 'Heavy'

    # Other thresholds/rules can be added
    return df
