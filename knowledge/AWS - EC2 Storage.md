It exists 2 types of storage within EC2 instances : 
### Amazon EBS
Amazon Elastic Block Store is an external hard drive that we can connect to EC2.
If we terminate the instance associated to the EBS, our data remained intact.

**EBS Volumes types :**

| Types                    | Name | Usage                                                                          |
| ------------------------ | ---- | ------------------------------------------------------------------------------ |
| General Purpose SSD      | `gp2`  | Boot Volumes, Dev & Test Env, Low-latency Interactive Applications             |
| Provisioned IOPS SSD     | `io1`  | I/O-Intensive Workloads ==(Large Database and Mission-critical Applications)== |
| Throughput Optimized HDD | `st1`  | Throughput-intensive Workloads ==(Big Data, Data Warehouses, Log Processing)== |
| Cold HDD                 | `sc1`  | Less Frequently Accessed Workloads ==(Backups & archives)==                    |
To **choose** a volume type, we need to **consider** : 
- Performance Requirements
- Durability Needs
- Budget Constraints
### Instance Store

It's a temporary storage and provides fast access to the data.
If we terminate the instance associated to the EBS, our data will be lost.