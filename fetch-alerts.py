import time
import json
from pdpyras import APISession

# Initialize the PagerDuty API session
api_token = 'your_api_token'
session = APISession(api_token)

def fetch_alerts_for_incident(incident_id):
    # Fetch alerts for a specific incident
    response = session.rget(f'/incidents/{incident_id}/alerts')
    return response

def save_to_file(incident_id, data, filename='incident_alerts.json'):
    # Save each response to a file in JSON format
    with open(filename, 'a') as file:
        file.write(json.dumps({incident_id: data}, indent=4) + '\n')

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

# Example usage
incident_ids = ['id1', 'id2', 'id3', ...]  # Replace with your actual list of incident IDs
batch_download(incident_ids)
