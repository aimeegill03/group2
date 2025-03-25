import os
import pandas as pd
from collections import defaultdict

# Define the folder containing the CSV files
folder = "Path of the folder containing the csv files"

# Dictionary to store DataFrames for each country code
country_data = defaultdict(list)

# Loop through all CSV files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".csv") and "_batch_" in filename:
        # Extract the country code from the filename
        country_code = filename.split("_")[0]
        
        # Read the CSV file into a DataFrame
        file_path = os.path.join(folder, filename)
        df = pd.read_csv(file_path)
        
        # Append the DataFrame to the list for the corresponding country code
        country_data[country_code].append(df)

# Combine DataFrames for each country and save to a new CSV file
for country_code, dataframes in country_data.items():
    combined_df = pd.concat(dataframes, ignore_index=True)
    output_file = os.path.join(folder, f"{country_code}.csv")
    combined_df.to_csv(output_file, index=False)
    print(f"Saved {output_file}")

print("Done!")
