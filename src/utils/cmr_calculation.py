import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def calculate_cmr(df, start_time, end_time, smoothing_window=10):
    df['timestamp'] = pd.to_datetime(df['timestamp'].str.strip(), format='%H:%M:%S')

    start_time_dt = pd.to_datetime(start_time, format='%H:%M:%S')
    end_time_dt = pd.to_datetime(end_time, format='%H:%M:%S')

    filtered_data = df[(df['timestamp'] >= start_time_dt) & (df['timestamp'] <= end_time_dt)].copy()
    filtered_data['Duration (sec)'] = (filtered_data['timestamp'] - filtered_data['timestamp'].iloc[0]).dt.total_seconds()
    filtered_data['SmO2_smoothed'] = filtered_data['SmO2'].rolling(window=smoothing_window, center=True).mean()
    filtered_data['De-oxy rate'] = filtered_data['SmO2_smoothed'].diff() / filtered_data['Duration (sec)'].diff()


    filtered_data = filtered_data.dropna().reset_index(drop=True)


    deoxy_rate = filtered_data['De-oxy rate'].values
    duration = filtered_data['Duration (sec)'].values

    # Ccritical Metabolic Rate (CMR) function
    def critical_metabolic_rate(t, CMR, M_prime):
        return CMR + M_prime / t

    # Do curve fitting to estimate CMR and M'
    popt, _ = curve_fit(critical_metabolic_rate, duration, deoxy_rate)
    CMR, M_prime = popt

    return CMR, M_prime
