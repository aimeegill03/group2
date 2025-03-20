import os
import pandas as pd

# Define input and output folder paths
input_folder = "XXZZ_no_jump"
output_folder = "XXZZ_with_returns"
chunk_size = 100000  # Adjust based on memory availability

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def process_large_csv(file_path, output_path):
    print(f"Processing {file_path}...")

    # Read a small sample to infer data types
    sample_df = pd.read_csv(file_path, nrows=10000, dtype=str)  # Read everything as string first

    # Explicitly set column data types
    dtypes = {col: "str" for col in sample_df.columns}  # Read all columns as strings initially

    # Open output file
    first_chunk = True

    # Dictionary to store last month's price per ID
    last_prices = {}

    # Process CSV in chunks
    with pd.read_csv(file_path, dtype=dtypes, chunksize=chunk_size) as reader:
        for chunk in reader:
            # Convert 'eom' to datetime
            chunk["eom"] = pd.to_datetime(chunk["eom"], errors="coerce")  # Convert explicitly to datetime

            # Convert 'prc' to numeric, coercing errors to NaN
            chunk["prc"] = pd.to_numeric(chunk["prc"], errors="coerce")

            # Drop rows with missing critical values
            chunk = chunk.dropna(subset=["id", "eom", "prc"])

            # Sort chunk by id and eom to ensure correct order
            chunk = chunk.sort_values(by=["id", "eom"])

            # Compute monthly returns per ID
            monthly_returns_list = []
            for id_val, group in chunk.groupby("id"):
                group = group.sort_values("eom")

                # Carry forward previous month's price if available
                if id_val in last_prices:
                    previous_price = last_prices[id_val]
                    group.loc[group.index[0], "monthly_returns"] = (group["prc"].iloc[0] - previous_price) / previous_price

                # Compute returns for the rest
                group["monthly_returns"] = group["prc"].pct_change()

                # Store the last price for this ID
                last_prices[id_val] = group["prc"].iloc[-1]

                monthly_returns_list.append(group)

            # Concatenate the grouped results
            if monthly_returns_list:
                chunk = pd.concat(monthly_returns_list)

            # Append to output file
            chunk.to_csv(output_path, index=False, mode="w" if first_chunk else "a", header=first_chunk)
            first_chunk = False

    print(f"Finished processing {file_path} -> Saved to {output_path}")

# Process all CSV files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)  # Save output in processed_files/
        process_large_csv(input_path, output_path)