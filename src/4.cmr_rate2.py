# File: main_script.py
import pandas as pd
from utils.cmr_calculation import calculate_cmr

file_path = '../data/3mt.csv'
df = pd.read_csv(file_path)

start_time = '07:41:15'
end_time = '07:44:15'

CMR, M_prime = calculate_cmr(df, start_time, end_time)

print(f"Estimated Critical Metabolic Rate (CMR): {CMR:.5f} %/s")
print(f"Estimated M': {M_prime:.5f}")
