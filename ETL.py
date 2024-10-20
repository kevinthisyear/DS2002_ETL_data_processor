import pandas as pd
import sqlite3
import os
import numpy as np
import requests

# Disease.sh API URL
API_URL = "https://disease.sh/v3/covid-19/countries"

# get the list of CSV/JSON in the current directory
files = [f for f in os.listdir() if f.endswith(('.csv', '.json'))]

# display file options including the API and a custom path option
print("\nAvailable sources:")
print("1. Fetch COVID-19 data from Disease.sh API")
for idx, file in enumerate(files, start=2):
    print(f"{idx}. {file}")
print(f"{len(files) + 2}. Enter your own file path")

while True:
    try:
        choice = int(input("Select the source by entering the number: "))
        if choice == 1:
            try:
                response = requests.get(API_URL)
                response.raise_for_status()
                data = pd.json_normalize(response.json())
                print("Fetched COVID-19 data from Disease.sh API.")
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                continue
        elif 2 <= choice <= len(files) + 1:
            file_path = files[choice - 2]
            ext = os.path.splitext(file_path)[1].lower()
            try:
                if ext == '.csv':
                    data = pd.read_csv(file_path)
                elif ext == '.json':
                    try:
                        data = pd.read_json(file_path)
                        print(f"Loaded {file_path} as standard JSON.")
                    except ValueError:
                        data = pd.read_json(file_path, lines=True)
                        print(f"Loaded {file_path} as NDJSON.")
                else:
                    print("Unsupported file format.")
                    continue
            except Exception as e:
                print(f"Error loading file '{file_path}': {e}")
                continue
        elif choice == len(files) + 2:
            file_path = input("Enter the full path to your file: ").strip()
            if not os.path.exists(file_path):
                print("File not found.")
                continue
            ext = os.path.splitext(file_path)[1].lower()
            try:
                if ext == '.csv':
                    data = pd.read_csv(file_path)
                elif ext == '.json':
                    try:
                        data = pd.read_json(file_path)
                        print(f"Loaded {file_path} as standard JSON.")
                    except ValueError:
                        data = pd.read_json(file_path, lines=True)
                        print(f"Loaded {file_path} as NDJSON.")
                else:
                    print("Unsupported file format.")
                    continue
            except Exception as e:
                print(f"Error loading file '{file_path}': {e}")
                continue
        else:
            print("Invalid choice.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue

columns = list(data.columns)
print(f"\nColumns: {columns}\nRecords: {len(data)}, Columns: {len(data.columns)}")

# remove columns
if input("Remove columns? (yes/no): ").strip().lower() == 'yes':
    while True:
        cols_to_remove = input("Enter columns to remove (comma-separated): ").split(',')
        cols_to_remove = [col.strip() for col in cols_to_remove]
        invalid_cols = [col for col in cols_to_remove if col not in columns]
        if invalid_cols:
            print(f"Invalid columns: {invalid_cols}. Please enter valid column names.")
        else:
            data.drop(cols_to_remove, axis=1, inplace=True)
            break

# add a random column
if input("Add a new column with random numbers? (yes/no): ").strip().lower() == 'yes':
    data[input("Enter column name: ")] = np.random.randint(0, 100, size=len(data))

# output format
while True:
    output_format = input("Enter the output format (csv, json, sql): ").strip().lower()
    if output_format in ['csv', 'json', 'sql']:
        break
    print("Invalid format. Choose csv, json, or sql.")

output_name = os.path.splitext(input("Enter output file name: ").strip())[0]
if output_format == 'csv':
    data.to_csv(f"{output_name}.csv", index=False)
elif output_format == 'json':
    data.to_json(f"{output_name}.json", orient='records', lines=False)
elif output_format == 'sql':
    conn = sqlite3.connect(f"{output_name}.db")
    data.to_sql(input("Enter table name: ").strip(), conn, if_exists='replace', index=False)
    conn.close()

print(f"Data saved as {output_name}.{output_format}")