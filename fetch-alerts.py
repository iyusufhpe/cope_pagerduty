import time
import json
from pdpyras import APISession
from token_getter import api_token
import csv

# Initialize the PagerDuty API session
session = APISession(api_token)


def save_to_file(incident_id, data, filename):
    try:
        with open(filename, 'r') as file:
            alerts_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts_list = []

    alerts_list.append({incident_id: data})

    with open(filename, 'w') as file:
        json.dump(alerts_list, file, indent=4)


def fetch_alerts_for_incident(incident_id):
    # Fetch alerts for a specific incident
    response = session.rget(f'/incidents/{incident_id}/alerts')
    return response


def batch_download(incident_ids, filename='incident_alerts.json'):
    batch_size = 960
    total_ids = len(incident_ids)
    
    for i in range(0, total_ids, batch_size):
        batch = incident_ids[i:i + batch_size]
        
        for incident_id in batch:
            alerts = fetch_alerts_for_incident(incident_id)
            # Save the alerts data to the file
            save_to_file(incident_id, alerts, filename)
            print(f"Fetched and saved alerts for incident {incident_id}")
        
        # Pause to respect the rate limit of 960 calls per minute
        if i + batch_size < total_ids:
            print("Pausing for 1 minute to respect rate limit...")
            time.sleep(60)


def read_incident_ids_from_csv(csv_file_path):
    incident_ids = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            incident_ids.append(row[0])  # Assuming incident IDs are in the first column
    return incident_ids


# # Example usage
# incident_ids = ['Q23RA58KK63575', 'Q0FUHDIJXCD1Q4', 'Q0HBWO2BH6UMAQ', 'Q3ZGOBT8W3GWW5', 'Q3XDFUVJR2D45U']  # Replace with your actual list of incident IDs
# batch_download(incident_ids)

# Example usage
csv_file_path = 'D:\\Data\\hpe\\pagerduty\\incidents_ids_aug2024.csv'
incident_ids = read_incident_ids_from_csv(csv_file_path)
batch_download(incident_ids)