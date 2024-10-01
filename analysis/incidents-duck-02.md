# Incidents

```
D describe incidents2;
┌───────────────────────┬──────────────┬─────────┬─────────┬─────────┬─────────┐
│      column_name      │ column_type  │  null   │   key   │ default │  extra  │
│        varchar        │   varchar    │ varchar │ varchar │ varchar │ varchar │
├───────────────────────┼──────────────┼─────────┼─────────┼─────────┼─────────┤
│ id                    │ VARCHAR      │ YES     │         │         │         │
│ incident_number       │ BIGINT       │ YES     │         │         │         │
│ resolved_at           │ TIMESTAMP_NS │ YES     │         │         │         │
│ service_id            │ VARCHAR      │ YES     │         │         │         │
│ created_at            │ TIMESTAMP_NS │ YES     │         │         │         │
│ total_notifications   │ BIGINT       │ YES     │         │         │         │
│ resolved_by_user_id   │ VARCHAR      │ YES     │         │         │         │
│ resolved_by_user_name │ VARCHAR      │ YES     │         │         │         │
│ acknowledged_user_ids │ VARCHAR[]    │ YES     │         │         │         │
│ team_id               │ VARCHAR      │ YES     │         │         │         │
│ team_name             │ VARCHAR      │ YES     │         │         │         │
│ seconds_to_first_ack  │ DOUBLE       │ YES     │         │         │         │
│ seconds_to_engage     │ DOUBLE       │ YES     │         │         │         │
│ priority_id           │ VARCHAR      │ YES     │         │         │         │
│ status                │ VARCHAR      │ YES     │         │         │         │
│ auto_resolved         │ BOOLEAN      │ YES     │         │         │         │
│ description           │ VARCHAR      │ YES     │         │         │         │
├───────────────────────┴──────────────┴─────────┴─────────┴─────────┴─────────┤
│ 17 rows                                                            6 columns │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Find total number of incidents
```sql
D select count(*) from incidents2;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       259639 │
└──────────────┘
```

### Max and Min created_at dates
```SQL
D SELECT MAX(created_at) as max_date from incidents2;
┌─────────────────────┐
│      max_date       │
│    timestamp_ns     │
├─────────────────────┤
│ 2024-09-26 10:52:15 │
└─────────────────────┘
D SELECT MIN(created_at) as max_date from incidents2;
┌─────────────────────┐
│      max_date       │
│    timestamp_ns     │
├─────────────────────┤
│ 2023-09-01 00:03:27 │
└─────────────────────┘
```


## Incidents greater then August 1st 2024
```sql
select count(*) from incidents2;
select count(*) from incidents2 where created_at > '2024-08-01 00:00:00';

D select count(*) from incidents2;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       259639 │
└──────────────┘
D
D select count(*) from incidents2 where created_at > '2024-08-01 00:00:00';
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        26940 │
└──────────────┘
``` 


## Create a table with just incident id for August 2024

```sql
CREATE TABLE AUG24_INCIDENTS AS
SELECT ID FROM INCIDENTS2 
WHERE CREATED_AT > '2024-08-01 00:00:00' 
AND 
CREATED_AT < '2024-09-01 00:00:00';
```

-- Let us output the coount of 

<DataTable data={query_name}>
    <Column id=column_name fmt=usd/>
    <Column id=column_name contentType=link align=center/>
</DataTable>

