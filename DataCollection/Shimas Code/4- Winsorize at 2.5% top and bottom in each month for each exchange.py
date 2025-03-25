import os
import pandas as pd
import numpy as np

# Define paths
input_folder = "XXZZ_with_returns"
output_folder = "XXZZ_winsorized"
os.makedirs(output_folder, exist_ok=True)

def winsorize_series(series, lower_quantile=0.025, upper_quantile=0.975):
    lower_bound = series.quantile(lower_quantile)
    upper_bound = series.quantile(upper_quantile)
    return series.clip(lower=lower_bound, upper=upper_bound)

def process_csv(file_path, output_path, chunk_size=100000):
    chunks = []

    for chunk in pd.read_csv(file_path, parse_dates=["eom"], chunksize=chunk_size):
        chunk["eom"] = pd.to_datetime(chunk["eom"])  # Ensure date parsing

        # Winsorize per month
        chunk["monthly_returns"] = chunk.groupby("eom")["monthly_returns"].transform(lambda x: winsorize_series(x))

        chunks.append(chunk)

    # Save the processed data
    processed_df = pd.concat(chunks, ignore_index=True)
    processed_df.to_csv(output_path, index=False)

# Process each CSV file
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        print(f"Processing {file_name}...")
        process_csv(input_path, output_path)
        print(f"Saved winsorized data to {output_path}")

print("All files processed successfully.")
