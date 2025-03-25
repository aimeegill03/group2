import os
import pandas as pd

# Define paths
input_folder = "XXZZ_winsorized"
output_folder = "XXZZ_no_0_no_miss"
os.makedirs(output_folder, exist_ok=True)

def remove_zero_and_missing_returns(file_path, output_path, chunk_size=100000):
    with pd.read_csv(file_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            # Drop rows where 'monthly_returns' is NaN or zero
            chunk = chunk.dropna(subset=["monthly_returns"])
            chunk = chunk[chunk["monthly_returns"] != 0]

            # Append to output file
            chunk.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)

# Process each CSV file
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        print(f"Processing {file_name}...")
        remove_zero_and_missing_returns(input_path, output_path)
        print(f"Saved cleaned data to {output_path}")

print("All files processed successfully.")
