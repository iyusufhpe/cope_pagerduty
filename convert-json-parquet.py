import os
import pandas as pd

def convert_all_json_to_parquet(json_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all JSON files in the input directory
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)
            parquet_path = os.path.join(output_folder, json_file.replace('.json', '.parquet'))

            # Read the JSON file into a DataFrame
            df = pd.read_json(json_path)

            # Write the DataFrame to a Parquet file
            df.to_parquet(parquet_path, index=False)

            print(f'Converted {json_file} to {parquet_path}')

def convert_incident_json_to_combined_parquet(json_folder, parquet_file):
    # List to hold DataFrames
    data_frames = []

    # Iterate over all JSON files in the input directory
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json') and json_file.startswith('incident'):
            json_path = os.path.join(json_folder, json_file)
            # Read the JSON file into a DataFrame
            df = pd.read_json(json_path)
            data_frames.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Write the combined DataFrame to a Parquet file
    combined_df.to_parquet(parquet_file, index=False)

    print(f'Combined data saved to {parquet_file}')

if __name__ == '__main__':
    
    # # Command: any JSON found in folder will be converted to individual Parquet files
    # convert_all_json_to_parquet('data-samples', 'parquet-output')

    # Command: any file with .json extension and name starts with 'incident' will be converted to one combined Parquet file
    convert_incident_json_to_combined_parquet('data/json-files', 'combined_incidents.parquet')