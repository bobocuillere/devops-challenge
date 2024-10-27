### Monitoring Step

#### Hardcoded Version Choice
- **PostgreSQL 16.4** and **PostgreSQL Exporter v0.15.0** : I chose to hardcode the versions because I encounter compatibility issues with postgres 17 and the postgres exporter.

#### Steps After `docker-compose up`
1. **Initialization**:
   - `init.sql` will be run to generates necessary database activity to expose table-level metrics.

2. **Confirm Metrics in Prometheus**:
   - Open **Prometheus** at `http://localhost:9090` and go to **Status -> Targets**. Ensure `node-exporter`, `postgresql_exporter`, and `prometheus` are `UP`.
   - Check for PostgreSQL metrics (e.g., `pg_stat_user_tables_seq_scan`), verifying data flow.

3. **Check Alerts**:
   - Visit **Status -> Alerts** in Prometheus to see if conditions meet alert thresholds.
   - Confirm alerts route to **Alertmanager** at `http://localhost:9093`.

#### Automated Grafana Dashboard Creation

1. Make sure `.env` is configured with Grafana and database credentials.
You can choose the different value for Login, Password etc... in that file.
Run `dashboard-creation.py`:


   ```bash
   python3 dashboard-creation.py

This script will do the following:

- Creating a Service Account with a token.
- Adding Prometheus as a Data Source in Grafana.
- Creating Dashboards with pre-configured panels for CPU, memory, and PostgreSQL   metrics (insertions, updates, deletions).