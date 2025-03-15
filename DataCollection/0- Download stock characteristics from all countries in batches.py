import wrds
import pandas as pd

# Connect to WRDS
print("Connecting to WRDS...")
wrds_db = wrds.Connection()
print("Connected to WRDS successfully!")

# Downloading and extracting list of countries
print("Downloading list of countries...")
countries = pd.read_excel('https://github.com/bkelly-lab/ReplicationCrisis/raw/master/GlobalFactors/Country%20Classification.xlsx')
countries_list = countries['excntry'].tolist()
print(f"Found {len(countries_list)} countries: {countries_list}")

# Downloading and extracting list of characteristics
print("Downloading list of characteristics...")
chars = pd.read_excel('https://github.com/bkelly-lab/ReplicationCrisis/raw/master/GlobalFactors/Factor%20Details.xlsx')
chars_rel = chars[chars['abr_jkp'].notna()]['abr_jkp'].tolist()
print(f"Found {len(chars_rel)} characteristics to download.")

# Process data in smaller batches
batch_size = 400000  # Adjust this based on your memory constraints

print("Starting data download and processing...")
for country in countries_list:
    print(f"\nProcessing data for country: {country}")
    offset = 0
    while True:
        print(f"Downloading batch {offset // batch_size + 1} for {country}...")
        sql_query = f"""
        SELECT id, eom, excntry, gvkey, permno, size_grp, me, {', '.join(map(str, chars_rel))}
        FROM contrib.global_factor
        WHERE common=1 and exch_main=1 and primary_sec=1 and obs_main=1 and
        excntry = {"'" + str(country) + "'"}
        LIMIT {batch_size} OFFSET {offset}
        """
        data = wrds_db.raw_sql(sql_query)
        if data.empty:
            print(f"No more data found for {country}. Moving to the next country.")
            break
        print(f"Saving batch {offset // batch_size + 1} to {country}_batch_{offset // batch_size}.csv")
        data.to_csv(f'{country}_batch_{offset // batch_size}.csv', mode='a', header=not offset)
        offset += batch_size

print("\nAll data downloaded and processed successfully!")