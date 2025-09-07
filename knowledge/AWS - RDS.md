The relational AWS managed  Database.
AWS take care of provisioning, configuration, patching and backups.

Under the hood RDS is built on top of EC2.
We can use many databases engines such as : 
* MySQL
* PostgresSQL
* MariaDB
* Oracle DB

### Benefits

#### Multi-AZ
Databases are **replicate** accross **multiple** **AZs**. It improves reliability and availability.
#### Automatic failover
There is an **automatic** failover **to** the standby instance which allows our database to still running.

#### Read Replicas
Allow to handle the **read-only workloads** to make the database less charge. Our master database would not become overloaded. We will have one databases for writing data and one for reading data. We can place read replicas in **other regions**.

#### Automatic Backups
It happens **once a day** and includes both : **RDS Instance** and **Transaction logs**. We can choose **Retention Period** (up to 35 days). If we want to keep it longer we have to create **manual snapshots** of our database. We can stored the backups in AWS S3.