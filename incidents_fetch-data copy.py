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

class IncidentFetcher:
    def __init__(self, api_token):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token token={self.api_token}',
            'Content-Type': 'application/json'
        })

    def fetch_incidents(self, created_at_start, created_at_end, starting_after=None):
        url = 'https://api.pagerduty.com/incidents'
        params = {
            'since': created_at_start,
            'until': created_at_end,
            'limit': 100,
            'offset': 0,
            'total': True
        }
        if starting_after:
            params['starting_after'] = starting_after

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def save_to_files(self, df, created_at_start, created_at_end):
        filename = f'incidents_{created_at_start}_{created_at_end}.csv'
        df.to_csv(filename, index=False)
        logging.info(f'Saved incidents to {filename}')

    def get_date_range(self, month=None, year=None, last_n_months=None, start_date=None, end_date=None):
        if last_n_months:
            end_date = datetime.now()
            start_date = end_date - relativedelta(months=last_n_months)
        elif month and year:
            start_date = datetime(year, month, 1)
            end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        elif start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            raise ValueError("Invalid date range parameters")

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def reorder_columns(self, df, column_order):
        return df[column_order]

    def main(self):
        parser = argparse.ArgumentParser(description='Fetch PagerDuty incidents.')
        parser.add_argument('--month', type=int, help='Month for which to fetch incidents')
        parser.add_argument('--year', type=int, help='Year for which to fetch incidents')
        parser.add_argument('--last_n_months', type=int, help='Fetch incidents for the last N months')
        parser.add_argument('--start_date', type=str, help='Start date for fetching incidents (YYYY-MM-DD)')
        parser.add_argument('--end_date', type=str, help='End date for fetching incidents (YYYY-MM-DD)')
        args = parser.parse_args()

        created_at_start, created_at_end = self.get_date_range(
            month=args.month,
            year=args.year,
            last_n_months=args.last_n_months,
            start_date=args.start_date,
            end_date=args.end_date
        )

        incidents = []
        starting_after = None
        while True:
            response = self.fetch_incidents(created_at_start, created_at_end, starting_after)
            incidents.extend(response['incidents'])
            if 'more' in response and response['more']:
                starting_after = response['incidents'][-1]['id']
            else:
                break

        df = pd.DataFrame(incidents)
        self.save_to_files(df, created_at_start, created_at_end)

if __name__ == "__main__":
    fetcher = IncidentFetcher(api_token)
    fetcher.main()