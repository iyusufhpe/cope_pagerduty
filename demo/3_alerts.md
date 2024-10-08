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
        FROM incidents
        WHERE created_at > '2024-09-21T00:00:27' AND created_at < '2024-09-307T23:49:27';

┌───────────┐
│      5152 │
└───────────┘
```

### Run some query on a sample set of alerts that got fetched from 09-21-2024 to 09-30-2024

- Examine alerts using DuckDB
```sql
SELECT count(*) FROM read_json_auto('incident_ids_0921_0930_alerts.json', ignore_errors=true);

┌──────────────┐
│         9939 │
└──────────────┘

```

- Made a table out of json

```sql

 .tables
alerts_0921_0930      incidents             incidents_sep23sep24

```


- Show incident_ids_0921_0930_alerts RAW JSON
```sql
describe alerts_0921_0930;
```

- Get some nested JSON object using SQL

- Find text in description
```sql

-- Find rows where the word "error" appears in the description field using LIKE
SELECT *
FROM alerts_0921_0930
WHERE body.details.firing  LIKE '% runbook_url %';

SELECT count(*)
FROM alerts_0921_0930
WHERE body.details.firing  LIKE '% runbook_url %';
┌──────────────┐
│         1155 │
└──────────────┘

COPY (
    SELECT id, summary, service.id, incident.id
    FROM alerts_0921_0930
    WHERE body.details.firing  LIKE '% runbook_url %'
) TO 'demo1.csv' WITH (FORMAT CSV, HEADER FALSE);

-- cat demo1.csv

-- Let the same query grouped by service.id

SELECT 
    service.id AS service_id, 
    COUNT(*) AS alert_count
FROM 
    alerts_0921_0930
WHERE 
    body.details.firing LIKE '% runbook_url %'
GROUP BY 
    service.id
ORDER BY
    alert_count DESC
;

```
