import requests
import json
import time
import pandas as pd
from token_getter import api_token

def fetch_incidents(starting_after=None):
    url = "https://api.pagerduty.com/analytics/raw/incidents"
    headers = {
        'Authorization': f"Token token={api_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "filters": {
            "created_at_start": "2024-09-01T00:00:00-00:00",
            "created_at_end": "2024-09-02T23:59:59-00:00"
        },
        "limit": 1000,
        "order": "asc",
        "order_by": "created_at",
        "time_zone": "Etc/UTC"
    }
    if starting_after:
        payload["starting_after"] = starting_after

    response = requests.post(url, headers=headers, json=payload, verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Initialize an empty DataFrame to store all data elements
all_data_df = pd.DataFrame()

# Initial fetch
data = fetch_incidents()
all_data_df = pd.DataFrame(data['data'])

# Pagination loop
while data.get('more'):
    starting_after = data['last']
    data = fetch_incidents(starting_after)
    new_data_df = pd.DataFrame(data['data'])
    all_data_df = pd.concat([all_data_df, new_data_df], ignore_index=True)
    
    # Delay to respect rate limit
    time.sleep(5.0)  # 1/16 seconds
    
# Optionally, save the combined DataFrame to a JSON file
all_data_df.to_json('combined_response_output.json', orient='records', indent=2)

# Optionally, save the combined DataFrame to a CSV file
all_data_df.to_csv('combined_response_output.csv', index=False)

print(f"Total incidents fetched: {len(all_data_df)}")