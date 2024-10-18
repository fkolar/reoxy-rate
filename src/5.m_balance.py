from utils.m_balance_calculation import calculate_m_balance

file_path = '../data/3mt.csv'

start_time = '-1'
end_time = '-1'

filtered_data, CMR, M_prime = calculate_m_balance(file_path, start_time, end_time)


print(f"Estimated Critical Metabolic Rate (CMR): {CMR:.5f} %/s")
print(f"Estimated M': {M_prime:.5f}")


fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot SmO2
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('SmO2 (%)', color='tab:blue')
ax1.plot(filtered_data['Duration (sec)'], filtered_data['SmO2_smoothed'], color='tab:blue', label='SmO2 (smoothed)')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# second y-axis for deoxy rate
ax2 = ax1.twinx()
ax2.set_ylabel('De-oxygenation Rate (ΔSmO2)', color='tab:orange')
ax2.plot(filtered_data['Duration (sec)'], filtered_data['De-oxy rate'], color='tab:orange', label='De-oxygenation Rate (ΔSmO2)')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Plot power data
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Power (W)', color='tab:green')
ax3.plot(filtered_data['Duration (sec)'], filtered_data['power'], color='tab:green', label='Power')
ax3.tick_params(axis='y', labelcolor='tab:green')

# Plot M' Balance
ax4 = ax1.twinx()
ax4.spines['right'].set_position(('outward', 120))  # Offset the fourth axis
ax4.set_ylabel("M' Balance", color='tab:red')
ax4.plot(filtered_data['Duration (sec)'], filtered_data['M_balance'], color='tab:red', label="M' Balance")
ax4.tick_params(axis='y', labelcolor='tab:red')


plt.title(f"M' Balance with Deoxygenation Rate, SmO2, Power, and M' Balance (from {start_time} to {end_time})")


fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')
ax3.legend(loc='upper right')
ax4.legend(loc='lower right')

plt.show()
