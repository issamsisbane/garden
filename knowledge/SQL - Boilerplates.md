---
created: "2025-12-04"
---

# SQL - Boilerplates

Create table : 
```sql
CREATE TABLE Utilisateurs (
    id INT PRIMARY KEY,
    nom VARCHAR(50),
    email VARCHAR(100)
);
```

Populate table :
```sql
INSERT INTO Utilisateurs (id, nom, email)
VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com'),
(3, 'Charlie', 'charlie@example.com');
```