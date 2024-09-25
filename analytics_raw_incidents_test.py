import requests
import json
from token_getter import api_token

url = "https://api.pagerduty.com/analytics/raw/incidents"

headers = {
  'Authorization': f"Token token={api_token}",
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

payload = json.dumps({
  "filters": {
    "created_at_start": "2024-09-02T00:00:00-00:01"
  },
  "limit": 10,
  "order": "asc",
  "order_by": "created_at",
  "time_zone": "Etc/UTC"
})

try:
  response = requests.request("POST", url, headers=headers, verify=False, data=payload)
except requests.exceptions.RequestException as e:
  print(f"Error: {e}")
  
if response.status_code == 200:
  with open('response_output.txt', 'a') as file:
    file.write(response.text + '\n')
else:
  print(f"Status code: {response.status_code}")