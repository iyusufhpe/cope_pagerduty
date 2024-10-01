

- Start DuckDB
```bash
➜  duckdb incidents_aug24
v1.1.1 af39bd0dcf
Enter ".help" for usage hints.
D create table incidents_aug23 as select * from "incidents_2024-09-01_to_2024-09-30.json";
```

- Import August incidents PagerDuty JSON file as a table
```bash
D create table incidents_aug23 as select * from "incidents_2024-09-01_to_2024-09-30.json";
```

- **Note:** I've just noticed that I made a mistake with the table name. Instead of 24 I used 23 to name it incidents_aug23

- Describe table incidents_aug23 and save it as a text

```bash
-- Redirect output to a text file
.output describe_output.txt

-- Execute the DESCRIBE command
DESCRIBE incidents_aug23;

-- Reset output to the terminal
.output stdout
```

- View the content of table schema

```text
┌─────────────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│         column_name         │ column_type │  null   │   key   │ default │  extra  │
│           varchar           │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ id                          │ VARCHAR     │ YES     │         │         │         │
│ snoozed_seconds             │ BIGINT      │ YES     │         │         │         │
│ seconds_to_resolve          │ DOUBLE      │ YES     │         │         │         │
│ acknowledgement_count       │ BIGINT      │ YES     │         │         │         │
│ updated_at                  │ VARCHAR     │ YES     │         │         │         │
│ manual_escalation_count     │ BIGINT      │ YES     │         │         │         │
│ timeout_escalation_count    │ BIGINT      │ YES     │         │         │         │
│ seconds_to_mobilize         │ DOUBLE      │ YES     │         │         │         │
│ business_hour_interruptions │ BIGINT      │ YES     │         │         │         │
│ incident_number             │ BIGINT      │ YES     │         │         │         │
│ escalation_policy_id        │ VARCHAR     │ YES     │         │         │         │
│ acknowledged_user_ids       │ VARCHAR[]   │ YES     │         │         │         │
│ total_notifications         │ BIGINT      │ YES     │         │         │         │
│ total_interruptions         │ BIGINT      │ YES     │         │         │         │
│ joined_user_names           │ VARCHAR[]   │ YES     │         │         │         │
│ auto_resolved               │ BOOLEAN     │ YES     │         │         │         │
│ acknowledged_user_names     │ VARCHAR[]   │ YES     │         │         │         │
│ service_name                │ VARCHAR     │ YES     │         │         │         │
│ joined_user_ids             │ VARCHAR[]   │ YES     │         │         │         │
│ active_user_count           │ BIGINT      │ YES     │         │         │         │
│ escalation_count            │ BIGINT      │ YES     │         │         │         │
│ team_name                   │ VARCHAR     │ YES     │         │         │         │
│ priority_order              │ DOUBLE      │ YES     │         │         │         │
│ priority_name               │ VARCHAR     │ YES     │         │         │         │
│ reassignment_count          │ BIGINT      │ YES     │         │         │         │
│ team_id                     │ VARCHAR     │ YES     │         │         │         │
│ urgency                     │ VARCHAR     │ YES     │         │         │         │
│ off_hour_interruptions      │ BIGINT      │ YES     │         │         │         │
│ engaged_seconds             │ BIGINT      │ YES     │         │         │         │
│ status                      │ VARCHAR     │ YES     │         │         │         │
│ service_id                  │ VARCHAR     │ YES     │         │         │         │
│ description                 │ VARCHAR     │ YES     │         │         │         │
│ resolved_at                 │ VARCHAR     │ YES     │         │         │         │
│ assignment_count            │ BIGINT      │ YES     │         │         │         │
│ assigned_user_ids           │ VARCHAR[]   │ YES     │         │         │         │
│ resolved_by_user_name       │ VARCHAR     │ YES     │         │         │         │
│ resolved_by_user_id         │ VARCHAR     │ YES     │         │         │         │
│ user_defined_effort_seconds │ JSON        │ YES     │         │         │         │
│ major                       │ BOOLEAN     │ YES     │         │         │         │
│ seconds_to_first_ack        │ DOUBLE      │ YES     │         │         │         │
│ assigned_user_names         │ VARCHAR[]   │ YES     │         │         │         │
│ seconds_to_engage           │ DOUBLE      │ YES     │         │         │         │
│ engaged_user_count          │ BIGINT      │ YES     │         │         │         │
│ sleep_hour_interruptions    │ BIGINT      │ YES     │         │         │         │
│ priority_id                 │ VARCHAR     │ YES     │         │         │         │
│ escalation_policy_name      │ VARCHAR     │ YES     │         │         │         │
│ created_at                  │ VARCHAR     │ YES     │         │         │         │
├─────────────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 47 rows                                                                 6 columns │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- Create a new table with limited columns
- I've selected to following columns. Consult with <?> to shrink or expand the list of columns for a new incidents table.

```text
id
incident_number
description
status
auto_resolved
service_name
team_name
priority_name
team_id
urgency
service_id
major
priority_id
created_at
```

- Create the table

```sql 
CREATE TABLE incidents_limited AS
SELECT 
    id,
    incident_number,
    description,
    status,
    auto_resolved,
    service_name,
    team_name,
    priority_name,
    team_id,
    urgency,
    service_id,
    major,
    priority_id,
    created_at
FROM incidents_aug23;
```

- Find total number of incidents (aka total number of rows)

```bash
    D select count(*) from incidents_limited;
    ┌──────────────┐
    │ count_star() │
    │    int64     │
    ├──────────────┤
    │        15889 │
    └──────────────┘
```

- Try to count only rows which has "Readiness probe failed" in description field

```sql
SELECT count(*)
FROM incidents_limited
WHERE description LIKE '%Readiness probe failed%';

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│          298 │
└──────────────┘
```

- Output the table with rows that have readiness probe failed in description field.

```sql
    -- Set output to CSV file
    .output readiness_probe_failed_aug2024.csv

    -- Execute the SELECT statement
    SELECT * FROM incidents_limited WHERE description LIKE '%Readiness probe failed%';

    -- Reset output to the terminal
    .output stdout
```

- Examine the content 


