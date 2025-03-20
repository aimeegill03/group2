import os
import pandas as pd

# Define paths
input_folder = "XXZZ"
output_folder = "XXZZ_no_jump"
os.makedirs(output_folder, exist_ok=True)

def remove_extreme_swings(chunk):
    chunk = chunk.sort_values(by=["id", "eom"])  # Ensure data is sorted by stock ID and date

    to_remove = set()

    for i in range(len(chunk) - 2):
        row = chunk.iloc[i]
        next_row = chunk.iloc[i + 1]
        after_next_row = chunk.iloc[i + 2]

        if row["id"] == next_row["id"] == after_next_row["id"]:  # Ensure same stock

            original_price = row["prc"]
            jump_price = next_row["prc"]
            post_jump_price = after_next_row["prc"]

            if (
                jump_price >= 4 * original_price and  # Jump 4x or more
                post_jump_price <= 2 * original_price  # Falls back to 2x or lower
            ):
                to_remove.add(next_row.name)  # Mark the jump month for removal

    return chunk.drop(index=to_remove)

def process_csv(file_path, output_path, chunk_size=100000):
    chunks = []

    for chunk in pd.read_csv(file_path, parse_dates=["eom"], chunksize=chunk_size):
        cleaned_chunk = remove_extreme_swings(chunk)
        chunks.append(cleaned_chunk)

    processed_df = pd.concat(chunks, ignore_index=True)
    processed_df.to_csv(output_path, index=False)

# Process each CSV file
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)
        print(f"Processing {file_name}...")
        process_csv(input_path, output_path)
        print(f"Saved cleaned data to {output_path}")

print("All files processed successfully.")
