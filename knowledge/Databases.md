[[CEA - Week 1 - Cloud Fondamentals]]

A **database** is a **structured collection of data** that is stored electronically on a computer system. The main purpose of a database is to make it easy to:

- **Access**
- **Manipulate**
- **Update**
- **Retrieve** data<
Databases play a crucial role in ensuring **data integrity** and **data consistency**, which is essential for maintaining the **accuracy** and **reliability** of information in various applications.

---

## Types of Databases

There are different types of databases, each designed for specific use cases and data management needs.

### Relational Databases

**Relational databases** use a structured approach that allows data to be identified and accessed based on its relationship to other data within the database. The data in relational databases is stored in **tables** (often called **relations**), which consist of rows and columns.

- **Tables**: Each table holds a specific type of data, and relationships can be established between different tables.
- **Structured Query Language (SQL)**: SQL is the standard language used to interact with relational databases.

Common examples of relational databases include:

- **MySQL**
- **PostgreSQL**
- **Microsoft SQL Server**
- **Oracle Database**

Relational databases are ideal for scenarios that require **complex queries** and **data integrity** across multiple data types.

### Non-Relational Databases (NoSQL)

**Non-relational databases**, often referred to as **NoSQL databases**, offer a more **flexible** approach to data storage. Instead of relying on structured tables, NoSQL databases store data in various formats, such as:

- **Document databases**: Store data in **JSON** or **XML** documents (e.g., **MongoDB**).
- **Graph databases**: Store data as **nodes** and **edges** to represent relationships (e.g., **Neo4j**).
- **Key-value stores**: Use **key-value pairs** for fast data retrieval (e.g., **Redis**, **DynamoDB**).
- **Wide-column stores**: Store data in rows and columns but are more flexible than relational databases (e.g., **Cassandra**, **HBase**).

NoSQL databases are often used for handling **large volumes of unstructured data** and offer **scalability** and **performance** for specific workloads like **real-time data processing**.

---

## Database as an Integral Part of Applications

Databases are an **integral part** of an application's **backend**, interacting with the **business logic** to **process**, **retrieve**, and **store data** based on user interactions. Applications communicate with databases using:

- **APIs (Application Programming Interfaces)**: APIs act as intermediaries that allow applications to send queries and receive responses from the database.
- **Database drivers**: Software components that enable applications to communicate directly with the database by translating application requests into database commands.

These connections are often defined using **connection strings**, which specify parameters for establishing the connection with the database, including:

- **Database type** (e.g., MySQL, MongoDB)
- **Server name** (e.g., IP address or domain)
- **Credentials** (e.g., username and password)
- **Specific database** to access (if multiple databases are hosted on the same server)

Connection strings ensure secure and efficient communication between the application and the database.

---

## CRUD Operations

Most databases perform the four basic **CRUD** operations, which are essential for managing data:

- **Create**: Insert new data into the database.
- **Read**: Retrieve existing data from the database.
- **Update**: Modify existing data within the database.
- **Delete**: Remove data from the database.

These operations are fundamental to any application that requires data management, whether it's for a small personal app or a large-scale enterprise system.

---

## Importance of Databases in Application Development

Databases are critical for ensuring the **smooth functioning** of applications by providing:

- **Data integrity**: Ensuring that data remains accurate and consistent across the system.
- **Efficiency**: Optimizing the storage and retrieval of data for **high-performance** applications.
- **Scalability**: Allowing applications to scale and handle increased workloads by distributing data effectively (especially important in cloud-based and NoSQL systems).

Additionally, databases help manage **transactions**, ensuring that complex sets of operations are executed **atomically** and **securely**, preventing data corruption or inconsistency.