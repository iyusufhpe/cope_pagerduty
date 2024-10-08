## Get alerts data

### Generate incidents IDs

- First get incidents id 
- Save incidents id to a CSV file named incidents_id_september2024.csv

```sql
COPY (
        SELECT id
    FROM incidents
    WHERE created_at > '2024-09-21T00:00:27' AND created_at < '2024-09-30T23:49:27'
) TO 'incident_ids_0921_0930.csv' WITH (FORMAT CSV, HEADER FALSE);
```

###

###
- Check how many incidents id we have
```sql
    SELECT count(id)
        FROM incidents_0701_1007
        WHERE created_at > '2024-10-01T00:00:27' AND created_at < '2024-10-07T23:49:27';
    ┌───────────┐
    │ count(id) │
    │   int64   │
    ├───────────┤
    │      4408 │
    └───────────┘
```

### Run some query on a sample set of alerts that got fetched using 100 incident ids.
- We will first try with 100 incidents ids to fetch alerts for
- Run Python to fetch alerts 
- Alerts are generated and saved in **incidents_ids_100_alerts.json**
- Now run DuckDB SQL to investigate how many top level JSON objects are present
```sql
D SELECT count(*) FROM read_json_auto('incidents_ids_100_alerts.json', ignore_errors=true);
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│          100 │
└──────────────┘
```

- We got 100 alerts from 100 incidents ids. 
- **TODO** I need to investigate why some time number of alerts sometime does not equal to number of incidents ids. I've noticed this behavior in the past.

### Fetch alerts for 4408 incidents ids and compare number of alerts that we will get.
- Run "alerts_fetch-data.py
    - Output: Saved remaining alerts data to ./data/incidents_0701_1007_ids_alerts.json
```bash

- Examine alerts using DuckDB
```sql
D SELECT count(*) FROM read_json_auto('incidents_0701_1007_ids_alerts.json', ignore_errors=true);

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         1184 │
└──────────────┘
```

### I am getting greedy now :) 
- Let us fetch alerts from **September 2024**

```sql
COPY (
    SELECT id
    FROM incidents_0701_1007
    WHERE created_at > '2024-09-01T00:00:27' AND created_at < '2024-09-30T23:49:27'
) TO 'incidents_0901_0930_ids.csv' WITH (FORMAT CSV, HEADER FALSE);
```

**Bug Fix** There was a bug in my python code. File appender was not appending.