import json
import pandas as pd

def main(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    # Normalize the JSON data
    # Update the record_path based on the actual JSON structure
    df = pd.DataFrame(data)
    
    # Print all column names
    print("Column names:")
    print(df.columns.tolist())
    
        # Access nested fields manually
    # Assuming 'Q0FUHDIJXCD1Q4' is the key for the nested list
    nested_df = pd.DataFrame(df['Q0FUHDIJXCD1Q4'].dropna().values[0])
    
    # Print the nested DataFrame
    print("Nested DataFrame:")
    print(nested_df.columns.tolist())
    nested_df.

    
if __name__ == '__main__':
    json_file = 'D:\\Data\\hpe\\pagerduty\\alerts\\incident_alerts.json'
    main(json_file) 