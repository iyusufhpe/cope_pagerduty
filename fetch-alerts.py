import os
import time
import json
from pdpyras import APISession
from token_getter import api_token
import csv
import pandas as pd

# Initialize the PagerDuty API session
session = APISession(api_token)

# Disable SSL verification for the session
session.verify = False

def save_to_file_bulk(alerts_data, filename):
    try:
        with open(filename, mode='a') as file:
            json_data = alerts_data.to_dict(orient='records')
            json.dump(json_data, file, indent=4)
            file.write('\n')  # Add a newline after each JSON object
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def fetch_alerts_for_incident(incident_id):
    # Fetch alerts for a specific incident
    response = session.rget(f'/incidents/{incident_id}/alerts')
    return response

def batch_download(input_incident_ids, output_alerts):
    batch_size = 900
    total_ids = len(input_incident_ids)
    all_alerts_data = []

    for i in range(total_ids):
        incident_id = input_incident_ids[i]
        alerts = pd.DataFrame(fetch_alerts_for_incident(incident_id))
        all_alerts_data.extend(alerts.to_dict(orient='records'))
        print(f"Fetched alerts for incident {incident_id}")

        # Save to file after every 900 calls
        if (i + 1) % batch_size == 0:
            save_to_file_bulk(all_alerts_data, output_alerts)
            all_alerts_data = []  # Clear the list after saving
            print(f"Saved alerts data to {output_alerts} after {batch_size} calls")
            print("Waiting for 5 seconds...")
            time.sleep(5)

    # Save any remaining alerts data after processing all incidents
    if all_alerts_data:
        save_to_file_bulk(all_alerts_data, output_alerts)
        print(f"Saved remaining alerts data to {output_alerts}")

def save_to_file_bulk(alerts_data, filename):
    try:
        with open(filename, mode='w') as file:
            json.dump(alerts_data, file, indent=4)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def read_incident_ids_from_csv(csv_file_path):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"The file {csv_file_path} does not exist.")
    
    incident_ids = []
    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:  # Check if the row is not empty
                    incident_ids.append(row[0])  # Assuming incident IDs are in the first column
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    
    return incident_ids

if __name__ == '__main__':
    # csv_input_incidents_ids = '/home/iyusuf/projects/data_pagerduty/id_incidents_test.csv' # uncomment to test
    # print(read_incident_ids_from_csv(csv_input_incidents_ids)) # unocmment to test
    csv_input_incidents_ids = '/home/iyusuf/projects/data_pagerduty/ids-augsep24.csv'
    incident_alerts_json = '/home/iyusuf/projects/data_pagerduty/alerts_augsep24.json'
    incident_ids = read_incident_ids_from_csv(csv_input_incidents_ids)
    batch_download(incident_ids, incident_alerts_json)
