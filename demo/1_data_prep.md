# Demo DuckDB for PagerDuty

## Get Incidents Data
- Used python to download PagerDuty data from api.pagerduty.com
- Saved data as JSON file

## Load Data to DuckDB
- I have the following json files for incidents.
- - ~ 450 mb in size
incidents_2023-09-01_to_2023-12-31.json
incidents_2024-01-01_to_2024-06-30.json
incidents_2024-07-01_to_2024-07-31.json
incidents_2024-08-01_to_2024-08-31.json
incidents_2024-09-01_to_2024-09-30.json

### Create a table from JSON
```sql
    -- Create the table and load data from the first JSON file
    CREATE TABLE incidents_sep23sep24 AS
    SELECT * FROM read_json_auto('incidents_2023-09-01_to_2023-12-31.json');

    -- Append data from additional JSON files
    INSERT INTO incidents_sep23sep24    SELECT * FROM read_json_auto('incidents_2024-01-01_to_2024-06-30.json');
    INSERT INTO incidents_sep23sep24    SELECT * FROM read_json_auto('incidents_2024-07-01_to_2024-07-31.json');
    INSERT INTO incidents_sep23sep24    SELECT * FROM read_json_auto('incidents_2024-08-01_to_2024-08-31.json');
    INSERT INTO incidents_sep23sep24    SELECT * FROM read_json_auto('incidents_2024-09-01_to_2024-09-30.json');
```

### Get the full list of column names

```sql
    -- Export the column names to a CSV file
    COPY (
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'incidents_sep23sep24'
    ) TO 'column_names.csv' WITH (FORMAT CSV, HEADER TRUE);
```

### Create a view as a permanent alias for the table

```sql
    -- Create a view as a permanent alias for the table
    CREATE VIEW incidents AS
    SELECT *
    FROM incidents_sep23sep24;
```

### Investigate some basic stats from incidents
```sql

    -- Count how many rows in that table
    select count(*) from incidents;

    ┌──────────────┐
    │ count_star() │
    │    int64     │
    ├──────────────┤
    │       262820 │
    └──────────────┘


-- Investigate start date and end date from created_at field
select min(created_at) from incidents;
┌─────────────────────┐
│ 2023-09-01T00:03:27 │
└─────────────────────┘

SELECT MAX(created_at) from incidents;
┌─────────────────────┐
│ 2024-09-30T22:59:48 │
└─────────────────────┘


-- Total rows (incidents ?? )
SELECT COUNT(*) 
FROM incidents
WHERE created_at >= '2023-09-01T00:00:23' AND created_at < '2024-09-30T23:59:23'
;

┌──────────────┐
│       262820 │
└──────────────┘
```

## Get alerts data

- First get incidents id 
- Save incidents id to a CSV file named incidents_id_september2024.csv

```sql
COPY (
        SELECT id
    FROM incidents
    WHERE created_at > '2024-09-21T00:00:27' AND created_at < '2024-09-30T23:49:27'
) TO 'incident_ids_0921_0930.csv' WITH (FORMAT CSV, HEADER FALSE);
```

- Check how many incidents id we have
```sql
    D SELECT count(id)
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