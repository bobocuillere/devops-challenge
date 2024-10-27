import os
import time
import json
import requests
from dotenv import load_dotenv

print("Starting in 5 seconds...")
time.sleep(5)

load_dotenv()

# Grafana settings
grafana_url = os.getenv('GRAFANA_URL')
grafana_admin_user = os.getenv('GRAFANA_ADMIN_USER')
grafana_admin_password = os.getenv('GRAFANA_ADMIN_PASSWORD')
service_account_name = os.getenv('GRAFANA_SERVICE_ACCOUNT_NAME')
service_account_role = os.getenv('GRAFANA_SERVICE_ACCOUNT_ROLE')

# Database connection settings
# db_host = os.getenv('DB_HOST')
# db_port = int(os.getenv('DB_PORT'))
# db_name = os.getenv('DB_NAME')
# db_user = os.getenv('DB_USER')
# db_password = os.getenv('DB_PASSWORD')

# Function to create a Grafana service account and retrieve the token
def create_grafana_service_account():
    # Authenticate with Grafana API using admin credentials
    auth = (grafana_admin_user, grafana_admin_password)
    headers = {
        'Content-Type': 'application/json'
    }

    # Create the service account
    payload = {
        "name": service_account_name,
        "role": service_account_role
    }

    response = requests.post(f"{grafana_url}/api/serviceaccounts", auth=auth, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        service_account = response.json()
        service_account_id = service_account.get('id')
        print("Service account created successfully.")
    elif response.status_code == 409:
        print("Service account already exists.")
        # Get existing service account ID
        response = requests.get(f"{grafana_url}/api/serviceaccounts/search?name={service_account_name}", auth=auth, headers=headers)
        if response.status_code == 200 and response.json():
            service_account_id = response.json()[0]['id']
        else:
            print(f"Failed to retrieve existing service account: {response.content}")
            return None
    else:
        print(f"Failed to create service account: {response.content}")
        return None

    # Create a token for the service account
    token_payload = {
        "name": "automated_sre_token"
    }

    response = requests.post(f"{grafana_url}/api/serviceaccounts/{service_account_id}/tokens", auth=auth, headers=headers, data=json.dumps(token_payload))

    if response.status_code == 200:
        token_response = response.json()
        token = token_response.get('key')
        print("Service account token created successfully.")
    elif response.status_code == 409:
        print("Service account token already exists.")
        # Retrieve existing tokens
        response = requests.get(f"{grafana_url}/api/serviceaccounts/{service_account_id}/tokens", auth=auth, headers=headers)
        if response.status_code == 200 and response.json():
            token = response.json()[0]['key']
            print("Using existing service account token.")
        else:
            print(f"Failed to retrieve existing service account tokens: {response.content}")
            return None
    else:
        print(f"Failed to create service account token: {response.content}")
        return None

    return token

# Add Prometheus as a data source in Grafana
def add_prometheus_datasource(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    datasource_payload = {
        "name": "Prometheus",
        "type": "prometheus",
        "url": "http://prometheus:9090",
        "access": "proxy",
        "basicAuth": False,
        "jsonData": {
            "timeInterval": "5s"
        }
    }

    datasource_url = f"{grafana_url}/api/datasources"
    response = requests.post(datasource_url, headers=headers, data=json.dumps(datasource_payload))

    if response.status_code == 200:
        print("Prometheus data source added successfully.")
    elif response.status_code == 409:
        print("Prometheus data source already exists.")
    else:
        print(f"Failed to add Prometheus data source: {response.content}")

# Create the Grafana dashboard using the API
def create_grafana_dashboard(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Define the panels for the dashboard
    panels = [
        {
            "title": "CPU Usage",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)",
                    "legendFormat": "{{instance}}",
                    "refId": "A"
                }
            ],
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "percent",
                    "thresholds": {
                        "mode": "percentage",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 70},
                            {"color": "red", "value": 90}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Memory Usage",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
                    "legendFormat": "{{instance}}",
                    "refId": "B"
                }
            ],
            "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "percent",
                    "thresholds": {
                        "mode": "percentage",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 70},
                            {"color": "red", "value": 90}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Rows Inserted Per Second",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "rate(pg_stat_user_tables_n_tup_ins[5m])",
                    "legendFormat": "{{schemaname}}.{{relname}}",
                    "refId": "C"
                }
            ],
            "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "ops",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 100},
                            {"color": "red", "value": 500}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Rows Updated Per Second",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "rate(pg_stat_user_tables_n_tup_upd[5m])",
                    "legendFormat": "{{schemaname}}.{{relname}}",
                    "refId": "D"
                }
            ],
            "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "ops",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 100},
                            {"color": "red", "value": 500}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Rows Deleted Per Second",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "rate(pg_stat_user_tables_n_tup_del[5m])",
                    "legendFormat": "{{schemaname}}.{{relname}}",
                    "refId": "E"
                }
            ],
            "gridPos": {"x": 0, "y": 16, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "ops",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 100},
                            {"color": "red", "value": 500}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Rows Fetched via Sequential Scan Per Second",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "rate(pg_stat_user_tables_seq_tup_read[5m])",
                    "legendFormat": "{{schemaname}}.{{relname}}",
                    "refId": "F"
                }
            ],
            "gridPos": {"x": 12, "y": 16, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "ops",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 1000},
                            {"color": "red", "value": 5000}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "Rows Fetched via Index Scan Per Second",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "rate(pg_stat_user_tables_idx_tup_fetch[5m])",
                    "legendFormat": "{{schemaname}}.{{relname}}",
                    "refId": "G"
                }
            ],
            "gridPos": {"x": 0, "y": 24, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "ops",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 1000},
                            {"color": "red", "value": 5000}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        },
        {
            "title": "PostgreSQL Active Connections",
            "type": "timeseries",
            "datasource": "Prometheus",
            "targets": [
                {
                    "expr": "pg_stat_activity_count{datname='postgres'}",
                    "legendFormat": "{{usename}} - {{state}}",
                    "refId": "H"
                }
            ],
            "gridPos": {"x": 12, "y": 24, "w": 12, "h": 8},
            "fieldConfig": {
                "defaults": {
                    "unit": "none",
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "green", "value": None},
                            {"color": "orange", "value": 50},
                            {"color": "red", "value": 100}
                        ]
                    }
                }
            },
            "options": {
                "showPoints": "never",
                "lineWidth": 2,
                "fillOpacity": 10
            }
        }
    ]

    # Define the dashboard payload
    dashboard_payload = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": "Automated SRE Dashboard",
            "tags": ["automated", "sre", "prometheus"],
            "timezone": "browser",
            "schemaVersion": 30,
            "version": 0,
            "refresh": "5s",
            "panels": panels
        },
        "folderId": 0,
        "overwrite": True
    }

    url = f"{grafana_url}/api/dashboards/db"
    response = requests.post(url, headers=headers, data=json.dumps(dashboard_payload))

    if response.status_code == 200:
        print("Dashboard created successfully.")
    else:
        print(f"Failed to create dashboard: {response.content}")

# Main execution
if __name__ == "__main__":
    token = create_grafana_service_account()
    if token:
        add_prometheus_datasource(token)
        create_grafana_dashboard(token)
    else:
        print("Failed to create service account and token.")
