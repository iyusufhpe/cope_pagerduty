import time
import json
from pdpyras import APISession
from token_getter import api_token
import csv
import pandas as pd
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AlertsFetcher:
    def __init__(self, api_token):
        self.api_token = api_token
        self.session = APISession(api_token)
        self.session.verify = False

    def save_to_file_bulk(self, alerts_data, filename, mode='a'):
        try:
            with open(filename, mode) as file:
                for alert in alerts_data:
                    json.dump(alert, file, indent=4)
                    file.write(',\n')  # Add a comma and newline after each JSON object
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")

    def fetch_alerts_for_incident(self, incident_id):
        # Fetch alerts for a specific incident
        response = self.session.rget(f'/incidents/{incident_id}/alerts')
        return response

    def batch_download(self, input_incident_ids, output_alerts):
        batch_size = 5  # Number of incidents to fetch alerts for before saving to file
        total_ids = len(input_incident_ids)
        all_alerts_data = []

        # Open the file in write mode initially to start with an empty file
        with open(output_alerts, 'w') as file:
            file.write('[')  # Start the JSON array

        for i in range(total_ids):
            incident_id = input_incident_ids[i]
            alerts = pd.DataFrame(self.fetch_alerts_for_incident(incident_id))
            alerts_data = alerts.to_dict(orient='records')
            all_alerts_data.extend(alerts_data)
            print(f"Fetched alerts for incident {incident_id} : Progress => ({i + 1}/{total_ids})")

            # Save to file after every batch_size calls
            if (i + 1) % batch_size == 0 or (i + 1) == total_ids:
                self.save_to_file_bulk(all_alerts_data, output_alerts, mode='a')
                all_alerts_data = []  # Clear the list after saving to file
                print(f"Processed batch with {i + 1} incidents, waiting for 5 seconds...")
                time.sleep(2)

        # Remove the last comma and newline, then close the JSON array
        with open(output_alerts, 'rb+') as file:
            file.seek(-2, 2)  # Move the cursor to the position of the last comma
            file.truncate()  # Remove the last comma and newline
            file.write(b'\n]')  # Close the JSON array

    def read_incident_ids_from_csv(self, csv_file):
        incident_ids = []
        try:
            with open(csv_file, mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    incident_ids.append(row[0])
        except IOError as e:
            print(f"Error reading from file {csv_file}: {e}")
        return incident_ids

    def main(self):
        # csv_input_incidents_ids = './data/incidents_0701_1007_ids.csv'
        # incident_alerts_json = './data/incidents_0701_1007_ids_alerts.json'
        
        csv_input_incidents_ids = './data/1ids.csv'
        incident_alerts_json = './data/1alerts.json'

        incident_ids = self.read_incident_ids_from_csv(csv_input_incidents_ids)
        self.batch_download(incident_ids, incident_alerts_json)

if __name__ == '__main__':
    fetcher = AlertsFetcher(api_token)
    fetcher.main()