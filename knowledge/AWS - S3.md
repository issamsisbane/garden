
[[AWS - Bucket Policies]]

## What is S3 ?

**amazon S3 (Simple Storage Service)** is a highly scalable, **cloud-based object storage** service designed for storing and retrieving data from anywhere on the web. It provides an impressive **99.999999999% durability** (referred to as **11 nines** of durability) and **99.99% availability**, ensuring your data is **protected against loss** and **accessible** when needed. S3 is known for its **large capacity**, **security**, and **reliability**, making it one of the most widely used storage services in cloud computing.

## Components

### Buckets

**Buckets** are the top-level containers used to store objects (data) in S3. Each bucket has a **unique name** across all AWS accounts globally and serves as the organizational unit where data is stored.

**Key Features** :
    - Buckets can be organized with **folders** (virtual directories) to structure your data.
    - **Bucket name** must be unique globally, and by default, AWS allows the creation of up to **100 buckets per account**.
    - **Data governance** can be enforced at the bucket level using **Bucket Policies** (for access control).
### Objects

Objects are the fundamental entities stored in S3, consisting of **data** and associated **metadata**. Each object can range in size from **0 bytes to 5 terabytes** and is identified by a **unique key**.

**Components** :
    - **Actual File**: The data being stored (e.g., an image, video, document).
    - **Metadata**: Information about the object, such as its content type, creation date, and user-defined metadata.

### Keys 

A **key** is a unique identifier for each object within a bucket. It includes the **full path** to the object, similar to a file path in a traditional file system. For example, in the bucket `my-bucket`, the key for an object might be `images/photo.jpg`.

## Features
### Bucket Policies

**Bucket Policies** are **JSON-based access control policies** that allow fine-grained control over who can access your S3 resources and how they can interact with them.

- **Key Features**:
    - Allow or deny access to specific **AWS accounts**, **IAM users**, or **IP ranges**.
    - Grant permissions such as **read**, **write**, or **delete** for objects in the bucket.
    - Enforce **encryption requirements** for objects uploaded to the bucket.
    - Restrict access based on **HTTP referers** or require specific conditions for access.
### Versioning

**Versioning** allows you to **maintain multiple versions** of an object within a bucket. When versioning is enabled, S3 keeps previous versions of objects, allowing you to **recover** from accidental deletions or overwrites.

**Benefits** :
    - **Accidental Deletion Protection**: Restores objects to their previous state in case of deletion.
    - **Compliance**: Meets regulatory requirements for data retention.
    - **Enable or Suspend**: You can enable or suspend versioning at any time. When suspended, existing versions are retained, but new versions are no longer created.
### Lifecycle Policies

**Lifecycle Policies** help automate the management of objects stored in S3. Based on predefined rules, you can transition objects between different **storage classes** or delete them after a certain period.

- **Key Features**:
    - Transition objects to **lower-cost storage classes** (e.g., move data from **Standard** to **Glacier** after a certain period).
    - **Expire objects** after a specified time to free up space and reduce costs.
    - **Delete previous versions** of objects based on defined retention policies.

Lifecycle policies help **optimize costs** by automatically transitioning data to more cost-effective storage tiers as its usage decreases.
## S3 Storage Classes

### Standard

**Frequently** **Accessed** Data & Requires durability & availability

### Intelligent

**Unknown** or **changing** Access Patterns. It automatically moves the data to the most cost effective access tier.

### Infrequent Access (IA)

**Less Frequently accessed** data that requires rapid access when needed.

### One Zone-InfrequentAccess (IA)

Data is stored in a **Single Availability** Zone & Costs 20% less than Standard IA. **Infrequently Accessed** data that doesn't need to be replicated across multiple AZs.

### Glacier and Glacier Deep Archive

Lowest-cost Storage for **Data Archiving** & **Long term** Backup.
For **Infrequently accessed data** and when several hours of retrieval time is suitable.

## Use Cases

### Website Hosting

Amazon S3 can be used to **host static websites**. S3’s automatic scalability allows it to handle large amounts of traffic without requiring manual intervention.

### Backup & Restore

S3 is widely used as a **primary storage** solution for disaster recovery.

### Archive

With **S3 Glacier** and **S3 Glacier Deep Archive**, you can easily move data to **low-cost storage** for long-term data retention.

### Big Data Analytics

**Store** and **analyze** Massive Data Sets using [[AWS Athena]] or[[ AWS Redshift]].

### Media Files

Amazon S3 is ideal for storing and distributing **unstructured data** like media files (images, videos, and audio).

