on prem is 15% fo all incidents.

## Total number of incidents between September 1st 2023 and September 30th 2024
```sql
select count(*) from incidents_sep23sep24;

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│       262820 │
└──────────────┘
```


##  Select count of rows where the description field contains "Domain Name" (case-insensitive)
```sql
SELECT COUNT(*)
FROM incidents_sep23sep24
WHERE description ILIKE '%Domain Name%';

┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        40324 │
└──────────────┘
```

## What is the percentage of rows that have "Domain Name" in description field

```sql
SELECT 
    (COUNT(*) FILTER (WHERE description ILIKE '%Domain Name%') * 100.0 / COUNT(*)) AS percentage_with_domain_name
FROM incidents_sep23sep24;

┌─────────────────────────────┐
│ percentage_with_domain_name │
│           double            │
├─────────────────────────────┤
│          15.342820181112549 │
└─────────────────────────────┘
```

## Find the most frequently used top 50 word in the description field

```sql
-- Open DuckDB CLI
duckdb your_database.db

-- Find the most frequently used word in the description field
WITH words AS (
    SELECT UNNEST(STRING_SPLIT(description, ' ')) AS word
    FROM incidents
),
word_counts AS (
    SELECT word, COUNT(*) AS count
    FROM words
    GROUP BY word
)
SELECT word, count
FROM word_counts
ORDER BY count DESC
LIMIT 50;

```

## How many distinct policy name we have
```sql
D select count(distinct(escalation_policy_name)) from incidents;
┌────────────────────────────────────────┐
│ count(DISTINCT escalation_policy_name) │
│                 int64                  │
├────────────────────────────────────────┤
│                                    190 │
└────────────────────────────────────────┘
```

