import pandas as pd

# Load the Parquet file
df = pd.read_parquet('alerts.parquet')


# Print all column names in column format
print("All column names:")
for col in df.columns:
    print(col)

