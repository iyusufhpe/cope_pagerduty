import pandas as pd
import os

def convert_incident_json_to_combined_parquet(json_folder, parquet_file):
    # List to hold DataFrames
    data_frames = []

    # Iterate over all JSON files in the input directory
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json') and json_file.startswith('incident'):
            json_path = os.path.join(json_folder, json_file)
            # Read the JSON file into a DataFrame
            df = pd.read_json(json_path)
            
            # Check for struct type columns with no child fields and remove them
            for column in df.columns:
                if isinstance(df[column].iloc[0], dict) and not df[column].iloc[0]:
                    df.drop(columns=[column], inplace=True)
                    
            data_frames.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Write the combined DataFrame to a Parquet file
    combined_df.to_parquet(parquet_file, index=False)

    print(f'Combined data saved to {parquet_file}')

# Example usage
if __name__ == '__main__':
    json_folder = 'D:\\Data\\hpe\\pagerduty\\json-files'
    parquet_file = 'D:\\Data\\hpe\\pagerduty\\combined_incidents.parquet'
    convert_incident_json_to_combined_parquet(json_folder, parquet_file)