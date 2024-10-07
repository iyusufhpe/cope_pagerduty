'''
This module fetches PagerDuty incidents data for a given month, year, or date range.
It paginates through the results and saves the combined data to JSON and CSV files.

Usage:  python main.py --month 1 --year 2024
        python main.py --last_n_months 3
        python main.py --start_date 04/23/2024 --end_date 04/24/2024
        
Note: The script respects the rate limit by waiting for 5 seconds between each request.

TODO: Schedule the script to run daily using a cron job. Make sure to use valid data time inputs.
TODO: Make this module a part of a larger ETL pipeline to fetch, transform, and load data into a database.

TODO: Add error handling for invalid date inputs.
TODO: Add a function to validate the date format.
TODO: Add a function to handle the response status code.
TODO: Add a function to reorder columns in the DataFrame.

'''
import requests
import json
import time
import pandas as pd
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import argparse
from token_getter import api_token

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_incidents(created_at_start, created_at_end, starting_after=None):
    url = "https://api.pagerduty.com/analytics/raw/incidents"
    headers = {
        'Authorization': f"Token token={api_token}",
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "filters": {
            "created_at_start": created_at_start,
            "created_at_end": created_at_end
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

def save_to_files(df, created_at_start, created_at_end):
    start_date_str = created_at_start.split('T')[0]
    end_date_str = created_at_end.split('T')[0]
    json_filename = f'incidents_{start_date_str}_to_{end_date_str}.json'
    csv_filename = f'incidents_{start_date_str}_to_{end_date_str}.csv'
    df.to_json(json_filename, orient='records', indent=2)
    df.to_csv(csv_filename, index=False)

def get_date_range(month=None, year=None, last_n_months=None, start_date=None, end_date=None):
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y') + timedelta(days=1) - timedelta(seconds=1)
    elif last_n_months:
        end_date = datetime.now()
        start_date = end_date - relativedelta(months=last_n_months)
    else:
        start_date = datetime(year, month, 1)
        end_date = start_date + relativedelta(months=1) - timedelta(seconds=1)
    return start_date.isoformat(), end_date.isoformat()

def main():
    parser = argparse.ArgumentParser(description='Fetch PagerDuty incidents data.')
    parser.add_argument('--month', type=int, help='Month for which to fetch data (1-12)')
    parser.add_argument('--year', type=int, help='Year for which to fetch data')
    parser.add_argument('--last_n_months', type=int, help='Fetch data for the last N months')
    parser.add_argument('--start_date', type=str, help='Start date in MM/DD/YYYY format')
    parser.add_argument('--end_date', type=str, help='End date in MM/DD/YYYY format')
    args = parser.parse_args()

    created_at_start, created_at_end = get_date_range(
        month=args.month,
        year=args.year,
        last_n_months=args.last_n_months,
        start_date=args.start_date,
        end_date=args.end_date
    )

    # Initialize an empty DataFrame to store all data elements
    all_data_df = pd.DataFrame()

    # Initial fetch
    data = fetch_incidents(created_at_start, created_at_end)
    if data:
        all_data_df = pd.DataFrame(data['data'])

    # Pagination loop
    while data and data.get('more'):
        starting_after = data['last']
        data = fetch_incidents(created_at_start, created_at_end, starting_after)
        if data:
            new_data_df = pd.DataFrame(data['data'])
            all_data_df = pd.concat([all_data_df, new_data_df], ignore_index=True)
        
        # Delay to respect rate limit
        time.sleep(5.0)  # Adjust as needed

    # Reorder columns to place "id" as the first column
    if 'id' in all_data_df.columns:
        columns = ['id'] + [col for col in all_data_df.columns if col != 'id']
        all_data_df = all_data_df[columns]

    # Save the combined DataFrame to JSON and CSV files
    save_to_files(all_data_df, created_at_start, created_at_end)

    logging.info(f"Total incidents fetched: {len(all_data_df)}")



'''
    Usage:
    python incidents-fetcc.py --month 1 --year 2024  # Fetch data for January 2024
    python incidents-fetcc.py --last_n_months 3  # Fetch data for the last three months from today
    python incidents-fetcc.py --start_date 09/01/2024 --end_date 09/30/2024  # Fetch data for a specific date range
'''
if __name__ == "__main__":
    main()