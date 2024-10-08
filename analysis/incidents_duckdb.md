# Differentiating Incidents in PagerDuty Data

The PagerDuty data received via Power BI service must distinguish between on-premises and non-on-premises incidents. This is done by examining the incident descriptions for domain names:

1. On-premises incidents:
   - If the incident description contains a domain name, the domain name (representing the customer) is extracted and added to a field labeled `customer_name`.
   - These incidents will have a specific customer name corresponding to the domain found in the description.
2. Non-on-premises incidents:
   - If no domain name is present in the incident description, the incidents are marked with the `customer_name` field set to "others" by default.


## Create a duckdb table for incidents between 09-01-2023 09-30-2024

- I have the following json files for incidents.
incidents_2023-09-01_to_2023-12-31.json
incidents_2024-01-01_to_2024-06-30.json
incidents_2024-07-01_to_2024-07-31.json
incidents_2024-08-01_to_2024-08-31.json
incidents_2024-09-01_to_2024-09-30.json
incidents_2024-09-01_to_2024-12-31.json

### Create the table

```sql
-- Create the table and load data from the first JSON file
CREATE TABLE incidents_sep23sep24 AS
SELECT * FROM read_json_auto('incidents_2023-09-01_to_2023-12-31.json');

-- Append data from additional JSON files
INSERT INTO incidents_sep23sep24
SELECT * FROM read_json_auto('incidents_2024-01-01_to_2024-06-30.json');

INSERT INTO incidents_sep23sep24
SELECT * FROM read_json_auto('incidents_2024-07-01_to_2024-07-31.json');

INSERT INTO incidents_sep23sep24
SELECT * FROM read_json_auto('incidents_2024-08-01_to_2024-08-31.json');

INSERT INTO incidents_sep23sep24
SELECT * FROM read_json_auto('incidents_2024-09-01_to_2024-09-30.json');

-- doesn't work as more columns has been added to new incidents data.
INSERT INTO incidents_sep23sep24
SELECT * FROM read_json_auto('./data/incidents_2024-10-01_to_2024-10-07.json');
                              
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

### Export describe's output to a file
```sql
COPY (
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'incidents_sep23sep24'
) TO 'schema_info.txt' WITH (FORMAT CSV, HEADER TRUE, DELIMITER ' ');
```

### Use schema info to create a table.
## Create the table with explicit schema

```sql
-- Open DuckDB CLI
duckdb your_database.db

-- Create the table with explicit schema
CREATE TABLE incidents_sep23sep24 (
    id VARCHAR,
    resolved_at VARCHAR,
    acknowledged_user_names VARCHAR[],
    assigned_user_ids VARCHAR[],
    service_id VARCHAR,
    urgency VARCHAR,
    created_at VARCHAR,
    acknowledgement_count BIGINT,
    priority_order DOUBLE,
    escalation_count BIGINT,
    user_defined_effort_seconds JSON,
    manual_escalation_count BIGINT,
    assignment_count BIGINT,
    total_notifications BIGINT,
    resolved_by_user_id VARCHAR,
    engaged_seconds BIGINT,
    assigned_user_names VARCHAR[],
    joined_user_ids VARCHAR[],
    resolved_by_user_name VARCHAR,
    team_id VARCHAR,
    seconds_to_first_ack DOUBLE,
    team_name VARCHAR,
    total_interruptions BIGINT,
    business_hour_interruptions BIGINT,
    seconds_to_engage DOUBLE,
    priority_id VARCHAR,
    joined_user_names VARCHAR[],
    off_hour_interruptions BIGINT,
    snoozed_seconds BIGINT,
    status VARCHAR,
    auto_resolved BOOLEAN,
    updated_at VARCHAR,
    description VARCHAR,
    engaged_user_count BIGINT,
    active_user_count BIGINT,
    service_name VARCHAR,
    escalation_policy_name VARCHAR,
    sleep_hour_interruptions BIGINT,
    escalation_policy_id VARCHAR,
    incident_number BIGINT,
    major BOOLEAN,
    seconds_to_mobilize DOUBLE,
    timeout_escalation_count BIGINT,
    priority_name VARCHAR,
    reassignment_count BIGINT,
    acknowledged_user_ids VARCHAR[],
    seconds_to_resolve BIGINT
);
```

### Insert data to newly created table from JSON files
```sql
-- Insert data from the first JSON file
INSERT INTO incidents_sep23sep24
SELECT 
    id,
    resolved_at,
    acknowledged_user_names,
    assigned_user_ids,
    service_id,
    urgency,
    created_at,
    acknowledgement_count,
    priority_order,
    escalation_count,
    user_defined_effort_seconds,
    manual_escalation_count,
    assignment_count,
    total_notifications,
    resolved_by_user_id,
    engaged_seconds,
    assigned_user_names,
    joined_user_ids,
    resolved_by_user_name,
    team_id,
    seconds_to_first_ack,
    team_name,
    total_interruptions,
    business_hour_interruptions,
    seconds_to_engage,
    priority_id,
    joined_user_names,
    off_hour_interruptions,
    snoozed_seconds,
    status,
    auto_resolved,
    updated_at,
    description,
    engaged_user_count,
    active_user_count,
    service_name,
    escalation_policy_name,
    sleep_hour_interruptions,
    escalation_policy_id,
    incident_number,
    major,
    seconds_to_mobilize,
    timeout_escalation_count,
    priority_name,
    reassignment_count,
    acknowledged_user_ids,
    seconds_to_resolve
FROM read_json_auto('incidents_2023-09-01_to_2023-12-31.json');
```


### Get row count
```bash
D select count(*) from incidents_sep23sep24;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       262820 │
└──────────────┘
```



### Create a view as a permanent alias for the table

```sql
-- Create a view as a permanent alias for the table
CREATE VIEW incidents AS
SELECT *
FROM incidents_sep23sep24;
```

### Using the view

```sql
SELECT *
FROM incidents
WHERE status = 'resolved';
```

### Get max and min created incidents date
```sql
D SELECT MIN(created_at) AS oldest_created_at FROM incidents;
┌─────────────────────┐
│  oldest_created_at  │
│       varchar       │
├─────────────────────┤
│ 2023-09-01T00:03:27 │
└─────────────────────┘
D SELECT MAX(created_at) AS recent_created_at FROM incidents;
┌─────────────────────┐
│  recent_created_at  │
│       varchar       │
├─────────────────────┤
│ 2024-09-30T22:59:48 │
└─────────────────────┘
```

## Analysis

### Search count of rows where the description field contains "Domain Name" [case sensitive]
```sql
SELECT COUNT(*) FROM incidents
WHERE description LIKE '%Domain Name%'
;

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        40254 │
└──────────────┘
```

### Search count of rows where the description field contains "Domain Name" [case in-sensitive]
```sql
SELECT COUNT(*) FROM incidents
WHERE description ILIKE '%Domain Name%'
;

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        40324 │
└──────────────┘
```




### Calculate the percentage of rows with "Domain Name" in the description field
```sql
SELECT
     (COUNT(*) FILTER (WHERE description ILIKE '%Domain Name%') * 100.0 / COUNT(*)) AS percentage_with_domain_name
FROM incidents;
┌─────────────────────────────┐
│ percentage_with_domain_name │
│           double            │
├─────────────────────────────┤
│          15.342820181112549 │
└─────────────────────────────┘
```

## Time related
### How many incidents is Auto Resolved

```sql
select count(*) from incidents
where auto_resolved is TRUE

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       124744 │
└──────────────┘
;


### Priority analysis

```SQL
select count(*) from incidents where priority_name LIKE 'P1';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        11563 │
└──────────────┘
select count(*) from incidents where priority_name LIKE 'P2';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         7669 │
└──────────────┘
select count(*) from incidents where priority_name LIKE 'P3';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        46652 │
└──────────────┘
select count(*) from incidents where priority_name LIKE 'P4';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        39911 │
└──────────────┘
D select count(*) from incidents where priority_name LIKE '';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            0 │
└──────────────┘
D select count(*) from incidents where priority_name IS NULL;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       157013 │
└──────────────┘
```


## Teams and Services
### How many teams are contributing to PagerDuty
```sql
select distinct(team_name) from incidents;

├────────────────────────────┤
│     68 rows (40 shown)     │
└────────────────────────────┘
```

### How many services are contributing to PagerDuty Incidents
```sql
 select distinct(service_name) from incidents;

├───────────────────────────────────────────────┤
│              671 rows (40 shown)              │
└───────────────────────────────────────────────┘
```

### Find On-Prem Services
```sql
SELECT distinct(service_name) FROM incidents
WHERE description ILIKE '%Domain Name%'
;

├──────────────────────────────────────────────────────┤
│                       41 rows                        │
└──────────────────────────────────────────────────────┘
```

### Find Team Names for onprem.
```sql
SELECT distinct(team_name) FROM incidents
WHERE description ILIKE '%Domain Name%'
;
```