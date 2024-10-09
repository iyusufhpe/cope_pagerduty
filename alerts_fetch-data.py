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
        batch_size = 925  # Number of incidents to fetch alerts for before saving to file
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
                print(f"Processed {i + 1} incidents, waiting for 5 seconds...")
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


    def time_keeper(self, csv_files):
        start_time = time.time()
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
        print(f"Script started at: {start_time_str}")

        self.main(csv_files)

        end_time = time.time()
        end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
        print(f"Script ended at: {end_time_str}")
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

        # Write start time and end time to a file
        with open('time.txt', 'w') as time_file:
            time_file.write(f"Script started at: {start_time_str}\n")
            time_file.write(f"Script ended at: {end_time_str}\n")
            time_file.write(f"Total execution time: {end_time - start_time:.2f} seconds\n")
            
            
    def main(self, csv_files):
        for csv_file in csv_files:
            incident_ids = self.read_incident_ids_from_csv(csv_file)
            output_file = f"./data/alerts_{csv_file.split('/')[-1].replace('.csv', '.json')}"
            self.batch_download(incident_ids, output_file)
            print(f"Processed file {csv_file} and saved alerts to {output_file}")

if __name__ == '__main__':
    # List of CSV files to process
    csv_files = [
    # './data/ids1.csv',
    # './data/ids2.csv'
    # './data/ids-01-24.csv',
    # './data/ids-01-24-rerun.csv',
    # './data/ids-02-24.csv'
    # './data/ids-03-24.csv',
    # './data/ids-04-24.csv',
    # './data/ids-05-24.csv',
    # './data/ids-06-24.csv'
    # './data/ids-07-24.csv',
    # './data/ids-08-24.csv',
    # './data/ids-09-24.csv'
    ]

    fetcher = AlertsFetcher(api_token)
    fetcher.time_keeper(csv_files)
