```sql

WITH json_data AS (
    SELECT json_each.value AS obj
    FROM read_json_objects('alerts_augsep24.json') AS json_each
)
SELECT 
    obj->>'id' AS id,
    obj->>'summary' AS summary,
    obj->>'created_at' AS created_at,
    obj->>'status' AS status,
    obj->>'resolved_at' AS resolved_at,
    obj->'service'->>'id' AS service_id,
    obj->>'severity' AS severity,
    obj->'incident'->>'id' AS incident_id,
    obj->'body'->'details'->>'Description' AS description,
    obj->'body'->'details'->>'Samples' AS samples,
    COALESCE(obj->'body'->'details'->>'firing', 'N/A') AS firing
FROM json_data;

```