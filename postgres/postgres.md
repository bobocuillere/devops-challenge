# 1. Answers for Database Architecture and Design

When designing a database architecture for such a demanding environment, several key factors need to be considered:

- **Scalability**: The ability to handle increasing workloads by adding resources.
- **High Availability**: Ensuring the system is operational and accessible even in the event of failures.
- **Fault Tolerance**: The system's ability to continue operating properly in the event of the failure of some of its components.
- **Performance**: Low-latency responses for queries and transactions.

## Proposed Database Architectures

### Master-Slave Replication (Primary-Replica)
One server acts as the primary (master) handling all write operations, while one or more replicas (slaves) handle read operations.

#### Advantages
- **Improved Read Performance**: Read queries can be distributed among replicas.
- **Fault Tolerance**: If the primary fails, a replica can be promoted to primary.
- **Simplicity**: Easier to set up and manage compared to more complex architectures.

#### Drawbacks
- Primary can become a write bottleneck; replication lag may cause stale reads.
- Replicas might lag behind the primary, leading to stale reads.

### Master-Master Replication (Multi-Master)
Multiple servers act as masters, handling both read and write operations. Data is synchronized between masters.

#### Advantages
- **Load Balancing**: Distributes both read and write loads.
- **High Availability**: If one master fails, others continue operating.
- **Scalability**: Better scalability for write-heavy applications.

#### Drawbacks
- **Conflict Resolution**: Concurrent writes can lead to data conflicts.
- **Complexity**: Harder to set up and maintain.
- **Latency**: Synchronous replication can introduce latency; asynchronous replication can lead to inconsistencies.

### Sharding (Horizontal Partitioning)
Data is partitioned across multiple servers (shards), each responsible for a subset of the data.

#### Advantages
- **Horizontal Scalability**: Easily add more shards to handle increased load.
- **Performance**: Reduces the amount of data each server handles.
- **Fault Isolation**: Issues in one shard don't affect others.

#### Drawbacks
- **Complexity**: Requires logic to route queries to the correct shard.
- **Maintenance Overhead**: Adding/removing shards requires data rebalancing.
- **Cross-Shard Queries**: Complex to perform joins and transactions across shards.

### Distributed Databases (e.g., NoSQL Solutions)
Use of distributed database systems like Cassandra, MongoDB designed for horizontal scaling and fault tolerance.

#### Advantages
- **Scalability**: Designed to handle large volumes of data and high throughput.
- **Fault Tolerance**: Data is replicated across nodes.
- **Flexible Schema**: Suitable for unstructured or semi-structured data.

#### Drawbacks
- **Consistency Models**: Often use eventual consistency, which may not be acceptable for all applications.
- **Data Model Changes**: May require significant changes to the application.
- **Learning Curve**: Requires expertise to manage and optimize.

### Cloud-Based Managed Services
Utilize managed database services like Amazon RDS, Google Cloud SQL, or Azure Database for PostgreSQL.

#### Advantages
- **Ease of Use**: Simplifies setup and maintenance.
- **Built-in High Availability**: Automated failover and backups.
- **Scalability**: Easy to scale resources up or down.

#### Drawbacks
- **Cost**: Can be more expensive than self-managed solutions.
- **Vendor Lock-In**: Dependence on a specific cloud provider.
- **Limited Control**: Less flexibility in configuration and optimization.

## Recommended Architecture

### Combination of Sharding with Master-Slave Replication
#### Master-Slave Replication
- **Scale Reads**: Distribute read queries across replicas to reduce load on the primary.
- **High Availability**: In case of primary failure, a replica can be promoted.

#### Sharding
- **Scale Writes**: Distribute data across multiple primaries (shards), each responsible for a portion of the data.
- **Reduced Latency**: Queries are processed on smaller datasets.

#### Advantages
- **Balanced Load**: Both read and write operations are scaled.
- **Fault Tolerance**: Failure in one shard doesn't bring down the entire system.
- **Low Latency**: Data is partitioned, reducing query response times.

#### Drawbacks
- **Complexity**: Requires careful design and management.
- **Application Changes**: Application logic must handle data routing and possibly handle cross-shard operations.
- **Operational Overhead**: Monitoring and maintaining multiple nodes and shards.

### Justification
This architecture combines the strengths of both replication and sharding, providing scalability, high availability, and performance. While it introduces complexity, the benefits align well with the requirements of processing millions of transactions daily with low latency and high fault tolerance.

# 2. Answers for Performance Tuning and Query Optimization

### Analysis of the Query
```sql
SELECT *
FROM test_data
WHERE LOWER(name) LIKE '%test%'
ORDER BY age DESC
LIMIT 10;
```

#### Potential Issues
- The use of `LOWER(name)` combined with `LIKE '%test%'` forces a full table scan, as indexes cannot be effectively utilized.
- Applying `LOWER()` to the name column prevents the use of standard indexes on name.
- The `%` at the beginning of the pattern (`'%test%'`) means the database cannot use an index to speed up the search.

#### Optimizations
- **Create an Index on `LOWER(name)`**:
    ```sql
    CREATE INDEX idx_lower_name ON test_data (LOWER(name));
    ```

- **Use Trigram Indexing**:
    - **Install Extension**:
        ```sql
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        ```
    - **Create Index**:
        ```sql
        CREATE INDEX idx_name_trgm ON test_data USING gin (LOWER(name) gin_trgm_ops);
        ```

- **Create Index on `age`**:
    ```sql
    CREATE INDEX idx_age ON test_data (age DESC);
    ```

- **Rewrite Query if Possible**:
    - **Use Full-Text Search**:
        ```sql
        ALTER TABLE test_data ADD COLUMN name_tsv tsvector GENERATED ALWAYS AS (to_tsvector('simple', name)) STORED;
        CREATE INDEX idx_name_tsv ON test_data USING gin (name_tsv);
        SELECT * FROM test_data WHERE name_tsv @@ plainto_tsquery('test') ORDER BY age DESC LIMIT 10;
        ```

## Backup and Disaster Recovery

### Task 1: Design a Backup Strategy

#### Requirements
- Ensure regular backups.
- Minimize performance impact.

#### Backup Strategy
- **Full Backups**:
    - Perform a full backup of the database weekly during low-traffic periods.
    - Use `pg_basebackup` or other tools like `pgBackRest`.

- **Incremental Backups (WAL Archiving)**:
    - Enable continuous archiving of WAL files.
    - Configure `archive_mode` and `archive_command` in `postgresql.conf`.

- **Point-In-Time Recovery (PITR)**:
    - Allows restoration to any point in time by replaying WAL files.
    - Provides flexibility in recovery scenarios.

- **Backup Automation**:
    - Schedule backups using cron jobs or task schedulers.
    - Monitor backup jobs for success or failure.

- **Backup Storage**:
    - Store backups on separate physical storage or cloud storage solutions.
    - Ensure backups are encrypted and access-controlled.

### Task 2: Steps to Restore the Database

#### Prepare the New Server
- Install the same version of PostgreSQL.
- Configure `postgresql.conf` and `pg_hba.conf` as needed.

#### Restore the Latest Full Backup
- Copy the latest full backup to the new server.
- Ensure correct ownership and permissions.

#### Set Up Recovery Configuration
- Create a `recovery.conf` file (for PostgreSQL versions prior to 12) or modify `postgresql.conf` with recovery parameters.
    ```conf
    restore_command = 'cp /path/to/archive/%f %p'
    recovery_target_time = 'YYYY-MM-DD HH:MM:SS'  # Optional
    ```

#### Start the PostgreSQL Service
- Start the service; it will enter recovery mode and begin restoring WAL files.

#### Monitor the Recovery Process
- Check logs to ensure WAL files are being applied.
- Wait for the recovery to complete.

#### Verify the Restored Database
- Connect to the database and perform sanity checks.
- Ensure data integrity and consistency.

#### Reconfigure for Normal Operation
- Remove or rename the recovery.conf file if applicable.
- Restart the PostgreSQL service to enter normal operation.

### Task 3: Analyze Replication Lag

#### Observation
```sql
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;
```
```
 replication_lag 
-----------------
 00:55:00.115093
```

#### Analysis
- The standby server is 55 minutes behind the primary server.
- This indicates a significant replication lag.

#### Potential Causes
- **High Write Volume**: The primary is generating WAL files faster than the standby can apply them.
- **Network Issues**: Slow or unstable network connection between primary and standby.
- **Resource Constraints**: The standby server may be under-resourced (CPU, RAM, I/O).
- **Disk I/O Bottlenecks**: Slow disk performance on the standby.
- **Replication Configuration Issues**: Incorrect settings causing delays.

### Task 4: Causes of Delay and Monitoring

#### Possible Causes of Delay
- **Network Latency**: High latency or packet loss affecting data transfer.
- **Disk Throughput**: Insufficient disk I/O performance on the standby.
- **Heavy Load**: Standby server is overloaded with other tasks.
- **Configuration Errors**: Incorrect settings in `postgresql.conf` or `recovery.conf`.

#### Monitoring Replication Lag
- **Use Monitoring Tools**: Implement tools like Prometheus with Grafana for visualization.
- **Check Replication Statistics**:
    ```sql
    SELECT
        client_addr,
        state,
        sent_lsn,
        write_lsn,
        flush_lsn,
        replay_lsn,
        (pg_current_wal_lsn() - replay_lsn) AS byte_lag
    FROM pg_stat_replication;
    ```
- **Set Up Alerts**: Configure alerts when replication lag exceeds a threshold.

#### General Strategies for Monitoring PostgreSQL
- **System Metrics**: Monitor CPU, memory, disk I/O, and network usage.
- **Database Metrics**: Track connections, replication status, query performance.
- **Logs**: Collect and analyze PostgreSQL logs for errors and warnings.
- **Regular Health Checks**: Perform routine checks on indexes, vacuuming, and bloat.
- **Security Monitoring**: Watch for unauthorized access attempts.

## Database Security

### Task 1: Safeguarding Against SQL Injection

#### Recommendations
- **Use Prepared Statements**:
    - Always use parameterized queries.
    - Prevents user input from altering SQL command structure.

- **Input Validation**:
    - Validate and sanitize all user inputs on the client and server sides.
    - Enforce data types and expected formats.

- **Least Privilege Principle**:
    - Limit database user permissions to only necessary operations.
    - Avoid using superuser roles for application connections.

- **Stored Procedures**:
    - Encapsulate database logic in stored procedures.
    - Restrict direct access to tables.

- **Web Application Firewalls (WAF)**:
    - Implement a WAF to detect and block malicious traffic.

- **Regular Updates and Patches**:
    - Keep database software up to date to mitigate known vulnerabilities.

### Task 2: Managing and Securing User Permissions

#### Best Practices
- **Role-Based Access Control (RBAC)**:
    - Create roles for different access levels.
    - Assign users to roles rather than granting permissions directly.

- **Strong Authentication Methods**:
    - Use `scram-sha-256` for password authentication.
    - Enforce strong password policies.

- **Regular Audits**:
    - Periodically review user permissions.
    - Remove unnecessary accounts and privileges.

- **Logging and Monitoring**:
    - Enable detailed logging of user activities.
    - Monitor logs for suspicious behavior.

- **Use Connection Encryption**:
    - Require SSL/TLS connections to secure data in transit.

- **Separation of Duties**:
    - Separate administrative duties among different users to reduce risk.

### Task 3: Encrypting Sensitive Data

#### Approach
- **Transparent Data Encryption (TDE)**:
    - Encrypt data files at the storage level.
    - PostgreSQL supports TDE through third-party tools or custom implementations.

- **Column-Level Encryption**:
    - Use PostgreSQL's `pgcrypto` module.
    - Encrypt specific columns containing sensitive data.
        ```sql
        -- Encrypt data
        UPDATE table SET sensitive_column = pgp_sym_encrypt('data', 'key');
        -- Decrypt data
        SELECT pgp_sym_decrypt(sensitive_column, 'key') FROM table;
        ```

- **Application-Level Encryption**:
    - Encrypt data within the application before storing it.
    - Decryption occurs in the application layer.

#### Key Management
- Use secure key management practices.
- Store encryption keys securely and separately from the data.

#### Compliance and Standards
- Ensure encryption methods meet industry standards and compliance requirements (e.g., GDPR, HIPAA).

## 5. Troubleshooting and Incident Response

### Task 1: Database Monitoring, Dashboard Improvement, and Metrics Explanation

#### Database Issues to Monitor
- **Connection States**: Monitor active, idle, and idle-in-transaction connections to ensure optimal resource usage and prevent connection leaks.
- **Longest Connections**: Keep an eye on connections that have been open for a long time, as they might indicate unoptimized queries or sessions.
- **Block Hit Ratios**: Low block hit ratios for indexes, databases, or heap tables could indicate a need for better indexing, caching, or adjustments in query optimization.
- **Max Connections**: Regularly monitor the maximum connections to prevent hitting the limit and causing service issues.
- **Uptime and Corruptions**: Ensure the database uptime is stable and monitor for corruption issues that could affect data integrity.

#### Dashboard Improvement Suggestions
- **Alerts and Thresholds**: Set up visual alerts for key metrics such as high active connections, low block hit ratios, or high connection duration.
- **Connection Trends**: Add visualizations for connections over time to quickly detect spikes or unusual patterns.
- **Cache Hit Ratio Visualization**: Add panels to separate cache hit ratios for different database objects (e.g., table vs. index) to gain insights on where optimization is most needed.
- **Error Logs**: Include a panel for recent error logs or anomalies that may hint at underlying issues.

#### Best Practices for Monitoring PostgreSQL
- **Track Connection Limits**: Monitor the number of active connections to avoid maxing out connections, which can disrupt service.
- **Block Hit Ratios**: Monitor block hit ratios to assess cache efficiency and identify tables or indexes that may need optimization.
- **Long-running Queries**: Track long-running queries to identify potential optimizations or indexing opportunities.
- **Replication Lag**: For high-availability setups, monitor replication lag to ensure secondary nodes are up-to-date.

#### Explanation of "Blocks Hit Ratio" for Indexes
The Blocks Hit Ratio for indexes represents the percentage of index reads served from memory (cache) rather than disk. A high ratio indicates that most index data is in memory, which is ideal for performance.

#### Explanation of "Block Hit Ratio" in a Database
The Block Hit Ratio in a database measures the efficiency of the database’s cache by showing the percentage of data requests that are served from memory rather than requiring disk access.

#### Explanation of "Block Hit Ratio" for Heap Tables
The Block Hit Ratio for heap tables measures the cache efficiency specifically for table data stored in the heap. A low ratio suggests that more data reads are hitting the disk, which can slow down performance.

#### How to Calculate Block Hit Ratio
**Formula**:
\[ \text{Block Hit Ratio} = \frac{\text{cache hits}}{\text{cache hits} + \text{disk reads}} \]

### Task 2: WAL Availability Error and Resolution

#### Error Log Analysis
```
Aug 19 07:18:40 secondary.node postgres[135986]: LOG:  waiting for WAL to become available at 0/1002000
Aug 19 07:18:45 secondary.node  postgres[450523]: FATAL:  could not connect to the primary server: connection to server at "primary.node" (10.10.10.00), port 5432 failed: FATAL:  no pg_hba.conf entry for re...
```

#### Cause
The secondary node is attempting to retrieve WAL (Write-Ahead Log) files for replication, but they are not available. This is often due to:
- **Network Connectivity Issues**: The connection between the primary and secondary nodes is failing.
- **Missing pg_hba.conf Entry**: The primary server is rejecting connections from the secondary due to missing or incorrect entries in the `pg_hba.conf` file.

#### Solution
- **Network Check**: Ensure that the secondary node can reach the primary node on port 5432.
- **Update pg_hba.conf**: Add an entry to allow the secondary node’s IP to connect to the primary server for replication.
    ```plaintext
    host replication all <secondary_IP>/32 md5
    ```
- **Reload Configurations**: Reload PostgreSQL on the primary server to apply the changes:
    ```bash
    sudo systemctl reload postgresql
    ```
- **WAL Retention**: Ensure the primary server retains sufficient WAL files for replication.

### Task 3: "Too Many Clients" Error and Solution

#### Error Log Analysis
```
psql: connection to server on socket /var/run/postgresql/.s.PGSQL.5432 failed: FATAL:  sorry, too many clients
```

#### Cause
This error occurs when the number of client connections exceeds the PostgreSQL `max_connections` setting, causing new connection attempts to be denied.

#### Solution
- **Increase `max_connections`**: Modify the `postgresql.conf` file to increase the `max_connections` limit.
    ```plaintext
    max_connections = 500  # Adjust as needed
    ```
    Then, reload PostgreSQL:
    ```bash
    sudo systemctl reload postgresql
    ```

- **Optimize Connection Management**:
    - Implement a connection pooler like PgBouncer to manage connections efficiently.
    - Review application-side connection handling to ensure that idle connections are closed.
    - Analyze query performance and optimize long-running queries to reduce the need for prolonged connections.

- **Monitor Connection Usage**: Regularly monitor the number of active connections to proactively address potential issues before reaching the limit again.
