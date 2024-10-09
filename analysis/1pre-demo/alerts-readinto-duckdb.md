```sql

CREATE TABLE alerts_data AS
WITH json_data AS (
    SELECT * 
    FROM read_json_objects('alerts_augsep24_cleaned.json')
)
SELECT 
    json_data->>'id' AS id,
    json_data->>'summary' AS summary,
    json_data->>'created_at' AS created_at,
    json_data->>'status' AS status,
    json_data->>'resolved_at' AS resolved_at,
    json_data->'service'->>'id' AS service_id,
    json_data->>'severity_renamed' AS severity,
    json_data->'incident'->>'id' AS incident_id,
    json_data->'body'->'details'->>'Description' AS description,
    json_data->'body'->'details'->>'Samples' AS samples,
    COALESCE(json_data->'body'->'details'->>'firing', 'N/A') AS firing
FROM json_data;

```