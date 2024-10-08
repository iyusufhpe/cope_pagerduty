import pandas as pd
import json
import argparse

class JSONDataLoader:
    def __init__(self):
        self.df = None

    def load_json_to_dataframe(self, input_file):
        with open(input_file, 'r') as infile:
            data = json.load(infile)
        
        # Load JSON data into a DataFrame
        self.df = pd.json_normalize(data)
    
    def display_dataframe(self):
        if self.df is not None:
            print(self.df.head())
        else:
            print("DataFrame is empty. Load data first.")
    
    def save_to_csv(self, output_file):
        if self.df is not None:
            self.df.to_csv(output_file, index=False)
        else:
            print("DataFrame is empty. Load data first.")
    
    def read_csv(self, csv_file):
        self.df = pd.read_csv(csv_file)
        print(f"CSV data loaded from {csv_file}")

"""
Example Usage:
--------------
To load JSON data into a DataFrame, display it, and save it to a CSV file, you can run the script with the following commands:

1. Load JSON data into DataFrame:
   python3 alerts_cleanup_json_saveto_csv.py --input_file ./data/alerts_augsep24.json --output_file ./data/alerts_augsep24.csv 1

2. Display the DataFrame:
   python3 alerts_cleanup_json_saveto_csv.py --input_file ./data/alerts_augsep24.json --output_file ./data/alerts_augsep24.csv 1 2

3. Save the DataFrame to a CSV file:
   python3 alerts_cleanup_json_saveto_csv.py --input_file ./data/alerts_augsep24.json --output_file ./data/alerts_augsep24.csv 1 3

4. Load, Display, and Save:
   python3 alerts_cleanup_json_saveto_csv.py --input_file ./data/alerts_augsep24.json --output_file ./data/alerts_augsep24.csv 1 2 3

5. Read a CSV file:
   python3 alerts_cleanup_json_saveto_csv.py --input_file ./data/alerts_augsep24.csv --output_file ./data/alerts_augsep24.csv 4

Commands:
---------
1: Load JSON data into DataFrame
2: Display the DataFrame
3: Save the DataFrame to a CSV file
4: Read a CSV file
"""

def main():
    parser = argparse.ArgumentParser(description="Process JSON data and convert to DataFrame.")
    parser.add_argument('--input_file', type=str, help='Path to the input file (JSON or CSV)', required=True)
    parser.add_argument('--output_file', type=str, help='Path to the output CSV file', required=False)
    parser.add_argument('commands', type=str, nargs='+', help='Commands to execute (1: load, 2: display, 3: save, 4: read CSV)')

    args = parser.parse_args()

    # Create an instance of JSONDataLoader
    loader = JSONDataLoader()

    # Execute commands based on input
    for command in args.commands:
        if command == '1':
            loader.load_json_to_dataframe(args.input_file)
        elif command == '2':
            loader.display_dataframe()
        elif command == '3':
            if args.output_file:
                loader.save_to_csv(args.output_file)
            else:
                print("Output file path is required for command 3")
        elif command == '4':
            loader.read_csv(args.input_file)
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()