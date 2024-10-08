import time
import json
from pdpyras import APISession
from token_getter import api_token
import csv
import pandas as pd
import urllib3

# Initialize the PagerDuty API session
session = APISession(api_token)

# Disable SSL verification for the session
session.verify = False
# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def save_to_file_bulk(alerts_data, filename, mode='a'):
    try:
        with open(filename, mode) as file:
            for alert in alerts_data:
                json.dump(alert, file, indent=4)
                file.write(',\n')  # Add a comma and newline after each JSON object
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def fetch_alerts_for_incident(incident_id):
    # Fetch alerts for a specific incident
    response = session.rget(f'/incidents/{incident_id}/alerts')
    return response

def batch_download(input_incident_ids, output_alerts):
    batch_size = 900  # Number of incidents to fetch alerts for before saving to file
    total_ids = len(input_incident_ids)

    # Open the file in write mode initially to start with an empty file
    with open(output_alerts, 'w') as file:
        file.write('[')  # Start the JSON array

    for i in range(total_ids):
        incident_id = input_incident_ids[i]
        alerts = pd.DataFrame(fetch_alerts_for_incident(incident_id))
        alerts_data = alerts.to_dict(orient='records')
        
        # Append the alerts data to the file
        save_to_file_bulk(alerts_data, output_alerts, mode='a')
        print(f"Fetched and saved alerts for incident {incident_id} : Progress => ({i + 1}/{total_ids})")

        # Pause after every batch_size calls to avoid hitting rate limits
        if (i + 1) % batch_size == 0:
            print(f"Processed {i + 1} incidents, waiting for 5 seconds...")
            time.sleep(2)

    # Remove the last comma and newline, then close the JSON array
    with open(output_alerts, 'rb+') as file:
        file.seek(-2, 2)  # Move the cursor to the position of the last comma
        file.truncate()  # Remove the last comma and newline
        file.write(b'\n]')  # Close the JSON array

def read_incident_ids_from_csv(csv_file):
    incident_ids = []
    try:
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                incident_ids.append(row[0])
    except IOError as e:
        print(f"Error reading from file {csv_file}: {e}")
    return incident_ids

if __name__ == '__main__':
    # csv_input_incidents_ids = './data/incidents_0701_1007_ids.csv'
    # incident_alerts_json = './data/incidents_0701_1007_ids_alerts.json'
    
    csv_input_incidents_ids = './data/incident_ids_0921_0930.csv'
    incident_alerts_json = './data/incident_ids_0921_0930_alerts.json'

    incident_ids = read_incident_ids_from_csv(csv_input_incidents_ids)
    batch_download(incident_ids, incident_alerts_json)