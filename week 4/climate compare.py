import pandas as pd
import matplotlib.pyplot as plt

# pd.read_csv("filename.csv") reads the CSV file and stores the data in a structured format.
# auckland_df holds Auckland's temperature data, and christchurch_df holds Christchurch's data.
auckland_df = pd.read_csv("Auckland temp_1992.csv")
christchurch_df = pd.read_csv("Christchurch temp_1992.csv")

# Rename columns for clarity. inplace=True ensures changes are applied directly to the DataFrame.
auckland_df.rename(columns={"PERIOD": "Month", "STATS_VALUE": "Temperature_Auckland"}, inplace=True)
christchurch_df.rename(columns={"PERIOD": "Month", "STATS_VALUE": "Temperature_Christchurch"}, inplace=True)

# Merge on Month
df = pd.merge(auckland_df, christchurch_df, on="Month")

# Plot comparison
plt.figure(figsize=(10, 5))
plt.plot(df["Month"], df["Temperature_Auckland"], marker="o", label="Auckland")
plt.plot(df["Month"], df["Temperature_Christchurch"], marker="s", label="Christchurch")

# Formatting plot
plt.title("Monthly Temperature Comparison: Auckland vs Christchurch (1992)")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

# Show plot
plt.show()