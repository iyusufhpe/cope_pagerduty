## Create a table

```sql
create table incidents_tbl AS 
SELECT * FROM read_parquet('combined_incidents.parquet');

select * from incidents_tbl
```

# Column names


```sql
COPY (
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'incidents_tbl'
) TO 'column_names.csv' WITH (FORMAT CSV, HEADER TRUE);



    column_name
    id
    resolved_at
    acknowledged_user_names
    assigned_user_ids
    service_id
    urgency
    created_at
    acknowledgement_count
    priority_order
    escalation_count
    user_defined_effort_seconds
    manual_escalation_count
    assignment_count
    total_notifications
    resolved_by_user_id
    engaged_seconds
    assigned_user_names
    joined_user_ids
    resolved_by_user_name
    team_id
    seconds_to_first_ack
    team_name
    total_interruptions
    business_hour_interruptions
    seconds_to_engage
    priority_id
    joined_user_names
    off_hour_interruptions
    snoozed_seconds
    status
    auto_resolved
    updated_at
    description
    engaged_user_count
    active_user_count
    service_name
    escalation_policy_name
    sleep_hour_interruptions
    escalation_policy_id
    incident_number
    major
    seconds_to_mobilize
    timeout_escalation_count
    priority_name
    reassignment_count
    acknowledged_user_ids
    seconds_to_resolve
```


## find earliest created_at date

```sql
D SELECT MIN(created_at) AS oldest_created_at FROM incidents_tbl;
┌─────────────────────┐
│  oldest_created_at  │
│    timestamp_ns     │
├─────────────────────┤
│ 2023-09-01 00:03:27 │
└─────────────────────┘
```


## Create a table with subset of main table with limited columns.

