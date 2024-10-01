# How to use pdpyras to get incidents

## Environment setup
- Install virtualenv
- Install dependencies by using 
    ```python
        pip install -r requirements.txt
    ```
- Create a .env file with your token. Otherwise the code will not function.
    - Sample .env
        ```python
            API_TOKEN=[[your token here]]
        ```


- Check if you are able to use pdpyras with your token by running get_started.ipynb

## Incidents
- Some test Curl commands

```curl

1. 
curl --request GET \
  --url https://api.pagerduty.com/incidents/618437 \
  --header 'Accept: application/json' \
  --header 'Authorization: Token token=xxxxxxxxxxxx' \
  --header 'Content-Type: application/json'
 
2. 
curl --request GET \
  --url https://api.pagerduty.com/log_entries/R510G5L4K6AN1JNTFQ7SI8AAKF \
  --header 'Accept: application/json' \
  --header 'Authorization: Token token=xxxxxxxxxxx' \
  --header 'Content-Type: application/json'

```

- Detail curl incidents get

```json 
curl --request GET -k \                                                                                         curl --request GET -k \
  --url https://api.pagerduty.com/incidents/618441 \
  --header 'Accept: application/json' \
  --header 'Authorization: Token token=xxxxxxxxxxxxxxxx' \
  --header 'Content-Type: application/json' | jq

{
  "incident": {
    "incident_number": 618441,
    "title": "[PROD-WEST] OpenSearch Cluster Yellow",
    "description": "[PROD-WEST] OpenSearch Cluster Yellow",
    "created_at": "2024-09-14T05:31:38Z",
    "updated_at": "2024-09-14T05:41:38Z",
    "status": "resolved",
    "incident_key": null,
    "service": {
      "id": "PYWUGEI",
      "type": "service_reference",
      "summary": "Nebula Infrastructure (Production)",
      "self": "https://api.pagerduty.com/services/PYWUGEI",
      "html_url": "https://hpe-hcss.pagerduty.com/service-directory/PYWUGEI"
    },
    "assignments": [],
    "assigned_via": "escalation_policy",
    "last_status_change_at": "2024-09-14T05:41:38Z",
    "resolved_at": "2024-09-14T05:41:38Z",
    "first_trigger_log_entry": {
      "id": "R9P6NP9XGGRS0ZGD87PFNAF038",
      "type": "trigger_log_entry_reference",
      "summary": "Triggered through the API.",
      "self": "https://api.pagerduty.com/log_entries/R9P6NP9XGGRS0ZGD87PFNAF038",
      "html_url": "https://hpe-hcss.pagerduty.com/incidents/Q0TUTXDJ0P1RRT/log_entries/R9P6NP9XGGRS0ZGD87PFNAF038"
    },
    "alert_counts": {
      "all": 1,
      "triggered": 0,
      "resolved": 1
    },
    "is_mergeable": true,
    "escalation_policy": {
      "id": "PU9VW8E",
      "type": "escalation_policy_reference",
      "summary": "Nebula Infrastructure (Production)",
      "self": "https://api.pagerduty.com/escalation_policies/PU9VW8E",
      "html_url": "https://hpe-hcss.pagerduty.com/escalation_policies/PU9VW8E"
    },
    "teams": [
      {
        "id": "PT5QHAT",
        "type": "team_reference",
        "summary": "Nebula Operations",
        "self": "https://api.pagerduty.com/teams/PT5QHAT",
        "html_url": "https://hpe-hcss.pagerduty.com/teams/PT5QHAT"
      }
    ],
    "impacted_services": [
      {
        "id": "PYWUGEI",
        "type": "service_reference",
        "summary": "Nebula Infrastructure (Production)",
        "self": "https://api.pagerduty.com/services/PYWUGEI",
        "html_url": "https://hpe-hcss.pagerduty.com/service-directory/PYWUGEI"
      }
    ],
    "pending_actions": [],
    "acknowledgements": [],
    "basic_alert_grouping": null,
    "alert_grouping": null,
    "last_status_change_by": {
      "id": "PYWUGEI",
      "type": "service_reference",
      "summary": "Nebula Infrastructure (Production)",
      "self": "https://api.pagerduty.com/services/PYWUGEI",
      "html_url": "https://hpe-hcss.pagerduty.com/service-directory/PYWUGEI"
    },
    "priority": {
      "id": "PWIZE3V",
      "type": "priority",
      "summary": "P3",
      "self": "https://api.pagerduty.com/priorities/PWIZE3V",
      "html_url": null,
      "account_id": "PD6TKZD",
      "color": "f9b406",
      "created_at": "2019-10-10T09:42:23Z",
      "description": "",
      "name": "P3",
      "order": 65536,
      "schema_version": 0,
      "updated_at": "2023-01-07T01:29:14Z"
    },
    "resolve_reason": null,
    "incidents_responders": [],
    "responder_requests": [],
    "subscriber_requests": [],
    "urgency": "low",
    "id": "Q0TUTXDJ0P1RRT",
    "type": "incident",
    "summary": "[#618441] [PROD-WEST] OpenSearch Cluster Yellow",
    "self": "https://api.pagerduty.com/incidents/Q0TUTXDJ0P1RRT",
    "html_url": "https://hpe-hcss.pagerduty.com/incidents/Q0TUTXDJ0P1RRT"
  }
}
```


- Get alerts for incident id : Q0TUTXDJ0P1RRT

```bash
iyusuf@TJGX55ZMES:/mnt/c/Users/yusufi/OneDrive - Hewlett Packard Enterprise/SHARED_ONEDRIVE_HPEIY/data$ curl --request GET -k   --url https://api.pagerduty.com/incidents/Q0TUTXDJ0P1RRT/alerts   --header 'Accept: application/json'   --header 'Authorization: Token token=XXXXXXXXXXXXXXXXX'   --header 'Content-Type: application/json' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4585  100  4585    0     0  16104      0 --:--:-- --:--:-- --:--:-- 16144
{
  "alerts": [
    {
      "id": "Q1RPVEX3LK98BU",
      "type": "alert",
      "summary": "[PROD-WEST] OpenSearch Cluster Yellow",
      "self": "https://api.pagerduty.com/alerts/Q1RPVEX3LK98BU",
      "html_url": "https://hpe-hcss.pagerduty.com/alerts/Q1RPVEX3LK98BU",
      "created_at": "2024-09-13T23:31:38-06:00",
      "status": "resolved",
      "resolved_at": "2024-09-13T23:41:38-06:00",
      "alert_key": "363f4374a7e469ae910b3c1fe6508012b94e1a7c37346a385101dd23e0a1b2d4",
      "suppressed": false,
      "service": {
        "id": "PYWUGEI",
        "type": "service_reference",
        "summary": "Nebula Infrastructure (Production)",
        "self": "https://api.pagerduty.com/services/PYWUGEI",
        "html_url": "https://hpe-hcss.pagerduty.com/service-directory/PYWUGEI"
      },
      "severity": "warning",
      "incident": {
        "id": "Q0TUTXDJ0P1RRT",
        "type": "incident_reference",
        "summary": "[#618441] [PROD-WEST] OpenSearch Cluster Yellow",
        "self": "https://api.pagerduty.com/incidents/Q0TUTXDJ0P1RRT",
        "html_url": "https://hpe-hcss.pagerduty.com/incidents/Q0TUTXDJ0P1RRT"
      },
      "first_trigger_log_entry": {
        "id": "RRWLUJVIHA3UWZVW9WEKZOO2P5",
        "type": "trigger_log_entry_reference",
        "summary": "Triggered through the API.",
        "self": "https://api.pagerduty.com/log_entries/RRWLUJVIHA3UWZVW9WEKZOO2P5",
        "html_url": "https://hpe-hcss.pagerduty.com/alerts/Q1RPVEX3LK98BU/log_entries/RRWLUJVIHA3UWZVW9WEKZOO2P5"
      },
      "body": {
        "contexts": [
          {
            "type": "link",
            "href": "https://hcss.atlassian.net/wiki/x/AQAk1",
            "text": "Runbook"
          },
          {
            "type": "link",
            "href": "https://grafana.bravo.cloudcruiser.com/d/JQn6RpBVz/opensearch?var-env=prod-west&var-interval=60m",
            "text": "Grafana Dashboard"
          },
          {
            "type": "link",
            "href": "https://prometheus.prod-west.cloudcruiser.com/graph?g0.expr=elasticsearch_cluster_health_status%7Bcolor%3D%22yellow%22%7D+%3D%3D+1&g0.tab=1",
            "text": "Prometheus Query"
          }
        ],
        "details": {
          "description": "The OpenSearch cluster is degraded, action may be needed.",
          "environment": "prod-west",
          "firing": "Labels:\n - alertname = OpenSearchClusterYellow\n - cluster = 245087973473:prod-west\n - color = yellow\n - env = prod-west\n - instance = prod-west-external-monitor\n - job = opensearch\n - monitor = prometheus-prod-west-1\n - severity = warning\n - team = devops\nAnnotations:\n - dashboard = https://grafana.bravo.cloudcruiser.com/d/JQn6RpBVz/opensearch?var-env=prod-west&var-interval=60m\n - description = The OpenSearch cluster is degraded, action may be needed.\n - runbook = https://hcss.atlassian.net/wiki/x/AQAk1\n - summary = OpenSearch Cluster Yellow\nSource: https://prometheus.prod-west.cloudcruiser.com/graph?g0.expr=elasticsearch_cluster_health_status%7Bcolor%3D%22yellow%22%7D+%3D%3D+1&g0.tab=1\n",
          "instance": "prod-west-external-monitor\n            ",
          "num_firing": "1",
          "num_resolved": "0",
          "resolved": "",
          "service_name": "",
          "summary": "[PROD-WEST] OpenSearch Cluster Yellow",
          "team": "devops"
        },
        "cef_details": {
          "client": "Alertmanager",
          "client_url": "https://alertmanager.prod-west.cloudcruiser.com/#/alerts?receiver=pagerduty",
          "contexts": [
            {
              "href": "https://hcss.atlassian.net/wiki/x/AQAk1",
              "text": "Runbook",
              "type": "link"
            },
            {
              "href": "https://grafana.bravo.cloudcruiser.com/d/JQn6RpBVz/opensearch?var-env=prod-west&var-interval=60m",
              "text": "Grafana Dashboard",
              "type": "link"
            },
            {
              "href": "https://prometheus.prod-west.cloudcruiser.com/graph?g0.expr=elasticsearch_cluster_health_status%7Bcolor%3D%22yellow%22%7D+%3D%3D+1&g0.tab=1",
              "text": "Prometheus Query",
              "type": "link"
            }
          ],
          "dedup_key": "363f4374a7e469ae910b3c1fe6508012b94e1a7c37346a385101dd23e0a1b2d4",
          "description": "[PROD-WEST] OpenSearch Cluster Yellow",
          "details": {
            "description": "The OpenSearch cluster is degraded, action may be needed.",
            "environment": "prod-west",
            "firing": "Labels:\n - alertname = OpenSearchClusterYellow\n - cluster = 245087973473:prod-west\n - color = yellow\n - env = prod-west\n - instance = prod-west-external-monitor\n - job = opensearch\n - monitor = prometheus-prod-west-1\n - severity = warning\n - team = devops\nAnnotations:\n - dashboard = https://grafana.bravo.cloudcruiser.com/d/JQn6RpBVz/opensearch?var-env=prod-west&var-interval=60m\n - description = The OpenSearch cluster is degraded, action may be needed.\n - runbook = https://hcss.atlassian.net/wiki/x/AQAk1\n - summary = OpenSearch Cluster Yellow\nSource: https://prometheus.prod-west.cloudcruiser.com/graph?g0.expr=elasticsearch_cluster_health_status%7Bcolor%3D%22yellow%22%7D+%3D%3D+1&g0.tab=1\n",
            "instance": "prod-west-external-monitor\n            ",
            "num_firing": "1",
            "num_resolved": "0",
            "resolved": "",
            "service_name": "",
            "summary": "[PROD-WEST] OpenSearch Cluster Yellow",
            "team": "devops"
          },
          "severity": "warning",
          "source_origin": "Alertmanager"
        },
        "type": "alert_body"
      },
      "integration": null,
      "privilege": null
    }
  ],
  "limit": 25,
  "offset": 0,
  "more": false,
  "total": null
}


```