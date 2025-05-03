import pandas as pd

# Read the Parquet file
df = pd.read_parquet("Sample_data_2.parquet")

# Display the first few rows
print("Number of rows in the file:", len(df))