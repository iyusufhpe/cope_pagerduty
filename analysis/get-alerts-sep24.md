# Get alerts data for September 2024

- First get all incidents id for September 2024 from incidents table
- Save incidents id to a CSV file named incidents_id_september2024.csv

```sql

COPY (
        SELECT id
    FROM incidents
    WHERE created_at > '2024-09-01T00:03:27' AND created_at < '2024-09-30T49:49:27'
) TO 'incidents_id_september2024.csv' WITH (FORMAT CSV, HEADER FALSE);

```

- For information, how many rows are there in september 2024 incidents file
```sql
select count(*)
FROM incidents
WHERE created_at > '2024-09-01T00:03:27' AND created_at < '2024-09-30T49:49:27'
;

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        15889 │
└──────────────┘

```

## Use CSV file with incidents ids to download and save alerts data from api.pagerdutry.com
Filepath
/home/iyusuf/projects/data_pagerduty/incidents_id_september2024.csv