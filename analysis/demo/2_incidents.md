## Total number of incidents : 09-

```sql

-- Find start of created_at date
select min(created_at) from incidents;
┌─────────────────────┐
│ 2023-09-01T00:03:27 │
└─────────────────────┘

-- Max created_at
D select max(created_at) from incidents;
┌─────────────────────┐
│ 2024-09-30T22:59:48 │
└─────────────────────┘

-- Total number of rows in incidenst table
D select count(*) from incidents;
┌──────────────┐
│       262820 │
└──────────────┘

-- auto_resolved, How many were
SELECT COUNT(*) FROM incidents
WHERE auto_resolved == TRUE;
┌──────────────┐
│       124744 │
└──────────────┘

-- Percentage of auto_resolved? == 47%

-- Total number of teams
SELECT COUNT(DISTINCT(team_name)) FROM incidents;
┌───────────────────────────┐
│                        67 │
└───────────────────────────┘

-- Total number of services
SELECT COUNT(DISTINCT(service_name)) FROM incidents;
┌──────────────────────────────┐
│                          671 │
└──────────────────────────────┘

-- Total number of alerts by service name
SELECT service_name, COUNT(*) AS total_incidents
FROM incidents
GROUP BY service_name
HAVING COUNT(*) > 100
ORDER BY total_incidents DESC;
┌──────────────────────────────┐
│   ** Run @ DuckDB CLI **     │
└──────────────────────────────┘


-- Total number of alerts by service name
SELECT team_name, COUNT(*) AS total_incidents
FROM incidents
GROUP BY team_name
HAVING COUNT(*) > 100
ORDER BY total_incidents DESC;
┌──────────────────────────────┐
│   ** Run @ DuckDB CLI **     │
└──────────────────────────────┘

-- Total incidents count grouped by team_name and service_name
SELECT team_name, service_name, COUNT(*) AS total_incidents
FROM incidents
WHERE auto_resolved = true
GROUP BY team_name, service_name
HAVING COUNT(*) > 100
ORDER BY total_incidents DESC;



-- Find the most common top 25 words in the description field when auto_resolved is true, excluding common words

WITH tokenized AS (
    SELECT
        UNNEST(STRING_SPLIT(LOWER(description), ' ')) AS word
    FROM
        incidents
    WHERE
        auto_resolved = true
)
SELECT
    word,
    COUNT(*) AS word_count
FROM
    tokenized
WHERE
    word NOT IN ('should', '(true', 'use', 'be','multiple', 'warning', 'enabled')
GROUP BY
    word
ORDER BY
    word_count DESC
LIMIT 25;

┌──────────────────────┬────────────┐
│         word         │ word_count │
│       varchar        │   int64    │
├──────────────────────┼────────────┤
│ monitoring/k8s       │      44821 │
│ us-west-2            │      44819 │
│ hpe-hcss             │      44286 │
│ [firing:1]           │      37217 │
│ not                  │      34046 │
│ warning)             │      32697 │
│ integration          │      29323 │
│ ec2                  │      24162 │
│ instances            │      22284 │
│ enis                 │      20689 │
│ oberon               │      18688 │
│ kube-state-metrics   │      15656 │
│ kube-rbac-proxy-main │      15196 │
│ production           │      11785 │
│ aws                  │      11415 │
│ kubehpamaxedout      │      11369 │
│ (oberon              │      10635 │
│ keys                 │      10228 │
│ kms                  │       9810 │
│ agena                │       9687 │
│ name:                │       8911 │
│ deleted              │       8675 │
│ unintentionally      │       8675 │
│ [firing:2]           │       7398 │
│ domain               │       7124 │
├──────────────────────┴────────────┤
│ 25 rows                 2 columns │
└───────────────────────────────────┘



-- What are all the values of "priority_id"
select distinct(priority_name) from incidents;

┌───────────────┐
│ priority_name │
│    varchar    │
├───────────────┤
│ P2            │
│               │
│ P5            │
│ P1            │
│ P4            │
│ P3            │
└───────────────┘


-- Find total count of P1
select count(priority_name) from incidents
where priority_name ILIKE 'P1'
and
auto_resolved==TRUE;


-- Find distinct status values
 select distinct(status) from incidents;
┌──────────────┐
│    status    │
│   varchar    │
├──────────────┤
│ resolved     │
│ acknowledged │
│ triggered    │
└──────────────┘


-- Find the percentage of each status in the incidents table
SELECT
      status,
      COUNT(*) * 100.0 / (SELECT COUNT(*) FROM incidents) AS percentage
  FROM
      incidents
  GROUP BY
      status;
┌──────────────┬────────────────────┐
│    status    │     percentage     │
│   varchar    │       double       │
├──────────────┼────────────────────┤
│ resolved     │  93.79423179362301 │
│ triggered    │ 4.8063313294269845 │
│ acknowledged │ 1.3994368769500038 │
└──────────────┴────────────────────┘

```


